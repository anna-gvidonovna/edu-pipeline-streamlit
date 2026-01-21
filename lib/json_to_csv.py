"""
JSON to CSV Converter - конвертация данных программы в 6 CSV файлов
Адаптировано из Notebook 2: JSON -> CSV
"""

import pandas as pd
from typing import Dict, Any, List
from collections import defaultdict


def get_competence_type_ru(comp_type: str) -> str:
    """Преобразует код типа компетенции в русское название."""
    type_map = {
        'УК': 'универсальный',
        'ОПК': 'общепрофессиональный',
        'ПК': 'профессиональный'
    }
    return type_map.get(comp_type, '')


def create_title_csv(program_data: Dict[str, Any]) -> pd.DataFrame:
    """Создает DataFrame с информацией о программе."""

    # Берём первый профессиональный стандарт
    prof_std = program_data.get('prof_standards', [{}])[0] if program_data.get('prof_standards') else {}

    # Подсчет общих кредитов
    duration_str = program_data.get('duration', '4')
    try:
        duration_years = int(duration_str)
    except (ValueError, TypeError):
        duration_years = 4
    total_credits = duration_years * 60

    title_row = {
        'edu_protocol_number': program_data.get('protocol_number', ''),
        'edu_protocol_date': program_data.get('protocol_date', ''),
        'qualification': program_data.get('qualification', ''),
        'start_year': program_data.get('start_year', ''),
        'form_of_study': (program_data.get('form_of_study', '') or '').lower(),
        'fgos_number': program_data.get('fgos_number', ''),
        'fgos_date': program_data.get('fgos_date', ''),
        'duration_years': duration_str,
        'direction': program_data.get('direction', ''),
        'program_name': program_data.get('program_name', ''),
        'faculty_name': program_data.get('faculty', ''),
        'program_total': str(total_credits),
        'prof_index': (prof_std.get('prof_group_code', '') or '').strip() + '.0' if prof_std.get('prof_group_code') else '',
        'prof_title': prof_std.get('prof_title', ''),
        'prof_func_index': prof_std.get('prof_index', ''),
        'prof_func_title': prof_std.get('title', '')
    }

    return pd.DataFrame([title_row])


def create_competences_csv(program_data: Dict[str, Any]) -> pd.DataFrame:
    """Создает DataFrame с компетенциями."""

    competences_list = []

    for comp_code, comp_data in program_data.get('competencies', {}).items():
        comp_type = comp_data.get('type', '')
        comp_type_ru = get_competence_type_ru(comp_type)

        activity = comp_data.get('activity', '')
        task_type = activity if activity != 'Не указана' else ''

        competences_list.append({
            'competence_code': comp_data.get('code', ''),
            'competence': comp_data.get('name', ''),
            'competence_type': comp_type_ru,
            'task_type': task_type
        })

    # Сортируем по коду компетенции
    def sort_key(item):
        code = item['competence_code']
        if '-' in code:
            parts = code.split('-')
            try:
                return (parts[0], int(parts[1]))
            except (ValueError, IndexError):
                return (code, 0)
        return (code, 0)

    competences_list.sort(key=sort_key)

    return pd.DataFrame(competences_list)


def create_indicators_csv(program_data: Dict[str, Any]) -> pd.DataFrame:
    """Создает DataFrame с индикаторами компетенций."""

    indicators_dict = {}

    for disc in program_data.get('disciplines', []):
        for comp in disc.get('competencies', []):
            indicator_code = comp.get('code', '')
            indicator_name = comp.get('title', '')

            # Определяем код компетенции
            if '.' in indicator_code:
                competence_code = indicator_code.split('.')[0]
            else:
                competence_code = indicator_code

            # Получаем информацию о компетенции
            comp_info = program_data.get('competencies', {}).get(competence_code, {})
            comp_type = comp_info.get('type', '')
            comp_type_ru = get_competence_type_ru(comp_type)

            activity = comp_info.get('activity', '')
            task_type = activity if activity != 'Не указана' else ''

            if indicator_code not in indicators_dict:
                indicators_dict[indicator_code] = {
                    'competence_code': indicator_code,
                    'indicator': indicator_name,
                    'competence_type': comp_type_ru,
                    'task_type': task_type
                }

    indicators_list = list(indicators_dict.values())

    # Сортируем по коду индикатора
    def sort_key(item):
        code = item['competence_code']
        if '.' in code:
            parts = code.split('.')
            comp_part = parts[0]
            ind_part = parts[1]
            if '-' in comp_part:
                comp_type, comp_num = comp_part.split('-')
                try:
                    return (comp_type, int(comp_num), int(ind_part))
                except ValueError:
                    return (code, 0, 0)
        return (code, 0, 0)

    indicators_list.sort(key=sort_key)

    return pd.DataFrame(indicators_list)


def create_matching_csv(program_data: Dict[str, Any]) -> pd.DataFrame:
    """Создает DataFrame с соответствием дисциплин и компетенций."""

    matching_list = []

    for disc in program_data.get('disciplines', []):
        disc_code = disc.get('code', '')
        disc_name = disc.get('name', '')

        for comp in disc.get('competencies', []):
            indicator_code = comp.get('code', '')
            indicator_name = comp.get('title', '')

            # Определяем код компетенции
            if '.' in indicator_code:
                competence_code = indicator_code.split('.')[0]
            else:
                competence_code = indicator_code

            # Получаем информацию о компетенции
            comp_info = program_data.get('competencies', {}).get(competence_code, {})
            competence_name = comp_info.get('name', '')
            comp_type = comp_info.get('type', '')
            comp_type_ru = get_competence_type_ru(comp_type)

            activity = comp_info.get('activity', '')
            task_type = activity if activity != 'Не указана' else ''

            unique_id = f"{disc_code}_{competence_code}"

            matching_list.append({
                'discipline_code': disc_code,
                'discipline': disc_name,
                'competence_code': competence_code,
                'competence': competence_name,
                'indicator_code': indicator_code,
                'indicator': indicator_name,
                'competence_type': comp_type_ru,
                'task_type': task_type,
                'ID': unique_id
            })

    return pd.DataFrame(matching_list)


def create_long_csv(program_data: Dict[str, Any]) -> pd.DataFrame:
    """Создает DataFrame с дисциплинами в длинном формате."""

    long_list = []

    for disc in program_data.get('disciplines', []):
        disc_code = disc.get('code', '')
        disc_name = disc.get('name', '')
        disc_type = disc.get('type', '')

        # Пропускаем "Блоки по выбору"
        if disc_type == 'Блоки по выбору':
            continue

        # Формируем строку компетенций
        competences_str = '; '.join([comp.get('code', '') for comp in disc.get('competencies', [])])

        # Определяем no_skip
        if '.ДВ.' in disc_code and disc_code.count('.') == 2:
            no_skip = 0
        elif '.ДВ.' in disc_code and disc_code.count('.') == 3:
            variant_num = disc_code.split('.')[-1]
            no_skip = 1 if variant_num == '01' else 0
        else:
            no_skip = 1

        # Определяем тип практики
        if '(У)' in disc_code:
            praxis = 'У'
        elif '(П)' in disc_code:
            praxis = 'П'
        else:
            praxis = '0'

        # Группируем данные по семестрам
        semesters_data = defaultdict(lambda: {
            'credits': '',
            'lectures': '',
            'labs': '',
            'practice': '',
            'solo': '',
            'control': '',
            'exam': 0,
            'pass': 0,
            'graded_pass': 0
        })

        hours_dist = disc.get('hours_distribution', [])
        for item in hours_dist:
            course = item.get('course', '')
            semester_in_year = item.get('semester', '')
            work_type = item.get('work_type', '')
            hours = item.get('hours', '')

            if not course or not semester_in_year:
                continue

            try:
                absolute_semester = (int(course) - 1) * 2 + int(semester_in_year)
            except ValueError:
                continue

            if work_type == 'ЗЕТ':
                semesters_data[absolute_semester]['credits'] = hours
            elif work_type == 'Лекционные занятия':
                semesters_data[absolute_semester]['lectures'] = hours
            elif work_type == 'Лабораторные занятия':
                semesters_data[absolute_semester]['labs'] = hours
            elif work_type == 'Практические занятия':
                semesters_data[absolute_semester]['practice'] = hours
            elif work_type == 'Самостоятельная работа':
                semesters_data[absolute_semester]['solo'] = hours
            elif work_type == 'Контроль':
                semesters_data[absolute_semester]['control'] = hours
            elif work_type == 'Экзамен':
                semesters_data[absolute_semester]['exam'] = 1
            elif work_type == 'Зачет':
                semesters_data[absolute_semester]['pass'] = 1
            elif work_type == 'Зачет с оценкой':
                semesters_data[absolute_semester]['graded_pass'] = 1

        for semester, sem_data in sorted(semesters_data.items()):
            grade_year = (semester + 1) // 2

            long_list.append({
                'discipline_code': disc_code,
                'discipline': disc_name,
                'exam': sem_data['exam'],
                'pass': sem_data['pass'],
                'graded_pass': sem_data['graded_pass'],
                'credits': sem_data['credits'],
                'lectures': sem_data['lectures'],
                'labs': sem_data['labs'],
                'practice': sem_data['practice'],
                'solo': sem_data['solo'],
                'control': sem_data['control'],
                'competences': competences_str,
                'semester': semester,
                'grade_year': grade_year,
                'no_skip': no_skip,
                'praxis': praxis
            })

    # Сортируем по семестру и коду дисциплины
    long_list.sort(key=lambda x: (x['semester'], x['discipline_code']))

    return pd.DataFrame(long_list)


def create_wide_csv(program_data: Dict[str, Any]) -> pd.DataFrame:
    """Создает DataFrame с дисциплинами в широком формате."""

    # Определяем количество семестров
    duration_str = program_data.get('duration', '4')
    try:
        program_duration = int(duration_str)
    except (ValueError, TypeError):
        program_duration = 4
    max_semester = program_duration * 2

    # Собираем данные по дисциплинам и семестрам
    disciplines_by_code = defaultdict(lambda: defaultdict(dict))

    for disc in program_data.get('disciplines', []):
        disc_code = disc.get('code', '')
        disc_name = disc.get('name', '')
        disc_type = disc.get('type', '')

        if disc_type == 'Блоки по выбору':
            continue

        competences_str = '; '.join([comp.get('code', '') for comp in disc.get('competencies', [])])

        # Определяем no_skip
        if '.ДВ.' in disc_code and disc_code.count('.') == 2:
            no_skip = 0
        elif '.ДВ.' in disc_code and disc_code.count('.') == 3:
            variant_num = disc_code.split('.')[-1]
            no_skip = 1 if variant_num == '01' else 0
        else:
            no_skip = 1

        # Определяем тип практики
        if '(У)' in disc_code:
            praxis = 'У'
        elif '(П)' in disc_code:
            praxis = 'П'
        else:
            praxis = ''

        if 'discipline' not in disciplines_by_code[disc_code]:
            disciplines_by_code[disc_code]['discipline'] = disc_name

        # Группируем данные по семестрам
        semesters_data = defaultdict(lambda: {
            'credits': '',
            'lectures': '',
            'labs': '',
            'practice': '',
            'solo': '',
            'control': '',
            'exam': 0,
            'pass': 0,
            'graded_pass': 0
        })

        hours_dist = disc.get('hours_distribution', [])
        for item in hours_dist:
            course = item.get('course', '')
            semester_in_year = item.get('semester', '')
            work_type = item.get('work_type', '')
            hours = item.get('hours', '')

            if not course or not semester_in_year:
                continue

            try:
                absolute_semester = (int(course) - 1) * 2 + int(semester_in_year)
            except ValueError:
                continue

            if work_type == 'ЗЕТ':
                semesters_data[absolute_semester]['credits'] = hours
            elif work_type == 'Лекционные занятия':
                semesters_data[absolute_semester]['lectures'] = hours
            elif work_type == 'Лабораторные занятия':
                semesters_data[absolute_semester]['labs'] = hours
            elif work_type == 'Практические занятия':
                semesters_data[absolute_semester]['practice'] = hours
            elif work_type == 'Самостоятельная работа':
                semesters_data[absolute_semester]['solo'] = hours
            elif work_type == 'Контроль':
                semesters_data[absolute_semester]['control'] = hours
            elif work_type == 'Экзамен':
                semesters_data[absolute_semester]['exam'] = 1
            elif work_type == 'Зачет':
                semesters_data[absolute_semester]['pass'] = 1
            elif work_type == 'Зачет с оценкой':
                semesters_data[absolute_semester]['graded_pass'] = 1

        for semester, sem_data in semesters_data.items():
            grade_year = (semester + 1) // 2

            disciplines_by_code[disc_code][semester] = {
                'discipline': disc_name,
                'exam': sem_data['exam'],
                'pass': sem_data['pass'],
                'graded_pass': sem_data['graded_pass'],
                'credits': sem_data['credits'],
                'lectures': sem_data['lectures'],
                'labs': sem_data['labs'],
                'practice': sem_data['practice'],
                'solo': sem_data['solo'],
                'control': sem_data['control'],
                'competences': competences_str,
                'grade_year': str(grade_year) + '.0',
                'no_skip': str(no_skip) + '.0' if no_skip == 0 else str(no_skip),
                'praxis': praxis
            }

    # Создаем wide формат
    wide_list = []
    for disc_code in sorted(disciplines_by_code.keys()):
        disc_data = disciplines_by_code[disc_code]

        row = {
            'discipline_code': disc_code,
            'discipline': disc_data['discipline']
        }

        for sem in range(1, max_semester + 1):
            if sem in disc_data and isinstance(disc_data[sem], dict):
                row[f'discipline_sem{sem}'] = disc_data[sem]['discipline']
                row[f'exam_sem{sem}'] = disc_data[sem]['exam']
                row[f'pass_sem{sem}'] = disc_data[sem]['pass']
                row[f'graded_pass_sem{sem}'] = disc_data[sem]['graded_pass']
                row[f'credits_sem{sem}'] = disc_data[sem]['credits']
                row[f'lectures_sem{sem}'] = disc_data[sem]['lectures']
                row[f'labs_sem{sem}'] = disc_data[sem]['labs']
                row[f'practice_sem{sem}'] = disc_data[sem]['practice']
                row[f'solo_sem{sem}'] = disc_data[sem]['solo']
                row[f'control_sem{sem}'] = disc_data[sem]['control']
                row[f'competences_sem{sem}'] = disc_data[sem]['competences']
                row[f'grade_year_sem{sem}'] = disc_data[sem]['grade_year']
                row[f'no_skip_sem{sem}'] = disc_data[sem]['no_skip']
                row[f'praxis_sem{sem}'] = disc_data[sem]['praxis']
            else:
                row[f'discipline_sem{sem}'] = ''
                row[f'exam_sem{sem}'] = 0
                row[f'pass_sem{sem}'] = 0
                row[f'graded_pass_sem{sem}'] = 0
                row[f'credits_sem{sem}'] = ''
                row[f'lectures_sem{sem}'] = ''
                row[f'labs_sem{sem}'] = ''
                row[f'practice_sem{sem}'] = ''
                row[f'solo_sem{sem}'] = ''
                row[f'control_sem{sem}'] = ''
                row[f'competences_sem{sem}'] = ''
                row[f'grade_year_sem{sem}'] = ''
                row[f'no_skip_sem{sem}'] = ''
                row[f'praxis_sem{sem}'] = ''

        wide_list.append(row)

    # Формируем порядок колонок
    columns = ['discipline_code', 'discipline']
    field_types = ['discipline_sem', 'exam_sem', 'pass_sem', 'graded_pass_sem',
                   'credits_sem', 'lectures_sem', 'labs_sem', 'practice_sem',
                   'solo_sem', 'control_sem', 'competences_sem', 'grade_year_sem',
                   'no_skip_sem', 'praxis_sem']

    for field_type in field_types:
        for sem in range(1, max_semester + 1):
            columns.append(f'{field_type}{sem}')

    df = pd.DataFrame(wide_list)

    # Переупорядочиваем колонки
    existing_columns = [col for col in columns if col in df.columns]
    return df[existing_columns]


def convert_to_csvs(program_data: Dict[str, Any]) -> Dict[str, pd.DataFrame]:
    """
    Главная функция: конвертирует данные программы в 6 CSV файлов.

    Args:
        program_data: Словарь с данными программы (из parse_plx)

    Returns:
        Словарь с 6 DataFrame: title, competences, indicators, matching, long, wide
    """
    return {
        'title': create_title_csv(program_data),
        'competences': create_competences_csv(program_data),
        'indicators': create_indicators_csv(program_data),
        'matching': create_matching_csv(program_data),
        'long': create_long_csv(program_data),
        'wide': create_wide_csv(program_data)
    }
