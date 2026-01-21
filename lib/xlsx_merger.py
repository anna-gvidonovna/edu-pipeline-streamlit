"""
XLSX Merger - объединение CSV с данными из Excel файла
Адаптировано из Notebook 3: Numbers + CSV -> CSV
Заменено: numbers_parser -> openpyxl для работы с Excel
"""

import pandas as pd
from typing import Dict, Any
from io import BytesIO


def extract_tables_from_xlsx(xlsx_content: bytes) -> Dict[str, pd.DataFrame]:
    """
    Извлекает данные из Excel файла (.xlsx).

    Args:
        xlsx_content: Содержимое Excel файла в байтах

    Returns:
        Словарь с DataFrame для каждого листа
    """
    tables = {}

    # Читаем Excel файл
    xlsx_file = BytesIO(xlsx_content)
    excel_file = pd.ExcelFile(xlsx_file, engine='openpyxl')

    # Получаем все листы
    sheet_names = excel_file.sheet_names

    for sheet_name in sheet_names:
        # Читаем лист в DataFrame
        df = pd.read_excel(excel_file, sheet_name=sheet_name, dtype=str)
        # Заполняем NaN пустыми строками
        df = df.fillna('')
        tables[sheet_name] = df

    return tables


def merge_indicators(indicators_df: pd.DataFrame, tables: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Объединяет indicators.csv с данными из Excel.

    Args:
        indicators_df: DataFrame с индикаторами
        tables: Словарь с таблицами из Excel

    Returns:
        Объединённый DataFrame с индикаторами
    """
    # Ожидаемые колонки результата
    expected_columns = ['indicator_code', 'indicator', 'competence_type', 'task_type',
                        'know', 'can', 'experience', 'bullets']

    # Копируем исходный DataFrame
    indicators_merge = indicators_df.copy()

    # Переименовываем колонку competence_code в indicator_code если нужно
    if 'competence_code' in indicators_merge.columns and 'indicator_code' not in indicators_merge.columns:
        indicators_merge = indicators_merge.rename(columns={'competence_code': 'indicator_code'})

    # Ищем таблицу indicators в Excel
    indicators_additional = None
    for table_name in tables.keys():
        if 'indicator' in table_name.lower() or 'индикатор' in table_name.lower():
            indicators_additional = tables[table_name]
            break

    if indicators_additional is not None:
        # Определяем ключ для соединения
        merge_key = None
        for possible_key in ['indicator_code', 'code', 'competence_code', 'ID']:
            if possible_key in indicators_additional.columns:
                merge_key = possible_key
                break

        if merge_key:
            # Переименовываем ключ если нужно
            if merge_key != 'indicator_code':
                indicators_additional = indicators_additional.rename(columns={merge_key: 'indicator_code'})

            # Соединяем таблицы
            indicators_merge = pd.merge(
                indicators_merge,
                indicators_additional,
                on='indicator_code',
                how='left',
                suffixes=('', '_xlsx')
            )

            # Обрабатываем дублирующиеся колонки
            for col in ['indicator', 'competence_type', 'task_type']:
                if f'{col}_xlsx' in indicators_merge.columns:
                    indicators_merge[col] = indicators_merge[col].fillna(indicators_merge[f'{col}_xlsx'])
                    indicators_merge = indicators_merge.drop(columns=[f'{col}_xlsx'])

    # Убеждаемся, что все нужные колонки присутствуют
    for col in expected_columns:
        if col not in indicators_merge.columns:
            indicators_merge[col] = ''

    # Выбираем только нужные колонки в правильном порядке
    indicators_merge = indicators_merge[expected_columns]

    # Заполняем NaN пустыми строками
    indicators_merge = indicators_merge.fillna('')

    return indicators_merge


def merge_wide(wide_df: pd.DataFrame, tables: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Объединяет wide.csv с данными из Excel.

    Args:
        wide_df: DataFrame с дисциплинами в широком формате
        tables: Словарь с таблицами из Excel

    Returns:
        Объединённый DataFrame с дисциплинами
    """
    # Дополнительные колонки из Excel
    additional_columns = ['aim', 'tasks', 'topics', 'topics_abstract',
                          'literature_base', 'literature_add', 'current_topics']

    # Копируем исходный DataFrame
    wide_merge = wide_df.copy()

    # Ищем таблицу disciplines в Excel
    disciplines_additional = None
    for table_name in tables.keys():
        if 'discipline' in table_name.lower() or 'дисциплин' in table_name.lower():
            disciplines_additional = tables[table_name]
            break

    if disciplines_additional is not None:
        # Определяем ключ для соединения
        merge_key = None
        for possible_key in ['discipline_code', 'code', 'дисциплина_код', 'ID']:
            if possible_key in disciplines_additional.columns:
                merge_key = possible_key
                break

        if merge_key:
            # Переименовываем ключ если нужно
            if merge_key != 'discipline_code':
                disciplines_additional = disciplines_additional.rename(columns={merge_key: 'discipline_code'})

            # Выбираем только нужные колонки
            cols_to_merge = ['discipline_code']
            for col in additional_columns:
                if col in disciplines_additional.columns:
                    cols_to_merge.append(col)

            # Соединяем таблицы
            wide_merge = pd.merge(
                wide_merge,
                disciplines_additional[cols_to_merge],
                on='discipline_code',
                how='left'
            )

    # Убеждаемся, что все дополнительные колонки присутствуют
    for col in additional_columns:
        if col not in wide_merge.columns:
            wide_merge[col] = ''

    # Переупорядочиваем колонки: сначала все колонки из wide_df, затем дополнительные
    original_columns = list(wide_df.columns)
    column_order = original_columns + [col for col in additional_columns if col not in original_columns]
    wide_merge = wide_merge[[col for col in column_order if col in wide_merge.columns]]

    # Заполняем NaN пустыми строками
    wide_merge = wide_merge.fillna('')

    return wide_merge


def extract_assessment(tables: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Извлекает таблицу assessment из Excel.

    Args:
        tables: Словарь с таблицами из Excel

    Returns:
        DataFrame с вопросами для оценивания
    """
    expected_columns = ['Q', 'Q_opt', 'A', 'ID']

    # Ищем таблицу assessment в Excel
    assessment_data = None
    for table_name in tables.keys():
        if 'assessment' in table_name.lower() or 'оценивание' in table_name.lower():
            assessment_data = tables[table_name]
            break

    if assessment_data is None:
        # Возвращаем пустой DataFrame с нужными колонками
        return pd.DataFrame(columns=expected_columns)

    # Создаем маппинг возможных названий колонок
    column_mapping = {
        'Q': ['Q', 'question', 'вопрос', 'Question'],
        'Q_opt': ['Q_opt', 'options', 'варианты', 'Options'],
        'A': ['A', 'answer', 'ответ', 'Answer'],
        'ID': ['ID', 'id', 'код', 'Code']
    }

    # Переименовываем колонки если нужно
    for target_col, possible_names in column_mapping.items():
        for possible_name in possible_names:
            if possible_name in assessment_data.columns and target_col not in assessment_data.columns:
                assessment_data = assessment_data.rename(columns={possible_name: target_col})
                break

    # Убеждаемся, что все нужные колонки присутствуют
    for col in expected_columns:
        if col not in assessment_data.columns:
            assessment_data[col] = ''

    # Выбираем только нужные колонки в правильном порядке
    assessment = assessment_data[expected_columns].copy()

    # Заполняем NaN пустыми строками
    assessment = assessment.fillna('')

    return assessment


def merge_with_xlsx(csvs: Dict[str, pd.DataFrame], xlsx_content: bytes) -> Dict[str, pd.DataFrame]:
    """
    Главная функция: объединяет CSV с данными из Excel файла.

    Args:
        csvs: Словарь с DataFrame (из convert_to_csvs)
        xlsx_content: Содержимое Excel файла в байтах

    Returns:
        Словарь с тремя обогащёнными DataFrame:
        - indicators_merge: индикаторы + know/can/experience
        - wide_merge: дисциплины + aim/tasks/topics/literature
        - assessment: вопросы для оценивания
    """
    # Извлекаем таблицы из Excel
    tables = extract_tables_from_xlsx(xlsx_content)

    # Объединяем индикаторы
    indicators_merge = merge_indicators(csvs['indicators'], tables)

    # Объединяем дисциплины
    wide_merge = merge_wide(csvs['wide'], tables)

    # Извлекаем assessment
    assessment = extract_assessment(tables)

    return {
        'indicators_merge': indicators_merge,
        'wide_merge': wide_merge,
        'assessment': assessment
    }


def get_xlsx_structure(xlsx_content: bytes) -> Dict[str, Dict[str, Any]]:
    """
    Возвращает структуру Excel файла для превью.

    Args:
        xlsx_content: Содержимое Excel файла в байтах

    Returns:
        Словарь с информацией о каждом листе
    """
    tables = extract_tables_from_xlsx(xlsx_content)

    structure = {}
    for table_name, df in tables.items():
        structure[table_name] = {
            'rows': len(df),
            'columns': len(df.columns),
            'column_names': list(df.columns)
        }

    return structure
