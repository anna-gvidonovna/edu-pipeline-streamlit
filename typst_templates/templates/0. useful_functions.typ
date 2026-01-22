#let delete-indices(arr, indices) = {
  arr.enumerate().filter(((i, v)) => i not in indices).map(((i, v)) => v)
}

#let title_csv = csv("../csv/title.csv", row-type: dictionary)
#let competences_csv = csv("../csv/competences.csv", row-type: dictionary)
#let indicators_csv = csv("../csv/indicators_merge.csv", row-type: dictionary)
#let module_desc = csv("../csv/wide_merge.csv", row-type: dictionary)
#let assessment_csv = csv("../csv/assessment.csv", row-type: dictionary)

#let title_n = 0

#let edu_protocol_number = title_csv.at(title_n).at("edu_protocol_number")
#let edu_protocol_date = title_csv.at(title_n).at("edu_protocol_date")
#let is_new_edition = false // показывать "(новая редакция)" в документах
#let new_edition_text = if is_new_edition { " (новая редакция)" } else { "" }
#let qualification = title_csv.at(title_n).at("qualification")
#let level = if qualification == "магистр" [высшее образование — магистратура] else [высшее образование — бакалавриат]
#let start_year = title_csv.at(title_n).at("start_year")
#let form_of_study = title_csv.at(title_n).at("form_of_study")
#let fgos_number = title_csv.at(title_n).at("fgos_number")
#let fgos_date = title_csv.at(title_n).at("fgos_date")
#let duration_years = title_csv.at(title_n).at("duration_years")
#let direction = title_csv.at(title_n).at("direction")
#let program_name = title_csv.at(title_n).at("program_name")
#let faculty_name = title_csv.at(title_n).at("faculty_name")
#let program_total = title_csv.at(title_n).at("program_total")
#let prof_index = title_csv.at(title_n).at("prof_index")
#let prof_title = title_csv.at(title_n).at("prof_title")
#let prof_func_index = title_csv.at(title_n).at("prof_func_index")
#let prof_func_title = title_csv.at(title_n).at("prof_func_title")
#let task_type = indicators_csv.slice(1).map(row => row.at("task_type")).filter(t => t != "" and t != none).dedup()
#let task_type_len = task_type.len()
#let bullets = delete-indices(indicators_csv.map(row => (row.at("bullets"))).dedup(), (0,1))
#let bullets_per_task = calc.floor(bullets.len() / task_type_len)
#let indicators_results = indicators_csv.map(row => (row.at("task_type")))

// Функция для капитализации текста (первая буква заглавная, остальные строчные)
#let capitalize(text) = {
  let s = str(text).trim()
  if s.len() == 0 {
    return s
  }
  let chars = s.clusters()
  upper(chars.first()) + lower(chars.slice(1).join())
}

// Функция для извлечения префикса (УК–1.1 -> УК–1)
#let get_prefix(code) = {
  let parts = code.split(".")
  parts.at(0)
}

 // Функция для создания таблицы с объединением ячеек
#let create_merged_table(data) = {
    let result = ()
    let prev_code = none
    let rowspan = 1
    let start_idx = 0
    
    for i in range(data.len()) {
      let current_code = data.at(i).at(0)
      
      if current_code == prev_code {
        rowspan += 1
      } else {
        if prev_code != none {
          // Добавляем строки с объединением
          result.push(table.cell(
            rowspan: rowspan,
            [#data.at(start_idx).at(1)]  // Используем колонку с кодом+текстом
          ))
          for j in range(start_idx, start_idx + rowspan) {
            result.push([#data.at(j).at(2)])
          }
        }
        rowspan = 1
        start_idx = i
        prev_code = current_code
      }
    }
    
    // Последняя группа
    if data.len() > 0 {
      result.push(table.cell(
        rowspan: rowspan,
        [#data.at(start_idx).at(1)]  // Используем колонку с кодом+текстом
      ))
      for j in range(start_idx, start_idx + rowspan) {
        result.push([#data.at(j).at(2)])
      }
    }
    
    result
  }

 // Функция для создания таблицы ПК с группировкой по task_type
#let create_pk_table(data) = {
  let result = ()
  
  // Группируем по task_type
  let grouped = (:)  // Используем dictionary
  for item in data {
    let task = item.at(3)  // task_type
    if task not in grouped {
      grouped.insert(task, ())
    }
    grouped.at(task).push(item)
  }
  
  // Создаем таблицу
  for (task_type, items) in grouped.pairs() {  // Используем .pairs()
    // Заголовок task_type (объединяем на всю ширину)
    result.push(table.cell(
      colspan: 3,
      [тип задач: #task_type]
    ))
    
    // Обрабатываем компетенции внутри этого task_type
    let prev_code = none
    let rowspan = 1
    let start_idx = 0
    
    for i in range(items.len()) {
      let current_code = items.at(i).at(0)
      
      if current_code == prev_code {
        rowspan += 1
      } else {
        if prev_code != none {
          // Компетенция
          result.push(table.cell(
            rowspan: rowspan,
            [#items.at(start_idx).at(1)]
          ))
          // Индикаторы и основания
          for j in range(start_idx, start_idx + rowspan) {
            result.push([#items.at(j).at(2)])  // Индикатор
            result.push([#items.at(j).at(4)])  // Основание
          }
        }
        rowspan = 1
        start_idx = i
        prev_code = current_code
      }
    }
    
    // Последняя группа компетенций
    if items.len() > 0 {
      result.push(table.cell(
        rowspan: rowspan,
        [#items.at(start_idx).at(1)]
      ))
      for j in range(start_idx, start_idx + rowspan) {
        result.push([#items.at(j).at(2)])
        result.push([#items.at(j).at(4)])
      }
    }
  }
  
  result
}

// Функция для получения префикса кода индикатора (например, УК-1.1 -> УК-1)
#let get-prefix(indicator_code) = {
  let parts = indicator_code.split(".")
  if parts.len() > 0 {
    parts.at(0)
  } else {
    indicator_code
  }
}

// Функция для получения всех компетенций конкретной дисциплины
#let get-discipline-competences(matching_csv, discipline_code) = {
  let result = ()
  
  // Пропускаем заголовок (первая строка)
  for i in range(1, matching_csv.len()) {
    let row = matching_csv.at(i)
    if row.at(0) == discipline_code {  // discipline_code - индекс 0
      result.push((
        comp_code: row.at(2),      // competence_code
        comp_text: row.at(3),      // competence
        indicator_code: row.at(4), // indicator_code
        indicator: row.at(5),      // indicator
        comp_type: row.at(6),      // competence_type
        task_type: row.at(7),      // task_type
      ))
    }
  }
  
  result
}

// Функция для получения планируемых результатов из indicators_merge
#let get-learning-outcomes(indicators_csv, indicator_code) = {
  for i in range(1, indicators_csv.len()) {
    let row = indicators_csv.at(i)
    if row.at(0) == indicator_code {  // indicator_code - индекс 0
      let know = row.at(4)     // know
      let can = row.at(5)      // can
      let experience = row.at(6) // experience
      
      let outcomes = []
      if know != "" and know != none [
      *Знать:* #know\ 
      ]
      if can != "" and can != none [
      *Уметь:* #can\
      ]
      if experience != "" and experience != none [
      *Иметь практический опыт:* #experience
      ]
      
      outcomes
    }
  }
  []
}

// Подготовка данных с планируемыми результатами
#let prepare-competence-data-with-outcomes(comp_data, indicators_csv) = {
  let uk_opk_data = ()
  let pk_data = ()
  
  for item in comp_data {
    let outcomes = get-learning-outcomes(indicators_csv, item.indicator_code)
    
    if item.comp_type == "профессиональный" {
      pk_data.push((
        item.comp_code,                                    // 0
        item.comp_code + " " + item.comp_text,            // 1
        item.indicator_code + " " + item.indicator,       // 2
        item.task_type,                                    // 3
        outcomes,                                          // 4 - планируемые результаты
      ))
    } else {
      uk_opk_data.push((
        item.comp_code,                                    // 0
        item.comp_code + " " + item.comp_text,            // 1
        item.indicator_code + " " + item.indicator,       // 2
        outcomes,                                          // 3 - планируемые результаты
      ))
    }
  }
  
  (uk_opk: uk_opk_data, pk: pk_data)
}

// Функция для создания таблицы УК/ОПК с планируемыми результатами
#let create-uk-opk-table(data) = {
  let result = ()
  
  if data.len() == 0 {
    return result
  }
  
  let prev_code = none
  let rowspan = 1
  let start_idx = 0
  
  for i in range(data.len()) {
    let current_code = data.at(i).at(0)
    
    if current_code == prev_code {
      rowspan += 1
    } else {
      if prev_code != none {
        result.push(table.cell(
          rowspan: rowspan,
          [#data.at(start_idx).at(1)]  // comp_code + comp_text
        ))
        for j in range(start_idx, start_idx + rowspan) {
          result.push([#data.at(j).at(2)])  // indicator
          result.push([#data.at(j).at(3)])  // планируемые результаты
        }
      }
      rowspan = 1
      start_idx = i
      prev_code = current_code
    }
  }
  
  // Последняя группа
  result.push(table.cell(
    rowspan: rowspan,
    [#data.at(start_idx).at(1)]
  ))
  for j in range(start_idx, start_idx + rowspan) {
    result.push([#data.at(j).at(2)])
    result.push([#data.at(j).at(3)])
  }
  
  result
}

// Функция для создания таблицы ПК с планируемыми результатами
#let create-pk-table(data) = {
  let result = ()
  
  if data.len() == 0 {
    return result
  }
  
  // Группируем по task_type
  let grouped = (:)
  for item in data {
    let task = item.at(3)  // task_type
    if task == "" or task == none {
      task = "Без типа задач"
    }
    if task not in grouped {
      grouped.insert(task, ())
    }
    grouped.at(task).push(item)
  }
  
  // Создаем таблицу
  for (task_type, items) in grouped.pairs() {
    // Заголовок task_type
    result.push(table.cell(
      colspan: 3,
      [тип задач: #task_type]
    ))
    
    // Обрабатываем компетенции
    let prev_code = none
    let rowspan = 1
    let start_idx = 0
    
    for i in range(items.len()) {
      let current_code = items.at(i).at(0)
      
      if current_code == prev_code {
        rowspan += 1
      } else {
        if prev_code != none {
          result.push(table.cell(
            rowspan: rowspan,
            [#items.at(start_idx).at(1)]  // comp_code + comp_text
          ))
          for j in range(start_idx, start_idx + rowspan) {
            result.push([#items.at(j).at(2)])  // indicator
            result.push([#items.at(j).at(4)])  // планируемые результаты
          }
        }
        rowspan = 1
        start_idx = i
        prev_code = current_code
      }
    }
    
    // Последняя группа
    if items.len() > 0 {
      result.push(table.cell(
        rowspan: rowspan,
        [#items.at(start_idx).at(1)]
      ))
      for j in range(start_idx, start_idx + rowspan) {
        result.push([#items.at(j).at(2)])
        result.push([#items.at(j).at(4)])
      }
    }
  }
  
  result
}

// Функция для безопасной конвертации в число
#let to-int(value) = {
  if value == none or value == "" or value == "0" {
    return 0
  }
  
  // Убираем пробелы
  let v = str(value).trim()
  
  // Если есть точка (float), сначала в float, потом в int
  if v.contains(".") {
    return int(calc.round(float(v)))
  }
  
  int(v)
}

// Функция для проверки, есть ли значение
#let has-value(value) = {
  value != none and value != "" and value != "0" and value != "0.0"
}

// Функция для определения формы аттестации
#let get-attestation-form(exam, pass, graded_pass) = {
  if has-value(exam) {
    "экзамен"
  } else if has-value(graded_pass) {
    "зачет с оценкой"
  } else if has-value(pass) {
    "зачет"
  } else {
    ""
  }
}

// Функция для создания таблицы объема работы для семестра
#let create-workload-table(
  semester_num,
  credits,
  lectures,
  labs,
  practice,
  solo,
  control,
  exam,
  pass,
  graded_pass
) = {
  // Проверяем, изучается ли дисциплина в этом семестре
  if not has-value(credits) {
    return none
  }
  
  let attestation = get-attestation-form(exam, pass, graded_pass)
  let credits_float = float(str(credits).trim())
  let total_hours = int(calc.round(credits_float * 36))
  
  // Считаем контактные часы
  let contact_hours = to-int(lectures) + to-int(labs) + to-int(practice)
  let solo_hours = to-int(solo)
  let control_hours = to-int(control)
  
  [
    Общая трудоемкость дисциплины в #semester_num семестре составляет #credits з.е.
    #v(0.5em)
    #table(
      columns: (20fr, 20fr),
      stroke: (x: none, y: 0.25pt + gray),
      row-gutter: (2pt, auto),
      [
        #align(center)[#text(size: 9pt)[виды учебной работы]]
      ],
      [
        #align(center)[#text(size: 9pt)[всего академических часов]]
      ],
      [Контактная работа, в том числе: #v(0.25em)], [#contact_hours],
      
      // Лекции
      ..if has-value(lectures) {
        ([#h(1em)_Лекции_ #v(0.25em)], [#to-int(lectures)])
      } else { () },
      
      // Лабораторные
      ..if has-value(labs) {
        ([#h(1em)_Лабораторные занятия_ #v(0.25em)], [#to-int(labs)])
      } else { () },
      
      // Практические
      ..if has-value(practice) {
        ([#h(1em)_Практические занятия_ #v(0.25em)], [#to-int(practice)])
      } else { () },
      [Самостоятельная работа  #v(0.25em)], [#solo_hours],
            // Контроль - показываем только если > 0
      ..if control_hours > 0 {
        ([#h(1em)_Контроль_ #v(0.25em)], [#control_hours])
      } else { () },
      [Форма промежуточной аттестации #v(0.25em)], [#attestation],
      [Итого #v(0.25em)], [#total_hours],
    )
    #v(1em)
  ]
}

// Функция для получения индексов колонок по семестрам
#let get-semester-column-indices(module_desc) = {
  let headers = module_desc.at(0)
  let indices = (:)

  // Находим все колонки, связанные с семестрами (headers - это dictionary)
  for col in headers.keys() {
    // Извлекаем номер семестра из названия колонки
    if col.contains("_sem") {
      let parts = col.split("_sem")
      if parts.len() > 1 {
        let sem_num = parts.at(1)
        let base_name = parts.at(0)

        if sem_num not in indices {
          indices.insert(sem_num, (:))
        }

        indices.at(sem_num).insert(base_name, col)
      }
    }
  }

  indices
}

// Функция для создания всех таблиц объема дисциплины (универсальная)
#let create-all-workload-tables(module_desc, var_cycle) = {
  let row = module_desc.at(var_cycle)
  let sem_indices = get-semester-column-indices(module_desc)

  // Вспомогательная функция для безопасного получения значения
  let get-col-value(row, cols, col_name) = {
    let col_key = cols.at(col_name, default: none)
    if col_key != none {
      row.at(col_key, default: "")
    } else {
      ""
    }
  }

  // Сортируем семестры по номеру
  let sorted_sems = sem_indices.pairs().sorted(key: ((k, v)) => int(k))

  // Проходим по всем семестрам по порядку
  for (sem_num, cols) in sorted_sems {
    let table_content = create-workload-table(
      sem_num,
      get-col-value(row, cols, "credits"),
      get-col-value(row, cols, "lectures"),
      get-col-value(row, cols, "labs"),
      get-col-value(row, cols, "practice"),
      get-col-value(row, cols, "solo"),
      get-col-value(row, cols, "control"),
      get-col-value(row, cols, "exam"),
      get-col-value(row, cols, "pass"),
      get-col-value(row, cols, "graded_pass")
    )

    if table_content != none {
      table_content
    }
  }
}

// Функция для создания содержания дисциплины из тем и аннотаций
#let create-discipline-content(topics, topics_abstract) = {
  // Разделяем темы и аннотации по точке с запятой
  let topics_list = topics.split(";").map(t => t.trim()).filter(t => t != "")
  let abstract_list = topics_abstract.split(";").map(a => a.trim()).filter(a => a != "")
  
  // Создаем нумерованный список
  for i in range(calc.min(topics_list.len(), abstract_list.len())) {
    [- #topics_list.at(i)
    #v(0.5em)
      #abstract_list.at(i)
    #v(1em)
      
    ]
  }
}

#let create-current-control-table(topics, control_forms: none) = {
  // Разделяем темы по точке с запятой
  let topics_list = topics.split(";").map(t => t.trim()).filter(t => t != "")
  
  // Если формы контроля не указаны, используем стандартную
  let default_form = [устный опрос \ и свободная дискуссия в аудитории]
  
  // Создаем строки таблицы
  let rows = (
    [],
    [#align(center)[#text(size: 9pt)[темы / разделы дисциплины]]],
    [#align(center)[#text(size: 9pt)[форма ТКУ]]],
  )
  
  for i in range(topics_list.len()) {
    rows.push([#(i + 1)])
    rows.push([#topics_list.at(i) #v(0.25em)])
    
    // Используем указанную форму контроля или стандартную
    if control_forms != none and i < control_forms.len() {
      rows.push([#control_forms.at(i)])
    } else {
      rows.push(default_form)
    }
  }
  
  table(
    columns: (0.25fr, 2fr, 2fr),
    stroke: (x: none, y: 0.1pt + rgb(192,192,192)),
    row-gutter: (2pt, auto),
    ..rows
  )
}

// Версия с настройкой отступов
#let format-discussion-topics(current_topics, spacing: 0.3em) = {
  let topics_list = current_topics.split(";").map(t => t.trim()).filter(t => t != "")
  
  v(1em)
  [_Темы для обсуждений:_]
  v(spacing)
  
  list(
    tight: false,
    ..topics_list.map(t => [#t])
  )
}

/// @brief Вспомогательная функция для форматирования ячейки "Вопрос + Варианты".
///
/// @param question: Текст вопроса (строка).
/// @param options: Текст вариантов ответа (строка).
#let format-question-cell(question, options) = {
  [
    #question
    
    // ИСПРАВЛЕНИЕ: Используем #if вместо ..if
    #if has-value(options) {
      // Внутри #if можно использовать 'let'
      let formatted_options = options
        .replace(" Б)", "\nБ)")
        .replace(" В)", "\nВ)")
        .replace(" Г)", "\nГ)")
        .replace(" Д)", "\nД)")
        .replace(" Е)", "\nЕ)")
      
      // Возвращаем контент
      [
        #v(0.5em)
        #formatted_options
      ]
    }
    // Если has-value(options) == false, блок #if ничего не вернет (none),
    // что является корректным поведением.
  ]
}

/// @brief Создает таблицу оценочных средств (с colspan для компетенций) 
///        с сортировкой: сначала закрытые, потом открытые вопросы.
///
/// @param current_discipline_code: Код текущей дисциплины.
/// @param assessment_csv: Данные из CSV-файла с вопросами.
/// @param indicators_csv: Данные из '3.3.1 indicators_merge.csv'.
#let create-assessment-table(
  current_discipline_code,
  assessment_csv,
  indicators_csv
) = {
  // --- Шаг 1: Создаем словарь для текстов компетенций ---
  let comp_text_map = (:)
  for row in indicators_csv.slice(1) {
    let comp_code = row.at("indicator_code", default: "")
    let comp_text = row.at("indicator", default: "")
    if comp_text_map.at(comp_code, default: none) == none {
      comp_text_map.insert(comp_code, comp_code + " " + comp_text)
    }
  }

  // --- Шаг 2: Фильтруем и ГРУППИРУЕМ вопросы по компетенции и типу ---
  let questions_by_comp = (:)

  for row in assessment_csv.slice(1) {
    let full_id = row.at("ID", default: "")

    if full_id.starts-with(current_discipline_code + "_") {
      let id_parts = full_id.split("_")
      if id_parts.len() < 2 { continue }

      let comp_prefix = id_parts.at(1)
      let question_data = (
        question: row.at("Q", default: ""),
        options: row.at("Q_opt", default: ""),
        answer: row.at("A", default: ""),
      )
      
      // Определяем тип вопроса: "closed" (закрытый) или "open" (открытый)
      let question_type = if has-value(question_data.options) { "closed" } else { "open" }
      
      if comp_prefix not in questions_by_comp {
        questions_by_comp.insert(comp_prefix, (closed: (), open: ()))
      }
      
      // Группируем внутри компетенции по типу
      questions_by_comp.at(comp_prefix).at(question_type).push(question_data)
    }
  }

  if questions_by_comp.len() == 0 {
    return [Нет оценочных средств для данной дисциплины.]
  }

  // --- Шаг 3: Строим строки таблицы (ЛОГИКА СОРТИРОВКИ) ---
  let table_rows = (
    // Заголовки, как вы просили
    align(center)[#text(size: 9pt)[задание и варианты ответа]], 
    align(center)[#text(size: 9pt)[верный ответ]], 
  )

  let sorted_prefixes = questions_by_comp.keys().sorted()

  for comp_prefix in sorted_prefixes {
    let comp_group = questions_by_comp.at(comp_prefix)
    let comp_text = comp_text_map.at(comp_prefix, default: comp_prefix)
    
    let all_questions = comp_group.closed + comp_group.open
    
    if all_questions.len() == 0 { continue }

    // Добавляем заголовок компетенции (colspan)
    table_rows.push(table.cell(
      colspan: 2,
      align(left, [*Планируемый результат обучения (код): #comp_text*])
    ))
    
    // 1. Сначала добавляем ЗАКРЫТЫЕ вопросы
    for q in comp_group.closed {
      table_rows.push(format-question-cell(q.question, q.options))
      table_rows.push([#align(center)[#q.answer]]) // Выравниваем ответ по центру
    }
    
    // 2. Затем добавляем ОТКРЫТЫЕ вопросы
    for q in comp_group.open {
      table_rows.push(format-question-cell(q.question, q.options))
      table_rows.push([#align(center)[#q.answer]]) // Выравниваем ответ по центру
    }
  }

  // --- Шаг 4: Возвращаем готовую таблицу (с вашими параметрами) ---
  table(
    columns: (2fr, 1fr), // Ваши 2 колонки
    stroke: (x: none, y: 0.25pt + gray),
    align: left + horizon,
    row-gutter: (2pt, auto),
    ..table_rows
  )
}

// Функция для определения типа практики
#let get-practice-type(praxis) = {
  if praxis == "П" {
    "производственная"
  } else if praxis == "У" {
    "учебная"
  } else {
    ""
  }
}

// Функция для сбора информации о практике по семестрам
#let get-practice-info(module_desc, var_cycle) = {
  let row = module_desc.at(var_cycle)
  let sem_indices = get-semester-column-indices(module_desc)
  
  let practice_semesters = ()
  let control_forms = ()
  let practice_type = ""
  
  // Проходим по всем семестрам
  for (sem_num, cols) in sem_indices.pairs() {
    let praxis = row.at(cols.at("praxis", default: 0))
    
    if has-value(praxis) {
      practice_type = get-practice-type(praxis)
      practice_semesters.push(sem_num)
      
      // Определяем форму контроля
      let exam = row.at(cols.at("exam", default: 0))
      let pass = row.at(cols.at("pass", default: 0))
      let graded_pass = row.at(cols.at("graded_pass", default: 0))
      
      let control = get-attestation-form(exam, pass, graded_pass)
      if control != "" {
        control_forms.push(control)
      }
    }
  }
  
  (
    type: practice_type,
    semesters: practice_semesters,
    controls: control_forms
  )
}

// Функция для создания таблицы практики
#let create-practice-table(module_desc, var_cycle) = {
  let practice_info = get-practice-info(module_desc, var_cycle)
  
  // Если нет практики, не создаем таблицу
  if practice_info.type == "" {
    return none
  }
  
  // Формируем текст о семестрах
  let semesters_text = if practice_info.semesters.len() > 0 {
    practice_info.semesters.join(", ") + " семестр"
    if practice_info.semesters.len() > 1 { "ы" } else { "" }
  } else {
    ""
  }
  
  // Формируем текст о формах контроля
  let control_text = if practice_info.controls.len() > 0 {
    practice_info.controls.join(", ")
  } else {
    ""
  }
  
  [
    #table(
      columns: (1fr, 2fr),
      stroke: (x: none, y: 0.1pt + gray),
      row-gutter: (2pt, auto),
      [
        #align(center)[#text(size: 9pt)[параметр]]
      ],
      [
        #align(center)[#text(size: 9pt)[содержание параметра]]
      ],
      [вид практики], [#practice_info.type],
      
      [практика проводится $*$], [#semesters_text],
      [сроки практики], [в соответствии с календарным учебным графиком и учебным планом],
      table.cell(colspan: 2)[
        $*$ Обучающиеся, совмещающие обучение с трудовой деятельностью, вправе проходить практику по месту трудовой деятельности в случаях, если профессиональная деятельность, осуществляемая ими, соответствует требованиям образовательной программы к проведению практики. 
        #v(0.5em) 
        Практика обучающихся с ограниченными возможностями здоровья и инвалидов организуется с учетом особенностей их психофизического развития, индивидуальных возможностей и состояния здоровья. 
        #v(0.5em) 
        Порядок организации и осуществления практической подготовки обучающихся при проведении практики также регламентируется Положением о практической подготовке обучающихся по программам высшего образования в АНО ВО "Универсальный Университет".
      ]
    )
  ]
}

#let logo = image("../pics/logo.svg", height: auto) 
#let gray = rgb(192,192,192)

#let internet = {
 [- Архи.ру веб-сайт об архитектуре https://archi.ru/ 
- ArchDaily блог об архитектуре https://www.archdaily.com/
- Союз московских архитекторов https://moscowarch.ru/
- Союз архитекторов России  https://uar.ru/]
}

#let author = {

align(top +  left)[
     *Составители рабочей программы:* \
     дизайнер образовательных программ Департамента академического качества – М. А. Бислер 
   ]
pagebreak()
}