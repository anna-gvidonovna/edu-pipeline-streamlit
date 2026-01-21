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


def compile_typst(typ_file: Path, output_pdf: Path, working_dir: Optional[Path] = None) -> Tuple[bool, str]:
    """
    Компилирует .typ файл в PDF через typst-py.
    Работает на сервере без системного бинарника Typst.

    Args:
        typ_file: Путь к .typ файлу
        output_pdf: Путь для сохранения PDF
        working_dir: Рабочая директория (по умолчанию - директория typ_file)

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
            typst.compile(str(typ_file), output=str(output_pdf))

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


def generate_all_pdfs(
    csvs: Dict[str, pd.DataFrame],
    merged: Dict[str, pd.DataFrame],
    templates_dir: Path,
    output_dir: Path,
    progress_callback: Optional[Callable[[int, int, str], None]] = None
) -> Tuple[List[Path], List[str]]:
    """
    Генерирует все PDF документы.

    Args:
        csvs: Базовые CSV DataFrames
        merged: Объединённые CSV DataFrames
        templates_dir: Директория с Typst шаблонами (UU EduDocs)
        output_dir: Директория для PDF
        progress_callback: Функция для отчёта о прогрессе (current, total, message)

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

    # 1. Program.pdf
    typ_file = templates_dir / "1. Program.typ"
    output_pdf = output_dir / "1. Program.pdf"
    if typ_file.exists():
        success, msg = compile_typst(typ_file, output_pdf)
        if success:
            created_pdfs.append(output_pdf)
        else:
            errors.append(f"1. Program: {msg}")
    report_progress("1. Program.pdf")

    # 2. Plan.pdf
    typ_file = templates_dir / "2. Plan.typ"
    output_pdf = output_dir / "2. Plan.pdf"
    if typ_file.exists():
        success, msg = compile_typst(typ_file, output_pdf)
        if success:
            created_pdfs.append(output_pdf)
        else:
            errors.append(f"2. Plan: {msg}")
    report_progress("2. Plan.pdf")

    # 3. Calendar.pdf
    typ_file = templates_dir / "3. Calendar.typ"
    output_pdf = output_dir / "3. Calendar.pdf"
    if typ_file.exists():
        success, msg = compile_typst(typ_file, output_pdf)
        if success:
            created_pdfs.append(output_pdf)
        else:
            errors.append(f"3. Calendar: {msg}")
    report_progress("3. Calendar.pdf")

    # 4. Module.pdf - для каждой дисциплины
    for idx, row in disciplines.iterrows():
        code = row['discipline_code']
        var_cycle = row['index']

        # Создаём временный .typ файл
        temp_typ = templates_dir / f"temp_module_{var_cycle}.typ"
        content = f'''#import "templates/4. module.typ": *
#show: module.with(
  var01: [],
  var_cycle : {var_cycle}
)
'''
        temp_typ.write_text(content, encoding='utf-8')

        output_pdf = output_dir / f"4. {code}.pdf"
        success, msg = compile_typst(temp_typ, output_pdf, templates_dir)

        if success:
            created_pdfs.append(output_pdf)
        else:
            errors.append(f"4. {code}: {msg}")

        temp_typ.unlink(missing_ok=True)
        report_progress(f"4. {code}.pdf")

    # 5. Practice.pdf - для каждой практики
    for idx, row in practices.iterrows():
        code = row['discipline_code']
        var_cycle = row['index']

        temp_typ = templates_dir / f"temp_practice_{var_cycle}.typ"
        content = f'''#import "templates/5. practice.typ": *
#show: practice.with(
  var01: [],
  var_cycle : {var_cycle}
)
'''
        temp_typ.write_text(content, encoding='utf-8')

        output_pdf = output_dir / f"5. {code}.pdf"
        success, msg = compile_typst(temp_typ, output_pdf, templates_dir)

        if success:
            created_pdfs.append(output_pdf)
        else:
            errors.append(f"5. {code}: {msg}")

        temp_typ.unlink(missing_ok=True)
        report_progress(f"5. {code}.pdf")

    # 6. Finals.pdf
    if len(finals) > 0:
        var_cycle = finals.iloc[0]['index']

        temp_typ = templates_dir / f"temp_finals_{var_cycle}.typ"
        content = f'''#import "templates/6. finals.typ": *
#show: finals.with(
  var01: [],
  var_cycle : {var_cycle}
)
'''
        temp_typ.write_text(content, encoding='utf-8')

        output_pdf = output_dir / "6. Finals.pdf"
        success, msg = compile_typst(temp_typ, output_pdf, templates_dir)

        if success:
            created_pdfs.append(output_pdf)
        else:
            errors.append(f"6. Finals: {msg}")

        temp_typ.unlink(missing_ok=True)
        report_progress("6. Finals.pdf")

    # 7. Assessment.pdf - для дисциплин и практик
    assessment_items = pd.concat([disciplines, practices], ignore_index=True)

    for idx, row in assessment_items.iterrows():
        code = row['discipline_code']
        var_cycle = row['index']

        temp_typ = templates_dir / f"temp_assessment_{var_cycle}.typ"
        content = f'''#import "templates/7. assessment.typ": *
#show: assessment.with(
  var01: [],
  var_cycle : {var_cycle}
)
'''
        temp_typ.write_text(content, encoding='utf-8')

        output_pdf = output_dir / f"7. {code}.pdf"
        success, msg = compile_typst(temp_typ, output_pdf, templates_dir)

        if success:
            created_pdfs.append(output_pdf)
        else:
            errors.append(f"7. {code}: {msg}")

        temp_typ.unlink(missing_ok=True)
        report_progress(f"7. {code}.pdf")

    # 8a. Upbringing.pdf
    typ_file = templates_dir / "8a. Upbringing.typ"
    output_pdf = output_dir / "8a. Upbringing.pdf"
    if typ_file.exists():
        success, msg = compile_typst(typ_file, output_pdf)
        if success:
            created_pdfs.append(output_pdf)
        else:
            errors.append(f"8a. Upbringing: {msg}")
    report_progress("8a. Upbringing.pdf")

    # 8b. Cal_upbringing.pdf
    typ_file = templates_dir / "8b. Cal_upbringing.typ"
    output_pdf = output_dir / "8b. Cal_upbringing.pdf"
    if typ_file.exists():
        success, msg = compile_typst(typ_file, output_pdf)
        if success:
            created_pdfs.append(output_pdf)
        else:
            errors.append(f"8b. Cal_upbringing: {msg}")
    report_progress("8b. Cal_upbringing.pdf")

    return created_pdfs, errors


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
        prefix = pdf.name.split(".")[0]
        name = type_names.get(prefix, prefix)
        stats[name] = stats.get(name, 0) + 1

    return stats
