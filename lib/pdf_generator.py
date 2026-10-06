"""
PDF Generator - генерация PDF через Typst
Адаптировано из Notebook 4: CSV -> PDF Export

ВАЖНО: Требует установленный Typst и библиотеку typst для Python
pip install typst
"""

import os
import shutil
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Callable
import pandas as pd


def check_typst_available() -> Tuple[bool, str]:
    """
    Проверяет, доступен ли Typst.

    Returns:
        (is_available, message)
    """
    try:
        import typst
        return True, "Typst доступен"
    except ImportError:
        return False, "Библиотека typst не установлена. Установите: pip install typst"


def compile_typst(typ_file: Path, output_pdf: Path, working_dir: Optional[Path] = None, font_paths: Optional[List[Path]] = None) -> Tuple[bool, str]:
    """
    Компилирует .typ файл в PDF через typst-py.
    Работает на сервере без системного бинарника Typst.

    Args:
        typ_file: Путь к .typ файлу
        output_pdf: Путь для сохранения PDF
        working_dir: Рабочая директория (по умолчанию - директория typ_file)
        font_paths: Список путей к директориям со шрифтами

    Returns:
        (success, message)
    """
    try:
        import typst

        original_cwd = os.getcwd()
        work_dir = working_dir or typ_file.parent
        os.chdir(work_dir)

        try:
            # typst.compile() принимает путь к файлу и опционально output
            # Если output не указан, возвращает bytes
            # Если output указан, записывает в файл
            compile_kwargs = {
                "output": str(output_pdf),
            }

            if font_paths:
                compile_kwargs["font_paths"] = [str(p) for p in font_paths]

            typst.compile(str(typ_file), **compile_kwargs)

            if output_pdf.exists():
                return True, f"Создан: {output_pdf.name}"
            else:
                return False, f"PDF не создан: {output_pdf.name}"
        finally:
            os.chdir(original_cwd)

    except Exception as e:
        return False, f"Ошибка: {str(e)}"


def prepare_csv_files(csvs: Dict[str, pd.DataFrame], merged: Dict[str, pd.DataFrame],
                      csv_dir: Path) -> None:
    """
    Сохраняет CSV файлы в директорию для Typst.

    Args:
        csvs: Базовые CSV (title, competences, indicators, matching, long, wide)
        merged: Объединённые CSV (indicators_merge, wide_merge, assessment)
        csv_dir: Директория для сохранения
    """
    csv_dir.mkdir(parents=True, exist_ok=True)

    # Базовые CSV
    for name, df in csvs.items():
        df.to_csv(csv_dir / f"{name}.csv", index=False, encoding='utf-8')

    # Объединённые CSV
    for name, df in merged.items():
        df.to_csv(csv_dir / f"{name}.csv", index=False, encoding='utf-8')


def _to_typst_bool(value: bool) -> str:
    """Преобразует Python bool в литерал Typst."""
    return "true" if value else "false"


# Подписи типов документов в именах файлов: {prefix: (en, ru)}
DOC_LABELS = {
    "1": ("Program", "ОПОП"),
    "2": ("Plan", "Учебный план"),
    "3": ("Calendar", "КУГ"),
    "4": ("Module", "РПД"),
    "5": ("Practice", "РПП"),
    "6": ("Finals", "ГИА"),
    "7": ("Assessment", "ФОС"),
    "8a": ("Upbringing", "РПВ"),
    "8b": ("Cal_upbringing", "КПВР"),
}

_FORBIDDEN_FILENAME_CHARS = '<>:"/\\|?*\n\r\t'


def _safe_filename(text: str, max_len: int = 120) -> str:
    """Убирает недопустимые для имени файла символы и обрезает длину."""
    cleaned = "".join("_" if c in _FORBIDDEN_FILENAME_CHARS else c for c in str(text))
    cleaned = " ".join(cleaned.split()).strip(" .")
    return cleaned[:max_len].rstrip(" .")


def _doc_filename(prefix: str, lang: str, item: Optional[str] = None, with_number: bool = True) -> str:
    """
    Формирует имя PDF: "[<prefix>. ]<Тип>[ <item>].pdf".

    Args:
        prefix: Номер документа ("1", "4", "8a", ...)
        lang: "en" или "ru" — язык подписи типа документа
        item: Индекс или название дисциплины (для РПД/РПП/ФОС)
        with_number: Добавлять ли номер документа в начало имени
    """
    en, ru = DOC_LABELS[prefix]
    label = ru if lang == "ru" else en
    name = f"{prefix}. {label}" if with_number else label
    if item:
        name += f" {item}"
    return f"{name}.pdf"


def _compile_wrapper_typst(
    templates_dir: Path,
    output_pdf: Path,
    import_path: str,
    show_name: str,
    with_args: List[str],
    temp_name: str,
    font_paths: Optional[List[Path]] = None,
) -> Tuple[bool, str]:
    """
    Создаёт временный Typst-обёрточный файл, компилирует его и удаляет.

    Args:
        templates_dir: Корневая директория шаблонов
        output_pdf: Путь выходного PDF
        import_path: Путь импорта шаблона внутри Typst
        show_name: Имя функции шаблона для `#show: ...with(...)`
        with_args: Аргументы внутри `with(...)` (по одному на строку)
        temp_name: Имя временного файла .typ
        font_paths: Список директорий со шрифтами
    """
    template_path = templates_dir / import_path
    if not template_path.exists():
        return False, f"Шаблон не найден: {import_path}"

    temp_typ = templates_dir / temp_name
    args_block = ",\n".join(f"  {arg}" for arg in with_args)
    content = (
        f'#import "{import_path}": *\n'
        f"#show: {show_name}.with(\n"
        f"{args_block}\n"
        f")\n"
    )

    temp_typ.write_text(content, encoding="utf-8")
    try:
        return compile_typst(temp_typ, output_pdf, templates_dir, font_paths=font_paths)
    finally:
        temp_typ.unlink(missing_ok=True)


def generate_all_pdfs(
    csvs: Dict[str, pd.DataFrame],
    merged: Dict[str, pd.DataFrame],
    templates_dir: Path,
    output_dir: Path,
    progress_callback: Optional[Callable[[int, int, str], None]] = None,
    is_accredited: bool = False,
    is_new_edition: bool = False,
    doc_year: int = 2026,
    name_by: str = "code",
    filename_lang: str = "en",
    with_number: bool = True,
) -> Tuple[List[Path], List[str]]:
    """
    Генерирует все PDF документы.

    Args:
        csvs: Базовые CSV DataFrames
        merged: Объединённые CSV DataFrames
        templates_dir: Директория с Typst шаблонами (UU EduDocs)
        output_dir: Директория для PDF
        progress_callback: Функция для отчёта о прогрессе (current, total, message)
        is_accredited: Аккредитована ли программа (влияет на Finals)
        is_new_edition: Добавлять ли "(новая редакция)" в шапках документов
        name_by: Как называть РПД/РПП/ФОС: "code" (по индексу) или "name" (по названию дисциплины)
        filename_lang: Язык подписей типов документов в именах файлов: "en" или "ru"
        with_number: Добавлять ли номер документа ("1. ", "4. ", ...) в начало имени файла

    Returns:
        (list_of_created_pdfs, list_of_errors)
    """
    available, msg = check_typst_available()
    if not available:
        return [], [msg]

    created_pdfs = []
    errors = []

    # Создаём директории
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_dir = templates_dir / "csv"

    # Путь к шрифтам
    fonts_dir = templates_dir / "fonts"
    font_paths = [fonts_dir] if fonts_dir.exists() else []

    # Сохраняем CSV файлы
    prepare_csv_files(csvs, merged, csv_dir)

    # Загружаем wide для определения дисциплин
    wide_df = merged.get('wide_merge', csvs.get('wide', pd.DataFrame()))

    if wide_df.empty:
        return [], ["Нет данных о дисциплинах (wide.csv пустой)"]

    # Разделяем на дисциплины, практики, ГИА
    disciplines = wide_df[
        wide_df['discipline_code'].str.startswith('Б1') |
        wide_df['discipline_code'].str.startswith('ФТД')
    ].reset_index()

    practices = wide_df[wide_df['discipline_code'].str.startswith('Б2')].reset_index()
    finals = wide_df[wide_df['discipline_code'].str.startswith('Б3')].reset_index()

    # Подсчёт общего количества PDF
    total_pdfs = (
        3 +  # Program, Plan, Calendar
        len(disciplines) +  # Module
        len(practices) +  # Practice
        (1 if len(finals) > 0 else 0) +  # Finals
        len(disciplines) + len(practices) +  # Assessment
        2  # Upbringing
    )

    current = 0

    def report_progress(message: str):
        nonlocal current
        current += 1
        if progress_callback:
            progress_callback(current, total_pdfs, message)

    typst_is_accredited = _to_typst_bool(is_accredited)
    typst_is_new_edition = _to_typst_bool(is_new_edition)
    typst_doc_year = str(doc_year)

    used_names: set = set()

    def doc_filename(prefix: str, lang: str, item: Optional[str] = None) -> str:
        return _doc_filename(prefix, lang, item, with_number=with_number)

    def item_filename(prefix: str, row) -> str:
        """Имя файла для дисциплины/практики с учётом name_by и без коллизий."""
        code = str(row['discipline_code'])
        raw_title = row.get('discipline', '')
        title = _safe_filename(raw_title) if name_by == "name" and pd.notna(raw_title) else ""
        filename = doc_filename(prefix, filename_lang, title or _safe_filename(code))
        if filename in used_names:
            filename = doc_filename(prefix, filename_lang, f"{title} ({_safe_filename(code)})")
        used_names.add(filename)
        return filename

    # 1. Program.pdf
    output_pdf = output_dir / doc_filename("1", filename_lang)
    success, msg = _compile_wrapper_typst(
        templates_dir=templates_dir,
        output_pdf=output_pdf,
        import_path="templates/1. program.typ",
        show_name="program",
        with_args=[
            "var01: []",
            f"is_new_edition: {typst_is_new_edition}",
            f"doc_year: {typst_doc_year}",
        ],
        temp_name="temp_program.typ",
        font_paths=font_paths,
    )
    if success:
        created_pdfs.append(output_pdf)
    else:
        errors.append(f"1. Program: {msg}")
    report_progress(output_pdf.name)

    # 2. Plan.pdf
    output_pdf = output_dir / doc_filename("2", filename_lang)
    success, msg = _compile_wrapper_typst(
        templates_dir=templates_dir,
        output_pdf=output_pdf,
        import_path="templates/2. plan.typ",
        show_name="plan",
        with_args=[
            "var01: []",
            f"is_new_edition: {typst_is_new_edition}",
            f"doc_year: {typst_doc_year}",
        ],
        temp_name="temp_plan.typ",
        font_paths=font_paths,
    )
    if success:
        created_pdfs.append(output_pdf)
    else:
        errors.append(f"2. Plan: {msg}")
    report_progress(output_pdf.name)

    # 3. Calendar.pdf
    output_pdf = output_dir / doc_filename("3", filename_lang)
    success, msg = _compile_wrapper_typst(
        templates_dir=templates_dir,
        output_pdf=output_pdf,
        import_path="templates/3. calendar.typ",
        show_name="calendar",
        with_args=[
            "var01: []",
            f"is_new_edition: {typst_is_new_edition}",
            f"doc_year: {typst_doc_year}",
        ],
        temp_name="temp_calendar.typ",
        font_paths=font_paths,
    )
    if success:
        created_pdfs.append(output_pdf)
    else:
        errors.append(f"3. Calendar: {msg}")
    report_progress(output_pdf.name)

    # 4. Module.pdf - для каждой дисциплины
    for idx, row in disciplines.iterrows():
        code = row['discipline_code']
        var_cycle = row['index']

        output_pdf = output_dir / item_filename("4", row)
        success, msg = _compile_wrapper_typst(
            templates_dir=templates_dir,
            output_pdf=output_pdf,
            import_path="templates/4. module.typ",
            show_name="module",
            with_args=[
                "var01: []",
                f"var_cycle : {var_cycle}",
                f"is_new_edition: {typst_is_new_edition}",
                f"doc_year: {typst_doc_year}",
            ],
            temp_name=f"temp_module_{var_cycle}.typ",
            font_paths=font_paths,
        )

        if success:
            created_pdfs.append(output_pdf)
        else:
            errors.append(f"4. {code}: {msg}")

        report_progress(output_pdf.name)

    # 5. Practice.pdf - для каждой практики
    for idx, row in practices.iterrows():
        code = row['discipline_code']
        var_cycle = row['index']

        output_pdf = output_dir / item_filename("5", row)
        success, msg = _compile_wrapper_typst(
            templates_dir=templates_dir,
            output_pdf=output_pdf,
            import_path="templates/5. practice.typ",
            show_name="practice",
            with_args=[
                "var01: []",
                f"var_cycle : {var_cycle}",
                f"is_new_edition: {typst_is_new_edition}",
                f"doc_year: {typst_doc_year}",
            ],
            temp_name=f"temp_practice_{var_cycle}.typ",
            font_paths=font_paths,
        )

        if success:
            created_pdfs.append(output_pdf)
        else:
            errors.append(f"5. {code}: {msg}")

        report_progress(output_pdf.name)

    # 6. Finals.pdf
    if len(finals) > 0:
        var_cycle = finals.iloc[0]['index']

        output_pdf = output_dir / doc_filename("6", filename_lang)
        success, msg = _compile_wrapper_typst(
            templates_dir=templates_dir,
            output_pdf=output_pdf,
            import_path="templates/6. finals.typ",
            show_name="finals",
            with_args=[
                "var01: []",
                f"var_cycle : {var_cycle}",
                f"is_accredited: {typst_is_accredited}",
                f"is_new_edition: {typst_is_new_edition}",
                f"doc_year: {typst_doc_year}",
            ],
            temp_name=f"temp_finals_{var_cycle}.typ",
            font_paths=font_paths,
        )

        if success:
            created_pdfs.append(output_pdf)
        else:
            errors.append(f"6. Finals: {msg}")

        report_progress(output_pdf.name)

    # 7. Assessment.pdf - для дисциплин и практик
    assessment_items = pd.concat([disciplines, practices], ignore_index=True)

    for idx, row in assessment_items.iterrows():
        code = row['discipline_code']
        var_cycle = row['index']

        output_pdf = output_dir / item_filename("7", row)
        success, msg = _compile_wrapper_typst(
            templates_dir=templates_dir,
            output_pdf=output_pdf,
            import_path="templates/7. assessment.typ",
            show_name="assessment",
            with_args=[
                "var01: []",
                f"var_cycle : {var_cycle}",
                f"is_new_edition: {typst_is_new_edition}",
                f"doc_year: {typst_doc_year}",
            ],
            temp_name=f"temp_assessment_{var_cycle}.typ",
            font_paths=font_paths,
        )

        if success:
            created_pdfs.append(output_pdf)
        else:
            errors.append(f"7. {code}: {msg}")

        report_progress(output_pdf.name)

    # 8a. Upbringing.pdf
    output_pdf = output_dir / doc_filename("8a", filename_lang)
    success, msg = _compile_wrapper_typst(
        templates_dir=templates_dir,
        output_pdf=output_pdf,
        import_path="templates/8a. upbringing.typ",
        show_name="upbringing",
        with_args=[
            "var01: []",
            f"is_new_edition: {typst_is_new_edition}",
            f"doc_year: {typst_doc_year}",
        ],
        temp_name="temp_upbringing.typ",
        font_paths=font_paths,
    )
    if success:
        created_pdfs.append(output_pdf)
    else:
        errors.append(f"8a. Upbringing: {msg}")
    report_progress(output_pdf.name)

    # 8b. Cal_upbringing.pdf
    output_pdf = output_dir / doc_filename("8b", filename_lang)
    success, msg = _compile_wrapper_typst(
        templates_dir=templates_dir,
        output_pdf=output_pdf,
        import_path="templates/8b. cal_upbringing.typ",
        show_name="cal_upbringing",
        with_args=[
            "var01: []",
            f"is_new_edition: {typst_is_new_edition}",
            f"doc_year: {typst_doc_year}",
        ],
        temp_name="temp_cal_upbringing.typ",
        font_paths=font_paths,
    )
    if success:
        created_pdfs.append(output_pdf)
    else:
        errors.append(f"8b. Cal_upbringing: {msg}")
    report_progress(output_pdf.name)

    return created_pdfs, errors


def _detect_doc_prefix(filename: str) -> str:
    """Определяет номер документа по имени файла (с номером или без него)."""
    stem = filename[:-4] if filename.endswith(".pdf") else filename
    number, sep, rest = stem.partition(". ")
    if sep and number in DOC_LABELS:
        return number
    for prefix, labels in DOC_LABELS.items():
        for label in labels:
            if stem == label or stem.startswith(label + " "):
                return prefix
    return stem


def get_pdf_statistics(pdf_list: List[Path]) -> Dict[str, int]:
    """
    Возвращает статистику по типам PDF.

    Args:
        pdf_list: Список путей к PDF файлам

    Returns:
        Словарь {тип: количество}
    """
    type_names = {
        "1": "Program (ООП)",
        "2": "Plan (Учебный план)",
        "3": "Calendar (КУГ)",
        "4": "Module (Программы дисциплин)",
        "5": "Practice (Программы практик)",
        "6": "Finals (ГИА)",
        "7": "Assessment (ФОСы)",
        "8a": "Upbringing (РПВ)",
        "8b": "Cal_upbringing (Кал. план РПВ)"
    }

    stats = {}
    for pdf in pdf_list:
        prefix = _detect_doc_prefix(pdf.name)
        name = type_names.get(prefix, prefix)
        stats[name] = stats.get(name, 0) + 1

    return stats
