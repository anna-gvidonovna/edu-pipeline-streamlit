"""
Educational Pipeline - Генератор документов образовательной программы
Streamlit веб-приложение для конвертации PLX -> CSV
"""

import streamlit as st
import pandas as pd
from io import BytesIO
import zipfile
import os

from lib.plx_parser import parse_plx
from lib.json_to_csv import convert_to_csvs
from lib.xlsx_merger import merge_with_xlsx, get_xlsx_structure
from lib.pdf_generator import check_typst_available, generate_all_pdfs, get_pdf_statistics
from pathlib import Path
import tempfile
import shutil

# Конфигурация страницы
st.set_page_config(
    page_title="Комплект ОП",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="auto"
)

# =============================================================================
# Аутентификация
# =============================================================================
def check_password():
    """Проверка пароля для доступа к приложению."""

    # Пароль из переменной окружения (для Streamlit Cloud) или дефолтный
    correct_password = os.environ.get("APP_PASSWORD", "0000")

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        return True

    st.title("🔐 Женщина-апостол не пускает!")
    st.markdown("Введите пароль для доступа")

    password = st.text_input("Пароль", type="password")

    if st.button("Войти", type="primary"):
        if password == correct_password:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Я тебя не боюсь, тварь!")

    return False

# Проверяем аутентификацию
if not check_password():
    st.stop()

# Заголовок
st.title("🎓 Генератор документов образовательной программы")
st.markdown("Конвертация PLX файлов учебных планов в CSV для генерации РПД")

# Инициализация состояния сессии
if 'program_data' not in st.session_state:
    st.session_state.program_data = None
if 'csvs' not in st.session_state:
    st.session_state.csvs = None
if 'merged' not in st.session_state:
    st.session_state.merged = None

# =============================================================================
# Шаг 1: Загрузка PLX
# =============================================================================
st.header("Шаг 1: Загрузите PLX файл")
st.markdown("PLX — это XML-файл учебного плана из системы Учебные Планы")

plx_file = st.file_uploader(
    "Выберите PLX файл учебного плана",
    type=['plx', 'xml'],
    help="Файл формата .plx или .xml с данными учебного плана"
)

if plx_file is not None:
    try:
        with st.spinner("Парсинг PLX файла..."):
            program_data = parse_plx(plx_file.read())

        if program_data:
            st.session_state.program_data = program_data
            st.success(f"✅ Ура, победа!")

            # Показываем информацию о программе
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Программа", program_data.get('program_name', 'Не указано')[:50])
                st.metric("Направление", program_data.get('direction', 'Не указано'))
            with col2:
                st.metric("Квалификация", program_data.get('qualification', 'Не указано'))
                st.metric("Форма обучения", program_data.get('form_of_study', 'Не указано'))

            # Статистика
            st.markdown("**Статистика:**")
            stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
            with stats_col1:
                st.metric("Компетенций", len(program_data.get('competencies', {})))
            with stats_col2:
                st.metric("Индикаторов", len(program_data.get('indicators', {})))
            with stats_col3:
                st.metric("Дисциплин", len(program_data.get('disciplines', [])))
            with stats_col4:
                st.metric("Профстандартов", len(program_data.get('prof_standards', [])))
        else:
            st.error("❌ Не удалось извлечь данные из PLX файла")

    except Exception as e:
        st.error(f"❌ Ошибка при парсинге PLX: {str(e)}")

# =============================================================================
# Шаг 2: Превью данных и конвертация в CSV
# =============================================================================
if st.session_state.program_data is not None:
    st.divider()
    st.header("Шаг 2: Проверьте данные и сконвертируйте в CSV")

    # Конвертация в CSV
    if st.session_state.csvs is None:
        with st.spinner("Конвертация в CSV..."):
            st.session_state.csvs = convert_to_csvs(st.session_state.program_data)

    csvs = st.session_state.csvs

    # Табы для просмотра данных
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Компетенции", "📚 Дисциплины", "🎯 Индикаторы", "🔗 Matching"])

    with tab1:
        st.subheader("Компетенции")
        st.dataframe(csvs['competences'], use_container_width=True, height=300)

    with tab2:
        st.subheader("Дисциплины (широкий формат)")
        # Показываем только основные колонки для читаемости
        display_cols = ['discipline_code', 'discipline']
        if 'credits_sem1' in csvs['wide'].columns:
            display_cols.extend(['credits_sem1', 'credits_sem2', 'credits_sem3', 'credits_sem4'])
        st.dataframe(csvs['wide'][display_cols], use_container_width=True, height=300)

    with tab3:
        st.subheader("Индикаторы компетенций")
        st.dataframe(csvs['indicators'], use_container_width=True, height=300)

    with tab4:
        st.subheader("Связи дисциплина-компетенция")
        st.dataframe(csvs['matching'][['discipline_code', 'discipline', 'competence_code', 'indicator_code']],
                     use_container_width=True, height=300)

    # Кнопки скачивания базовых CSV
    st.markdown("### Скачать базовые CSV файлы")
    st.markdown("Эти файлы можно использовать без дополнительного Excel файла.")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.download_button(
            "📥 title.csv",
            csvs['title'].to_csv(index=False, encoding='utf-8'),
            "title.csv",
            "text/csv"
        )
        st.download_button(
            "📥 competences.csv",
            csvs['competences'].to_csv(index=False, encoding='utf-8'),
            "competences.csv",
            "text/csv"
        )
    with col2:
        st.download_button(
            "📥 indicators.csv",
            csvs['indicators'].to_csv(index=False, encoding='utf-8'),
            "indicators.csv",
            "text/csv"
        )
        st.download_button(
            "📥 matching.csv",
            csvs['matching'].to_csv(index=False, encoding='utf-8'),
            "matching.csv",
            "text/csv"
        )
    with col3:
        st.download_button(
            "📥 long.csv",
            csvs['long'].to_csv(index=False, encoding='utf-8'),
            "long.csv",
            "text/csv"
        )
        st.download_button(
            "📥 wide.csv",
            csvs['wide'].to_csv(index=False, encoding='utf-8'),
            "wide.csv",
            "text/csv"
        )

# =============================================================================
# Шаг 3: Загрузка Excel с дополнительными данными
# =============================================================================
if st.session_state.csvs is not None:
    st.divider()
    st.header("Шаг 3: Загрузите Excel с дополнительными данными (опционально)")

    st.markdown("""
    Для генерации полных РПД нужен Excel файл с дополнительной информацией.

    **Структура Excel файла (3 листа):**

    | Лист | Колонки |
    |------|---------|
    | `indicators` | indicator_code, know, can, experience, bullets |
    | `disciplines` | discipline_code, aim, tasks, topics, literature_base, literature_add |
    | `assessment` | Q, Q_opt, A, ID |
    """)

    xlsx_file = st.file_uploader(
        "Выберите Excel файл (.xlsx)",
        type=['xlsx'],
        help="Excel файл с листами: indicators, disciplines, assessment"
    )

    if xlsx_file is not None:
        try:
            xlsx_content = xlsx_file.read()

            # Показываем структуру файла
            with st.spinner("Анализ Excel файла..."):
                structure = get_xlsx_structure(xlsx_content)

            st.success("✅ Excel файл загружен!")
            st.markdown("**Найденные листы:**")

            for sheet_name, info in structure.items():
                st.markdown(f"- **{sheet_name}**: {info['rows']} строк, {info['columns']} колонок")
                st.markdown(f"  Колонки: `{', '.join(info['column_names'][:5])}{'...' if len(info['column_names']) > 5 else ''}`")

            # Объединение данных
            if st.button("🔗 Объединить данные", type="primary"):
                with st.spinner("Объединение данных..."):
                    st.session_state.merged = merge_with_xlsx(st.session_state.csvs, xlsx_content)
                st.success("✅ Данные объединены!")
                st.rerun()

        except Exception as e:
            st.error(f"❌ Ошибка при чтении Excel: {str(e)}")

# =============================================================================
# Шаг 4: Скачивание результатов
# =============================================================================
if st.session_state.merged is not None:
    st.divider()
    st.header("Шаг 4: Скачайте результаты")

    merged = st.session_state.merged

    # Превью объединённых данных
    tab1, tab2, tab3 = st.tabs(["🎯 Индикаторы (merge)", "📚 Дисциплины (merge)", "❓ Assessment"])

    with tab1:
        st.subheader("Индикаторы с дополнительной информацией")
        st.dataframe(merged['indicators_merge'], use_container_width=True, height=300)

    with tab2:
        st.subheader("Дисциплины с дополнительной информацией")
        # Показываем новые колонки
        new_cols = ['discipline_code', 'discipline', 'aim', 'tasks', 'topics']
        available_cols = [c for c in new_cols if c in merged['wide_merge'].columns]
        st.dataframe(merged['wide_merge'][available_cols], use_container_width=True, height=300)

    with tab3:
        st.subheader("Вопросы для оценивания")
        st.dataframe(merged['assessment'], use_container_width=True, height=300)

    # Кнопки скачивания
    st.markdown("### Скачать объединённые CSV файлы")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.download_button(
            "📥 indicators_merge.csv",
            merged['indicators_merge'].to_csv(index=False, encoding='utf-8'),
            "indicators_merge.csv",
            "text/csv"
        )
    with col2:
        st.download_button(
            "📥 wide_merge.csv",
            merged['wide_merge'].to_csv(index=False, encoding='utf-8'),
            "wide_merge.csv",
            "text/csv"
        )
    with col3:
        st.download_button(
            "📥 assessment.csv",
            merged['assessment'].to_csv(index=False, encoding='utf-8'),
            "assessment.csv",
            "text/csv"
        )

    # Скачать все файлы одним архивом
    st.markdown("### Скачать все файлы архивом")

    def create_zip():
        """Создаёт ZIP архив со всеми CSV файлами."""
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Базовые CSV
            for name, df in st.session_state.csvs.items():
                zip_file.writestr(f"{name}.csv", df.to_csv(index=False, encoding='utf-8'))
            # Объединённые CSV
            for name, df in merged.items():
                zip_file.writestr(f"{name}.csv", df.to_csv(index=False, encoding='utf-8'))
        zip_buffer.seek(0)
        return zip_buffer

    program_name = st.session_state.program_data.get('program_name', 'program')
    # Очищаем имя от спецсимволов
    safe_name = "".join(c for c in program_name if c.isalnum() or c in (' ', '-', '_'))[:50]

    st.download_button(
        "📦 Скачать все CSV (ZIP)",
        create_zip(),
        f"{safe_name}_csv.zip",
        "application/zip"
    )

# =============================================================================
# Шаг 5: Генерация PDF
# =============================================================================
if st.session_state.merged is not None:
    st.divider()
    st.header("Шаг 5: Генерация PDF")

    # Проверяем доступность Typst
    typst_available, typst_msg = check_typst_available()

    if not typst_available:
        st.warning(f"""
        ⚠️ **{typst_msg}**

        Для генерации PDF установите библиотеку typst:
        ```bash
        pip install typst
        ```
        """)
    else:
        st.success("✅ Typst доступен!")

        # Путь к шаблонам (встроены в проект)
        default_templates = Path(__file__).parent / "typst_templates"

        templates_path = st.text_input(
            "Путь к директории с Typst шаблонами",
            value=str(default_templates) if default_templates.exists() else "",
            help="По умолчанию используются встроенные шаблоны. Можно указать свой путь."
        )

        if templates_path and Path(templates_path).exists():
            templates_dir = Path(templates_path)

            # Проверяем наличие шаблонов
            required_templates = ["1. Program.typ", "templates/4. module.typ"]
            missing = [t for t in required_templates if not (templates_dir / t).exists()]

            if missing:
                st.error(f"❌ Не найдены шаблоны: {', '.join(missing)}")
            else:
                st.success(f"✅ Шаблоны найдены в: {templates_dir}")

                # Статистика по PDF
                wide_df = st.session_state.merged.get('wide_merge', st.session_state.csvs.get('wide'))
                if wide_df is not None:
                    disciplines_count = len(wide_df[
                        wide_df['discipline_code'].str.startswith('Б1') |
                        wide_df['discipline_code'].str.startswith('ФТД')
                    ])
                    practices_count = len(wide_df[wide_df['discipline_code'].str.startswith('Б2')])
                    finals_count = len(wide_df[wide_df['discipline_code'].str.startswith('Б3')])

                    total_pdfs = 3 + disciplines_count + practices_count + (1 if finals_count > 0 else 0) + disciplines_count + practices_count + 2

                    st.markdown(f"""
                    **Будет создано PDF файлов:**
                    - 1x Program, 1x Plan, 1x Calendar
                    - {disciplines_count}x Module (дисциплины)
                    - {practices_count}x Practice (практики)
                    - 1x Finals (ГИА)
                    - {disciplines_count + practices_count}x Assessment (ФОСы)
                    - 2x Upbringing

                    **Всего: ~{total_pdfs} PDF файлов**
                    """)

                if st.button("🚀 Генерировать PDF", type="primary"):
                    # Создаём временную директорию для PDF
                    with tempfile.TemporaryDirectory() as temp_dir:
                        output_dir = Path(temp_dir) / "pdf_output"
                        output_dir.mkdir()

                        # Прогресс-бар
                        progress_bar = st.progress(0)
                        status_text = st.empty()

                        def update_progress(current, total, message):
                            progress_bar.progress(current / total)
                            status_text.text(f"[{current}/{total}] {message}")

                        # Генерация
                        with st.spinner("Генерация PDF..."):
                            created_pdfs, errors = generate_all_pdfs(
                                st.session_state.csvs,
                                st.session_state.merged,
                                templates_dir,
                                output_dir,
                                progress_callback=update_progress
                            )

                        progress_bar.progress(1.0)
                        status_text.text("Готово!")

                        # Результаты
                        if created_pdfs:
                            st.success(f"✅ Создано {len(created_pdfs)} PDF файлов!")

                            # Статистика
                            stats = get_pdf_statistics(created_pdfs)
                            st.markdown("**По категориям:**")
                            for category, count in stats.items():
                                st.markdown(f"- {category}: {count}")

                            # Создаём ZIP с PDF
                            zip_buffer = BytesIO()
                            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                                for pdf_path in created_pdfs:
                                    zip_file.write(pdf_path, pdf_path.name)
                            zip_buffer.seek(0)

                            program_name = st.session_state.program_data.get('program_name', 'program')
                            safe_name = "".join(c for c in program_name if c.isalnum() or c in (' ', '-', '_'))[:50]

                            st.download_button(
                                "📦 Скачать все PDF (ZIP)",
                                zip_buffer,
                                f"{safe_name}_pdf.zip",
                                "application/zip"
                            )

                        if errors:
                            st.warning(f"⚠️ Ошибки при генерации ({len(errors)}):")
                            for err in errors[:10]:
                                st.text(f"  - {err}")
                            if len(errors) > 10:
                                st.text(f"  ... и ещё {len(errors) - 10} ошибок")

        elif templates_path:
            st.error(f"❌ Директория не найдена: {templates_path}")

# =============================================================================
# Footer
# =============================================================================
st.divider()
st.markdown("""
---
**Инструкция:**
1. Загрузите PLX файл учебного плана
2. Проверьте извлечённые данные
3. (Опционально) Загрузите Excel с дополнительной информацией
4. Скачайте CSV файлы
5. Генерируйте PDF через Typst
""")
