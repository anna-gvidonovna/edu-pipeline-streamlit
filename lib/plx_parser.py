"""
PLX Parser - парсинг файлов учебных планов в формате PLX (XML)
Адаптировано из Notebook 1: PLX -> XML_JSON
"""

import xml.etree.ElementTree as ET
import re
import json
from typing import Dict, List, Any, Optional
from io import BytesIO


def clean_tag_name(tag: str) -> str:
    """Удаляет namespace из XML тега."""
    pos = tag.rfind('}')
    return tag[pos + 1:] if pos > -1 else tag


def format_date(xml_date: Optional[str]) -> str:
    """Преобразует 'YYYY-MM-DDTHH:MM:SS' в 'DD.MM.YYYY'."""
    if xml_date and 'T' in xml_date:
        parts = xml_date.split('T')[0].split('-')
        if len(parts) == 3:
            return f"{parts[2]}.{parts[1]}.{parts[0]}"
    return xml_date or ""


def get_competency_type(type_code: Optional[str]) -> str:
    """Определяет тип компетенции по коду."""
    type_map = {2: "УК", 3: "ОПК", 4: "ПК"}
    return type_map.get(int(type_code) if type_code else 0, "Не указан")


def build_references(root: ET.Element) -> Dict[str, Dict]:
    """Извлекает все справочные данные за один проход."""

    refs = {
        'forms': {},              # Формы обучения
        'groups': {},             # Группы профстандартов
        'activities': {},         # Виды деятельности
        'work_kinds': {},         # Виды работ
        'obj_types': {},          # Типы объектов
        'obj_kinds': {},          # Виды объектов
        'gen_functions': {},      # Обобщенные функции ПС
        'functions': {}           # Трудовые функции ПС
    }

    for elem in root.iter():
        tag = clean_tag_name(elem.tag)
        attr = elem.attrib

        if tag == "ФормаОбучения":
            refs['forms'][attr.get("Код")] = attr.get("ФормаОбучения")

        elif tag == "псГруппы":
            refs['groups'][attr.get("КодГруппы")] = attr.get("Группа")

        elif tag in ["псВидыДеятельности", "СправочникВидыДеятельности", "ВидыДеятельности"]:
            code = attr.get("Код")
            name = attr.get("Наименование") or attr.get("Название")
            if code and name:
                refs['activities'][code] = name

        elif tag == "СправочникВидыРабот":
            refs['work_kinds'][attr.get("Код")] = attr.get("Название")

        elif tag == "СправочникТипОбъекта":
            refs['obj_types'][attr.get("Код")] = attr.get("Название")

        elif tag == "СправочникВидОбъекта":
            refs['obj_kinds'][attr.get("Код")] = attr.get("Наименование")

        elif tag == "псОбобщенныеФункции":
            code = attr.get("Код")
            refs['gen_functions'][code] = {
                'standard_code': attr.get("КодСтандарта"),
                'index': attr.get("Шифр"),
                'title': attr.get("ОбобщеннаяФункция"),
                'qualification_level': attr.get("УровеньКвалификации")
            }

        elif tag == "псФункции":
            code = attr.get("Код")
            refs['functions'][code] = {
                'gen_func_code': attr.get("КодОбщФункции"),
                'index': attr.get("Шифр"),
                'title': attr.get("Функция")
            }

    return refs


def build_prof_standards(root: ET.Element, refs: Dict) -> Dict[str, Dict]:
    """Извлекает профстандарты с их обобщенными и трудовыми функциями."""

    standards = {}

    for elem in root.iter():
        if clean_tag_name(elem.tag) == "псСтандарты":
            attr = elem.attrib
            std_id = attr.get("Код")
            group_code = attr.get("КодГруппы")

            # Находим обобщенные функции для этого стандарта
            gen_funcs = []
            for gf_id, gf_data in refs['gen_functions'].items():
                if gf_data['standard_code'] == std_id:
                    # Находим трудовые функции для обобщенной функции
                    labor_funcs = [
                        {'index': f_data['index'], 'title': f_data['title']}
                        for f_id, f_data in refs['functions'].items()
                        if f_data['gen_func_code'] == gf_id
                    ]

                    gen_funcs.append({
                        'index': gf_data['index'],
                        'title': gf_data['title'],
                        'qualification_level': gf_data['qualification_level'],
                        'labor_functions': labor_funcs
                    })

            standards[std_id] = {
                'prof_index': attr.get("НомерВГруппе"),
                'prof_group_code': group_code,
                'prof_title': refs['groups'].get(group_code, ""),
                'title': attr.get("НаименованиеСтандарта"),
                'reg_number': attr.get("РегистрационныйНомер"),
                'activity_type': attr.get("НаименованиеВидаПрофДеятельности"),
                'order_number': attr.get('ПриказНомер'),
                'order_date': format_date(attr.get('ПриказДата')),
                'is_active': attr.get("Статус") == "true",
                'generalized_functions': gen_funcs
            }

    return standards


def extract_program_metadata(root: ET.Element, refs: Dict) -> tuple:
    """Извлекает общие данные о программе и профилях."""

    # Данные плана
    plan_data = {}
    for elem in root.iter():
        if clean_tag_name(elem.tag) == "Планы":
            attr = elem.attrib
            plan_data = {
                'start_year': attr.get('ГодНачалаПодготовки'),
                'duration': attr.get('СрокОбучения'),
                'qualification': attr.get('Квалификация'),
                'protocol_number': attr.get('НомПротокСовета'),
                'protocol_date': format_date(attr.get('ДатаУтверСоветом')),
                'form_of_study': refs['forms'].get(attr.get("КодФормыОбучения"))
            }
            break

    # Факультет
    for elem in root.iter():
        if clean_tag_name(elem.tag) == "Факультеты":
            plan_data['faculty'] = elem.attrib.get('Факультет') or elem.attrib.get('Наименование')
            break

    # Направление и профили
    direction = {}
    profiles = []

    for elem in root.iter():
        if clean_tag_name(elem.tag) == "ООП":
            attr = elem.attrib
            if not attr.get('КодРодительскогоООП'):
                direction = {
                    'id': attr.get('Код'),
                    'name': attr.get('Название'),
                    'code': attr.get('Шифр'),
                    'fgos_number': attr.get('НомерДокумента'),
                    'fgos_date': format_date(attr.get('ДатаДокумента'))
                }
            else:
                profiles.append({
                    'id': attr.get('Код'),
                    'name': attr.get('Название')
                })

    # Если профилей нет, создаем фиктивный = направлению
    if not profiles:
        profiles = [{'id': direction['id'], 'name': direction['name']}]

    return plan_data, direction, profiles


def extract_competencies(root: ET.Element, refs: Dict) -> tuple:
    """Извлекает компетенции и индикаторы, сгруппированные по профилям."""

    comp_by_oop = {}  # {oop_id: {'competencies': {}, 'indicators': {}}}
    comp_lookup = {}  # {comp_id: basic_info} для связи с дисциплинами

    for elem in root.iter():
        if clean_tag_name(elem.tag) == 'ПланыКомпетенции':
            attr = elem.attrib

            comp_id = attr.get('Код')
            code = attr.get("ШифрКомпетенции", "")
            name = attr.get("Наименование")
            oop_id = attr.get("КодООП")
            type_code = attr.get("Тип")

            comp_type = get_competency_type(type_code)
            activity = refs['activities'].get(attr.get("КодВидаДеятельности"), "Не указана")

            # Для связи с дисциплинами
            comp_lookup[comp_id] = {
                'code': code,
                'title': name,
                'category': attr.get('Категория')
            }

            # Для структуры программы
            if oop_id not in comp_by_oop:
                comp_by_oop[oop_id] = {'competencies': {}, 'indicators': {}}

            comp_data = {
                'code': code,
                'name': name,
                'type': comp_type,
                'activity': activity
            }

            # Все записи - индикаторы
            comp_by_oop[oop_id]['indicators'][code] = comp_data

            # Только без точки - компетенции
            if "." not in code:
                comp_by_oop[oop_id]['competencies'][code] = comp_data

    return comp_lookup, comp_by_oop


def extract_disciplines(root: ET.Element, refs: Dict, comp_lookup: Dict, direction_id: str) -> Dict:
    """Извлекает дисциплины с часами и формами контроля."""

    # Формы контроля
    control_forms_codes = {'1', '2', '3', '4', '5', '6', '49'}

    # Связи дисциплина -> компетенции
    disc_to_comp = {}
    for elem in root.iter():
        if clean_tag_name(elem.tag) == 'ПланыКомпетенцииДисциплины':
            line_id = elem.attrib.get('КодСтроки')
            comp_id = elem.attrib.get('КодКомпетенции')
            if line_id not in disc_to_comp:
                disc_to_comp[line_id] = []
            if comp_id in comp_lookup:
                disc_to_comp[line_id].append(comp_lookup[comp_id])

    # Часы по семестрам с формами контроля
    hours_data = {}  # {obj_id: {'hours': [], 'control': {}}}
    for elem in root.iter():
        if clean_tag_name(elem.tag) == 'ПланыНовыеЧасы':
            attr = elem.attrib
            obj_id = attr.get('КодОбъекта')
            work_code = attr.get('КодВидаРаботы')
            course = attr.get('Курс')
            semester = attr.get('Семестр')
            hours = attr.get('Количество')

            if obj_id not in hours_data:
                hours_data[obj_id] = {'hours': [], 'control': {}}

            work_name = refs['work_kinds'].get(work_code, f"Код {work_code}")

            # Сохраняем часы
            hours_data[obj_id]['hours'].append({
                'course': course,
                'semester': semester,
                'work_type': work_name,
                'hours': hours
            })

            # Если это форма контроля
            if work_code in control_forms_codes:
                sem_key = f"{course}.{semester}"
                if sem_key not in hours_data[obj_id]['control']:
                    hours_data[obj_id]['control'][sem_key] = []
                hours_data[obj_id]['control'][sem_key].append(work_name)

    # Собираем дисциплины
    disciplines_by_oop = {'common': []}

    for elem in root.iter():
        if clean_tag_name(elem.tag) == "ПланыСтроки":
            attr = elem.attrib
            obj_id = attr.get('Код')
            oop_id = attr.get('КодООП')

            hours_info = hours_data.get(obj_id, {'hours': [], 'control': {}})

            discipline = {
                'id': obj_id,
                'code': attr.get('ДисциплинаКод'),
                'name': attr.get('Дисциплина'),
                'type': refs['obj_types'].get(attr.get('ТипОбъекта')),
                'kind': refs['obj_kinds'].get(attr.get('ВидОбъекта')),
                'credits': attr.get('ЗЕТфакт'),
                'total_hours': attr.get('ЧасовПоПлану'),
                'hours_distribution': hours_info['hours'],
                'control_forms': hours_info['control'],
                'competencies': disc_to_comp.get(obj_id, [])
            }

            # Определяем, куда отнести дисциплину
            is_common = not oop_id or oop_id == '0' or oop_id == direction_id

            if is_common:
                disciplines_by_oop['common'].append(discipline)
            else:
                if oop_id not in disciplines_by_oop:
                    disciplines_by_oop[oop_id] = []
                disciplines_by_oop[oop_id].append(discipline)

    return disciplines_by_oop


def build_final_programs(plan_meta: Dict, direction: Dict, profiles: List,
                         prof_stds: Dict, comps_by_oop: Dict, discs_by_oop: Dict,
                         root: ET.Element) -> List[Dict]:
    """Собирает финальные структуры образовательных программ."""

    programs = []

    for profile in profiles:
        prof_id = profile['id']
        dir_id = direction['id']

        program = {
            # Идентификация
            'program_name': profile['name'],
            'direction': f"{direction['code']} {direction['name']}",
            'faculty': plan_meta.get('faculty'),

            # Реквизиты
            'protocol_number': plan_meta.get('protocol_number'),
            'protocol_date': plan_meta.get('protocol_date'),
            'fgos_number': direction.get('fgos_number'),
            'fgos_date': direction.get('fgos_date'),

            # Параметры
            'start_year': plan_meta.get('start_year'),
            'duration': plan_meta.get('duration'),
            'qualification': plan_meta.get('qualification'),
            'form_of_study': plan_meta.get('form_of_study'),

            # Данные
            'competencies': {},
            'indicators': {},
            'prof_standards': [],
            'disciplines': []
        }

        # Объединяем компетенции (общие + профильные)
        for source_id in [dir_id, prof_id]:
            if source_id in comps_by_oop:
                program['competencies'].update(comps_by_oop[source_id]['competencies'])
                program['indicators'].update(comps_by_oop[source_id]['indicators'])

        # Добавляем профстандарты
        added_stds = set()
        for elem in root.iter():
            if clean_tag_name(elem.tag) == "ПланыПрофСтандарты":
                attr = elem.attrib
                link_oop = attr.get('КодООП')
                if link_oop in [prof_id, dir_id, '0', None]:
                    std_code = attr.get('КодПС')
                    if std_code in prof_stds and std_code not in added_stds:
                        program['prof_standards'].append(prof_stds[std_code])
                        added_stds.add(std_code)

        # Объединяем дисциплины (общие + профильные)
        program['disciplines'] = discs_by_oop.get('common', []) + discs_by_oop.get(prof_id, [])

        programs.append(program)

    return programs


def parse_plx(plx_content: bytes) -> Dict[str, Any]:
    """
    Главная функция: парсит PLX файл и возвращает структуру программы.

    Args:
        plx_content: Содержимое PLX файла в байтах

    Returns:
        Словарь с данными первой программы (или None если ошибка)
    """
    # Парсим XML
    root = ET.parse(BytesIO(plx_content)).getroot()

    # Извлекаем справочники
    references = build_references(root)

    # Извлекаем профстандарты
    prof_standards = build_prof_standards(root, references)

    # Извлекаем метаданные
    plan_metadata, direction_info, profiles_list = extract_program_metadata(root, references)

    # Извлекаем компетенции
    competencies_lookup, competencies_by_oop = extract_competencies(root, references)

    # Извлекаем дисциплины
    disciplines_by_profile = extract_disciplines(
        root, references, competencies_lookup, direction_info.get('id', '')
    )

    # Собираем программы
    final_programs = build_final_programs(
        plan_metadata,
        direction_info,
        profiles_list,
        prof_standards,
        competencies_by_oop,
        disciplines_by_profile,
        root
    )

    # Возвращаем первую программу (обычно одна)
    if final_programs:
        return final_programs[0]

    return None


def parse_plx_all(plx_content: bytes) -> List[Dict[str, Any]]:
    """
    Парсит PLX файл и возвращает все программы (если их несколько профилей).

    Args:
        plx_content: Содержимое PLX файла в байтах

    Returns:
        Список словарей с данными программ
    """
    # Парсим XML
    root = ET.parse(BytesIO(plx_content)).getroot()

    # Извлекаем справочники
    references = build_references(root)

    # Извлекаем профстандарты
    prof_standards = build_prof_standards(root, references)

    # Извлекаем метаданные
    plan_metadata, direction_info, profiles_list = extract_program_metadata(root, references)

    # Извлекаем компетенции
    competencies_lookup, competencies_by_oop = extract_competencies(root, references)

    # Извлекаем дисциплины
    disciplines_by_profile = extract_disciplines(
        root, references, competencies_lookup, direction_info.get('id', '')
    )

    # Собираем программы
    final_programs = build_final_programs(
        plan_metadata,
        direction_info,
        profiles_list,
        prof_standards,
        competencies_by_oop,
        disciplines_by_profile,
        root
    )

    return final_programs
