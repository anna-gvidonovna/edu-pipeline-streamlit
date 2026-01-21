#import "0. useful_functions.typ": *
#import "0. method_recommend.typ": *
#import "0. mats_techs.typ": *
#let finals(
  // общая информация
   var01: [],
  var_cycle : [],// 
  doc
  )  = {

    for comp_row in competences_csv.slice(1) {
    let comp_code = comp_row.at("competence_code")
    let comp_text = comp_row.at("competence")
    let comp_type = comp_row.at("competence_type")
    let task_type = comp_row.at("task_type")}

 set par(justify: true, spacing: 0.25em)
  set block(spacing: 0.25em)
  
  set heading(numbering: "1.")
  show heading.where(level: 1): set text(size: 11pt, weight: "bold", hyphenate: false)
  show heading.where(level: 1): set align(left)
  
  show heading.where(level: 2): set text(size: 11pt, weight: "regular")
  show heading.where(level: 2): set align(left)

    show heading.where(level: 3): set text(size: 10pt, weight: "regular")
  let row = module_desc.at(var_cycle)
  let discipline_code = row.at("discipline_code", default: "")
  let discipline = row.at("discipline", default: "")
  let discipline_sem1 = row.at("discipline_sem1", default: "")
  let discipline_sem2 = row.at("discipline_sem2", default: "")
  let discipline_sem3 = row.at("discipline_sem3", default: "")
  let discipline_sem4 = row.at("discipline_sem4", default: "")
  let discipline_sem5 = row.at("discipline_sem5", default: "")
  let discipline_sem6 = row.at("discipline_sem6", default: "")
  let discipline_sem7 = row.at("discipline_sem7", default: "")
  let discipline_sem8 = row.at("discipline_sem8", default: "")
  let discipline_sem9 = row.at("discipline_sem9", default: "")
  let discipline_sem10 = row.at("discipline_sem10", default: "")
  let exam_sem1 = row.at("exam_sem1", default: "")
  let exam_sem2 = row.at("exam_sem2", default: "")
  let exam_sem3 = row.at("exam_sem3", default: "")
  let exam_sem4 = row.at("exam_sem4", default: "")
  let exam_sem5 = row.at("exam_sem5", default: "")
  let exam_sem6 = row.at("exam_sem6", default: "")
  let exam_sem7 = row.at("exam_sem7", default: "")
  let exam_sem8 = row.at("exam_sem8", default: "")
  let exam_sem9 = row.at("exam_sem9", default: "")
  let exam_sem10 = row.at("exam_sem10", default: "")
  let pass_sem1 = row.at("pass_sem1", default: "")
  let pass_sem2 = row.at("pass_sem2", default: "")
  let pass_sem3 = row.at("pass_sem3", default: "")
  let pass_sem4 = row.at("pass_sem4", default: "")
  let pass_sem5 = row.at("pass_sem5", default: "")
  let pass_sem6 = row.at("pass_sem6", default: "")
  let pass_sem7 = row.at("pass_sem7", default: "")
  let pass_sem8 = row.at("pass_sem8", default: "")
  let pass_sem9 = row.at("pass_sem9", default: "")
  let pass_sem10 = row.at("pass_sem10", default: "")
  let graded_pass_sem1 = row.at("graded_pass_sem1", default: "")
  let graded_pass_sem2 = row.at("graded_pass_sem2", default: "")
  let graded_pass_sem3 = row.at("graded_pass_sem3", default: "")
  let graded_pass_sem4 = row.at("graded_pass_sem4", default: "")
  let graded_pass_sem5 = row.at("graded_pass_sem5", default: "")
  let graded_pass_sem6 = row.at("graded_pass_sem6", default: "")
  let graded_pass_sem7 = row.at("graded_pass_sem7", default: "")
  let graded_pass_sem8 = row.at("graded_pass_sem8", default: "")
  let graded_pass_sem9 = row.at("graded_pass_sem9", default: "")
  let graded_pass_sem10 = row.at("graded_pass_sem10", default: "")
  let credits_sem1 = row.at("credits_sem1", default: "")
  let credits_sem2 = row.at("credits_sem2", default: "")
  let credits_sem3 = row.at("credits_sem3", default: "")
  let credits_sem4 = row.at("credits_sem4", default: "")
  let credits_sem5 = row.at("credits_sem5", default: "")
  let credits_sem6 = row.at("credits_sem6", default: "")
  let credits_sem7 = row.at("credits_sem7", default: "")
  let credits_sem8 = row.at("credits_sem8", default: "")
  let credits_sem9 = row.at("credits_sem9", default: "")
  let credits_sem10 = row.at("credits_sem10", default: "")
  let lectures_sem1 = row.at("lectures_sem1", default: "")
  let lectures_sem2 = row.at("lectures_sem2", default: "")
  let lectures_sem3 = row.at("lectures_sem3", default: "")
  let lectures_sem4 = row.at("lectures_sem4", default: "")
  let lectures_sem5 = row.at("lectures_sem5", default: "")
  let lectures_sem6 = row.at("lectures_sem6", default: "")
  let lectures_sem7 = row.at("lectures_sem7", default: "")
  let lectures_sem8 = row.at("lectures_sem8", default: "")
  let lectures_sem9 = row.at("lectures_sem9", default: "")
  let lectures_sem10 = row.at("lectures_sem10", default: "")
  let labs_sem1 = row.at("labs_sem1", default: "")
  let labs_sem2 = row.at("labs_sem2", default: "")
  let labs_sem3 = row.at("labs_sem3", default: "")
  let labs_sem4 = row.at("labs_sem4", default: "")
  let labs_sem5 = row.at("labs_sem5", default: "")
  let labs_sem6 = row.at("labs_sem6", default: "")
  let labs_sem7 = row.at("labs_sem7", default: "")
  let labs_sem8 = row.at("labs_sem8", default: "")
  let labs_sem9 = row.at("labs_sem9", default: "")
  let labs_sem10 = row.at("labs_sem10", default: "")
  let practice_sem1 = row.at("practice_sem1", default: "")
  let practice_sem2 = row.at("practice_sem2", default: "")
  let practice_sem3 = row.at("practice_sem3", default: "")
  let practice_sem4 = row.at("practice_sem4", default: "")
  let practice_sem5 = row.at("practice_sem5", default: "")
  let practice_sem6 = row.at("practice_sem6", default: "")
  let practice_sem7 = row.at("practice_sem7", default: "")
  let practice_sem8 = row.at("practice_sem8", default: "")
  let practice_sem9 = row.at("practice_sem9", default: "")
  let practice_sem10 = row.at("practice_sem10", default: "")
  let solo_sem1 = row.at("solo_sem1", default: "")
  let solo_sem2 = row.at("solo_sem2", default: "")
  let solo_sem3 = row.at("solo_sem3", default: "")
  let solo_sem4 = row.at("solo_sem4", default: "")
  let solo_sem5 = row.at("solo_sem5", default: "")
  let solo_sem6 = row.at("solo_sem6", default: "")
  let solo_sem7 = row.at("solo_sem7", default: "")
  let solo_sem8 = row.at("solo_sem8", default: "")
  let solo_sem9 = row.at("solo_sem9", default: "")
  let solo_sem10 = row.at("solo_sem10", default: "")
  let control_sem1 = row.at("control_sem1", default: "")
  let control_sem2 = row.at("control_sem2", default: "")
  let control_sem3 = row.at("control_sem3", default: "")
  let control_sem4 = row.at("control_sem4", default: "")
  let control_sem5 = row.at("control_sem5", default: "")
  let control_sem6 = row.at("control_sem6", default: "")
  let control_sem7 = row.at("control_sem7", default: "")
  let control_sem8 = row.at("control_sem8", default: "")
  let control_sem9 = row.at("control_sem9", default: "")
  let control_sem10 = row.at("control_sem10", default: "")
  let competences_sem1 = row.at("competences_sem1", default: "")
  let competences_sem2 = row.at("competences_sem2", default: "")
  let competences_sem3 = row.at("competences_sem3", default: "")
  let competences_sem4 = row.at("competences_sem4", default: "")
  let competences_sem5 = row.at("competences_sem5", default: "")
  let competences_sem6 = row.at("competences_sem6", default: "")
  let competences_sem7 = row.at("competences_sem7", default: "")
  let competences_sem8 = row.at("competences_sem8", default: "")
  let competences_sem9 = row.at("competences_sem9", default: "")
  let competences_sem10 = row.at("competences_sem10", default: "")
  let grade_year_sem1 = row.at("grade_year_sem1", default: "")
  let grade_year_sem2 = row.at("grade_year_sem2", default: "")
  let grade_year_sem3 = row.at("grade_year_sem3", default: "")
  let grade_year_sem4 = row.at("grade_year_sem4", default: "")
  let grade_year_sem5 = row.at("grade_year_sem5", default: "")
  let grade_year_sem6 = row.at("grade_year_sem6", default: "")
  let grade_year_sem7 = row.at("grade_year_sem7", default: "")
  let grade_year_sem8 = row.at("grade_year_sem8", default: "")
  let grade_year_sem9 = row.at("grade_year_sem9", default: "")
  let grade_year_sem10 = row.at("grade_year_sem10", default: "")
  let no_skip_sem1 = row.at("no_skip_sem1", default: "")
  let no_skip_sem2 = row.at("no_skip_sem2", default: "")
  let no_skip_sem3 = row.at("no_skip_sem3", default: "")
  let no_skip_sem4 = row.at("no_skip_sem4", default: "")
  let no_skip_sem5 = row.at("no_skip_sem5", default: "")
  let no_skip_sem6 = row.at("no_skip_sem6", default: "")
  let no_skip_sem7 = row.at("no_skip_sem7", default: "")
  let no_skip_sem8 = row.at("no_skip_sem8", default: "")
  let no_skip_sem9 = row.at("no_skip_sem9", default: "")
  let no_skip_sem10 = row.at("no_skip_sem10", default: "")
  let praxis_sem1 = row.at("praxis_sem1", default: "")
  let praxis_sem2 = row.at("praxis_sem2", default: "")
  let praxis_sem3 = row.at("praxis_sem3", default: "")
  let praxis_sem4 = row.at("praxis_sem4", default: "")
  let praxis_sem5 = row.at("praxis_sem5", default: "")
  let praxis_sem6 = row.at("praxis_sem6", default: "")
  let praxis_sem7 = row.at("praxis_sem7", default: "")
  let praxis_sem8 = row.at("praxis_sem8", default: "")
  let praxis_sem9 = row.at("praxis_sem9", default: "")
  let praxis_sem10 = row.at("praxis_sem10", default: "")
  let aim = row.at("aim", default: "")
  let tasks = row.at("tasks", default: "")
  let topics = row.at("topics", default: "")
  let topics_abstract = row.at("topics_abstract", default: "")
  let literature_base = row.at("literature_base", default: "")
  let literature_add = row.at("literature_add", default: "")
  let current_topics = row.at("current_topics", default: "")

  let get-discipline-type(discipline_code) = {
  if discipline_code.contains(".О.") {
    "обязательную часть"
  } else if discipline_code.contains(".ДВ.") {
    "элективные дисциплины части, формируемой участниками образовательных отношений"
  } else if discipline_code.contains(".В.") {
    "часть, формируемую участниками образовательных отношений"
  } else {
    "" // or "неопределена" if you want a default
  }
}// Usage:
let disc_type = get-discipline-type(discipline_code)

  let get-conclusion-semesters(..discipline_sems) = {
    let semesters = ()
    let sem_array = discipline_sems.pos()
    
    for (index, value) in sem_array.enumerate() {
      if value != none and value != "" and value != "0" {
        semesters.push(str(index + 1))
      }
    }
    
    semesters
  }
  
  // Использование:
  let conclusion_semesters = get-conclusion-semesters(
    discipline_sem1,
    discipline_sem2,
    discipline_sem3,
    discipline_sem4,
    discipline_sem5,
    discipline_sem6,
    discipline_sem7,
    discipline_sem8,
    discipline_sem9,
    discipline_sem10
  )

  // Функция для получения последнего семестра и его трудоёмкости
  let get-last-semester-info(credits_array) = {
    let last_sem = 0
    let last_credits = ""
    for (index, value) in credits_array.enumerate() {
      if value != none and value != "" and value != "0" {
        last_sem = index + 1
        last_credits = value
      }
    }
    (semester: last_sem, credits: last_credits)
  }

  let last_sem_info = get-last-semester-info((
    credits_sem1, credits_sem2, credits_sem3, credits_sem4, credits_sem5,
    credits_sem6, credits_sem7, credits_sem8, credits_sem9, credits_sem10
  ))

    set page(
  paper: "a4",
  footer: context {
    let page-number = counter(page).at(here()).first()
    if page-number > 2 {
      align(center)[
        #text(size: 10pt)[#(page-number)]
      ]
    }
  }
)

  // шапка
  set text(size: 10pt, lang: "ru", font: "Univers LT CYR")
  set par(justify: false)
  
  table(
    columns: (2fr, 1fr),
    stroke: none,
    [
      #v(0.75em)
      #text(font: "Univers LT CYR", weight: "light")[
      #upper[автономная некоммерческая организация \ высшего образования]]
      #v(0.75em)
      
      #text(font: "Univers LT CYR", weight: "bold")[
        #upper["универсальный университет"]]
    ], 
    [
      #logo
    ],
  )

  set text(size: 11pt, lang: "ru", font: "Times New Roman")
  set par(justify: true, spacing: 0.5em)

  v(2em)
  table(
    columns: (1fr, 2fr),
    stroke: none, 
    [], 
    [#align(right)[#upper[*утверждена*] \
        Ученым советом АНО ВО "Универсальный Университет"  \ в составе образовательной программы высшего образования (новая редакция)
        #v(1em)
       протокол №#edu_protocol_number от #edu_protocol_date]]
     )
     
     v(5em)
     align(center)[
       #faculty_name
     ]

     v(1em)
   align(center)[
    #upper[
      *Программа государственной итоговой аттестации*
    ] \
  ]
v(1em)
  table(
    columns: (0.5fr, 1fr),
    stroke: none,
    [уровень образования:], [#level],
    [направление подготовки:], [#direction], 
    [направленность (профиль):], [#program_name],
    [квалификация:], [#qualification],
   
    [форма обучения:], [#form_of_study],
    [срок обучения (в годах): ], [#duration_years],
    [год набора:], [#start_year]
  )

  align(bottom + center)[
    Москва, 2025
  ]

  pagebreak()

 outline()

  pagebreak()

  heading("Общие положения")

  [В соответствии с Федеральным законом от 29 декабря 2012 г. № 273-ФЗ «Об образовании в Российской Федерации»,  а также ФГОС ВО по направлению подготовки #direction (#level), приказ Министерства образования и науки России от #fgos_date № #fgos_number, освоение основных профессиональных образовательных программ высшего образования завершается государственной итоговой аттестацией выпускников.

]

  heading("Цель и задачи государственной итоговой аттестации", level: 2)

  [Целью государственной итоговой аттестации является установление уровня подготовки выпускника Университета к выполнению профессиональных задач и соответствия его подготовки требованиям Федерального государственного образовательного стандарта высшего образования по направлению подготовки #direction (#level).
#v(0.5em)
  Государственная итоговая аттестация направлена на решение следующих задач:
- оценить полученные выпускниками результаты обучения по дисциплинам образовательной программы, освоение которых имеют определяющее значение для профессиональной деятельности выпускников.
- оценить уровень подготовленности выпускников к самостоятельной профессиональной деятельности.
]

 heading("Формы аттестационных испытаний", level: 2)

  [Форма государственной итоговой аттестации по направлению подготовки #direction (профиль) #program_name: 
- Защита выпускной квалификационной работы.
]
 heading("Область и сферы профессиональной деятельности выпускников", level: 2)

  [#prof_index #capitalize(prof_title) #v(0.5em) Выпускники могут осуществлять профессиональную деятельность в других областях профессиональной деятельности и (или) сферах профессиональной деятельности при условии соответствия уровня их образования и полученных компетенций требованиям к квалификации работника.
]

heading("Типы задач профессиональной деятельности, к которому готовятся выпускники", level: 2)

  [
  #for i in range(task_type_len) [
      - #task_type.at(i)
]
]

heading("Трудоемкость государственной итоговой аттестации", level: 2)

  [Общая трудоемкость в #last_sem_info.semester семестре составляет #last_sem_info.credits з.е. #v(0.5em) К государственной итоговой аттестации допускается обучающийся, не имеющий академической задолженности и в полном объеме выполнивший учебный план или индивидуальный учебный план.]

// Полное использование:
let matching = csv("../csv/matching.csv")
let indicators_merge = csv("../csv/indicators_merge.csv")
let comp_data = get-discipline-competences(matching, discipline_code)
let prepared = prepare-competence-data-with-outcomes(comp_data, indicators_merge)

    // Разделяем данные по типам компетенций
  let uk_opk_data = ()
  let pk_data = ()
  // Собираем данные
  for comp_row in competences_csv.slice(0) {
    let comp_code = comp_row.at("competence_code")
    let comp_text = comp_row.at("competence")
    let comp_type = comp_row.at("competence_type")
    let task_type = comp_row.at("task_type")

    let matching = indicators_csv.slice(0).filter(ind_row => {
      let ind_code = ind_row.at("indicator_code")
      get_prefix(ind_code) == comp_code
    })

    if matching.len() > 0 {
      for ind_row in matching {
        if comp_type == "профессиональный" {
          pk_data.push((
            comp_code,
            comp_code + " " + comp_text,
            ind_row.at("indicator_code") + " " + ind_row.at("indicator"),
            task_type,
            "Профстандарт " + prof_func_index,  // или берите из данных
          ))
        } else {
          uk_opk_data.push((
            comp_code,
            comp_code + " " + comp_text,
            ind_row.at("indicator_code") + " " + ind_row.at("indicator"),
          ))
        }
      }
    }
  }

  // Сортируем: УК идут перед ОПК
  uk_opk_data = uk_opk_data.sorted(key: row => {
    let code = row.at(0)
    if code.starts-with("УК") { 0 }
    else if code.starts-with("ОПК") { 1 }
    else { 2 }
  })

  pagebreak()
heading("Перечень компетенций, которыми должны овладеть обучающиеся в результате освоения образовательной программы
", level: 2)

[Выпускник по направлению #direction (профиль) #program_name в соответствии с данной образовательной программой должен обладать следующими компетенциями]

// Таблица УК и ОПК
[===  Универсальные и общепрофессиональные компетенции]
table(
  columns: (1fr, 2fr),
  stroke: (x: none, y: 0.25pt + gray),
    align: left + top,
    row-gutter: (2pt, auto),
    align(center)[#text(size: 9pt)[компетенция]], 
    align(center)[#text(size: 9pt)[индикатор]],
  ..create_merged_table(uk_opk_data)
)

v(1em)

// Таблица ПК
[=== Профессиональные компетенции]
table(
  columns: (1fr, 1.5fr, 0.5fr),
stroke: (x: none, y: 0.25pt + gray),
    align: left + top,
    row-gutter: (2pt, auto),
    align(center)[#text(size: 9pt)[компетенция]], 
    align(center)[#text(size: 9pt)[индикатор]],
    align(center)[#text(size: 9pt)[основание]],
  ..create_pk_table(pk_data)
)
/*
Совокупность компетенций, установленных программой #level, обеспечивает выпускнику способность осуществлять профессиональную деятельность не менее чем в одной сфере и решать профессиональные задачи не менее чем одного типа.#v(0.5em)
Результаты обучения по дисциплинам (модулям) и практикам соотнесены с установленными в программе #level индикаторами достижения компетенций. #v(0.5em)
Совокупность запланированных результатов обучения по дисциплинам (модулям) и практикам обеспечивает формирование у выпускника всех компетенций, установленных программой #level.

*/
pagebreak()
heading("Требования по подготовке к процедуре выполнения и защиты выпускной квалификационной работы (ВКР)")
[
Подготовка к процедуре защиты и защита выпускной квалификационной работы предполагает наличие у обучающегося умений и навыков проводить самостоятельное законченное исследование на заданную тему, свидетельствующее об усвоении теоретических знаний и практических навыков, позволяющих решать профессиональные задачи, соответствующие требованиям Федерального государственного образовательного стандарта высшего образования по направлению подготовки.
#v(0.5em)
Выпускная квалификационная работа выполняется в виде #if qualification == "магистр" [магистерской диссертации] else if qualification == "специалист" [дипломной работы] else [бакалаврской выпускной квалификационной работы].
]

heading("Рекомендации по подготовке и оформлению ВКР")

heading("Общие требования к содержанию и оформлению ВКР", level: 2)

[Выпускная квалификационная работа должна включать:
- титульный лист
- содержание (оглавление)
- введение
- основную часть, состоящую из глав (разделов), которые разбиваются на подразделы (параграфы)
- заключение, включающее краткое изложение основных результатов работы, выводы, обобщенные рекомендации и возможные перспективы дальнейшего изучения темы
- список источников и литературы
- приложения (при необходимости)

#v(0.5em) Основными требованиями к выпускной квалификационной работе являются:
- четкость и логическая последовательность изложения материала
- краткость и точность формулировок, исключающая возможность неоднозначного их толкования
- конкретность изложения полученных результатов, их анализа и теоретических положений
- обоснованность выводов, рекомендаций и предложений
#v(0.5em) Минимальный объем выпускной квалификационной работы (без приложений) устанавливается в объеме не менее 4000 слов.

#v(0.5em) Выпускная квалификационная работа печатается через 1,5 интервала шрифтом Times New Roman, размер шрифта - 14 пт. 

#v(0.5em)  Библиографические ссылки в виде подстрочных примечаний оформляются в соответствии с ГОСТ Р 7.0.5-2008 «Библиографическая ссылка. Общие требования и правила составления», нумеруются арабскими цифрами в пределах страницы.

#v(0.5em)  Список источников и литературы оформляется в соответствии с ГОСТ 7.1-2003 «Библиографическая запись. Библиографическое описание. Общие требования и правила составления».

#v(0.5em) Если выпускная квалификационная работа выполняется на иностранном языке, то готовятся текст дипломной работы на иностранном языке и реферат работы на русском языке (не превышающий 50% от объема выпускной квалификационной работы).
]

heading("Оценочные материалы для ВКР", level: 2)

heading("Описание показателей, критериев и шкалы оценивания", level:  3)
[Члены ГЭК оценивают ВКР, исходя из степени раскрытия темы, самостоятельности и
глубины изучения проблемы, обоснованности выводов и предложений, а также исходя из
уровня сформированности компетенций выпускника, который оценивают руководитель,
рецензент и сами члены ГЭК. #v(0.5em)Результаты определяются оценками «отлично», «хорошо», «удовлетворительно»,
«неудовлетворительно».
#pagebreak()
Критерии оценки ВКР:
#v(0.5em)
#table(
  columns: (1fr, 4fr),
      stroke: (x: none, y: 0.25pt + gray),
      row-gutter: (2pt, auto),
  inset: 8pt,
  
    align(center)[#text(size: 9pt)[оценка]], 
    align(center)[#text(size: 9pt)[критерии]],
  
  [«Отлично»], [
    - доклад структурирован, раскрывает причины выбора темы и ее актуальность, цель, задачи, предмет, объект исследования, логику получения каждого вывода; в заключительной части доклада показаны перспективы и задачи дальнейшего исследования данной темы, освещены вопросы практического применения и внедрения результатов исследования в практику;
    - ВКР выполнена в соответствии с целевой установкой, отвечает предъявляемым требованиям и оформлена в соответствии со стандартом;
    - представленный демонстрационный материал высокого качества в части оформления и полностью соответствует содержанию ВКР и доклада;
    - ответы на вопросы членов ГЭК показывают глубокое знание исследуемой проблемы, подкрепляются ссылками на соответствующие нормативно-правовые акты, литературные источники, выводами из ВКР, демонстрируют самостоятельность и глубину изучения проблемы студентом;
    - выводы в отзыве руководителя и в рецензии на ВКР не содержат замечаний.
  ],
  
  [«Хорошо»], [
    - доклад структурирован, допускаются одна-две неточности при раскрытии причин выбора и актуальности темы, цели, задач, предмета, объекта исследования, но эти неточности устраняются при ответах на дополнительные уточняющие вопросы;
    - ВКР выполнена в соответствии с целевой установкой, отвечает предъявляемым требованиям и оформлена в соответствии со стандартом;
    - представленный демонстрационный материал хорошего качества в части оформления и полностью соответствует содержанию ВКР и доклада;
    - ответы на вопросы членов ГЭК показывают хорошее владение материалом, нормативно-правовыми актами действующего законодательства, подкрепляются выводами из ВКР, показывают самостоятельность и глубину изучения проблемы студентом;
    - выводы в отзыве руководителя и в рецензии на ВКР без замечаний или содержат незначительные замечания, которые не влияют на полноту раскрытия темы.
  ],
  
  [«Удовлетворительно»], [
    - доклад структурирован, допускаются неточности при раскрытии причин выбора и актуальности темы, цели, задач, предмета, объекта исследования, но эти неточности устраняются в ответах на дополнительные вопросы;
    - ВКР выполнена в соответствии с целевой установкой, но не в полной мере отвечает предъявляемым требованиям;
    - представленный демонстрационный материал удовлетворительного качества в части оформления и в целом соответствует содержанию ВКР и доклада;
    - ответы на вопросы членов ГЭК носят не достаточно полный и аргументированный характер, не раскрывают до конца сущности вопроса, слабо подкрепляются выводами из ВКР, показывают недостаточную самостоятельность и глубину изучения проблемы студентом;
    - выводы в отзыве руководителя и в рецензии на ВКР содержат замечания, указывают на недостатки, которые не позволили студенту в полной мере раскрыть тему.
  ],
  
  [«Неудовлетворительно»], [
    - доклад не достаточно структурирован, допускаются существенные неточности при раскрытии причин выбора и актуальности темы, цели, задач, предмета, объекта исследования, эти неточности не устраняются в ответах на дополнительные вопросы, использованы недействующие нормативно-правовые акты;
    - ВКР не отвечает предъявляемым требованиям;
    - представленный демонстрационный материал низкого качества в части оформления и не соответствует содержанию ВКР и доклада;
    - ответы на вопросы членов ГЭК носят неполный характер, не раскрывают сущности вопроса, не подкрепляются выводами и расчетами из ВКР, показывают недостаточную самостоятельность и глубину изучения проблемы студентом;
    - выводы в отзыве руководителя и в рецензии на ВКР содержат существенные замечания, указывают на недостатки, которые не позволили студенту раскрыть тему.
  ],
)]

heading("Примерная тематика ВКР", level: 3)
[- Проектирование аграрного исследовательского и образовательного комплекса в г.Зерноград, Ростовская область
- Реконструкция и функциональная трансформация здания
- Рекреационный комплекс
- Тотальная реконструкция жилого квартала
- Реновация застройки и здания бывшего завода
- Реконструкция и приспособление объектов исторической застройки прибрежной территории
- Реконструкция и приспособление объектов центральной территории креативного кластера
]

heading("Методические материалы, определяющие процедуры оценивания", level: 3)

[ Защита выпускной квалификационной работы проводится в установленное время на заседании государственной экзаменационной комиссии. Кроме членов комиссии на защите должен присутствовать руководитель выпускной квалификационной работы.
  #v(0.5em)
  В аудитории, в которой проходит защита, должны находиться выпускные квалификационные работы, отзывы научных руководителей и рецензии, оформленные в соответствии с требованиями.
  #v(0.5em)
  Перед началом защиты председатель государственной экзаменационной комиссии знакомит студентов с порядком проведения защиты, секретарь комиссии представляет студента и тему его выпускной квалификационной работы.
  #v(0.5em)
  Защита начинается с доклада студента по теме выпускной квалификационной работы, на который отводится до 15 минут.
  #v(0.5em)
  После завершения доклада члены государственной экзаменационной комиссии задают студенту вопросы как непосредственно связанные с темой выпускной квалификационной работы, так и с проблемой, решению которой посвящена работа. При ответах на вопросы студент имеет право пользоваться своей работой.
  #v(0.5em)
  После ответов студента на вопросы слово предоставляется руководителю.  Руководитель дает характеристику выпускной квалификационной работы, степени подготовленности обучающегося к самостоятельному решению профессиональных задач в избранной области профессиональной деятельности.
  #v(0.5em)
  После выступления руководителя слово предоставляется рецензенту. В конце выступления рецензент дает свою оценку работе.
  #v(0.5em)
  В случае отсутствия руководителя и/или рецензента председатель государственной экзаменационной комиссии зачитывает отзыв и/или рецензию на выпускную квалификационную работу.
  #v(0.5em)
  После окончания дискуссии студенту предоставляется заключительное слово. В своем заключительном слове студент должен ответить на замечания рецензента.
  #v(0.5em)
  Общее время защиты выпускной квалификационной работы с учетом дополнительных вопросов членов государственной экзаменационной комиссии должно составлять не более 30 минут.
  #v(0.5em)
  Защита выпускных квалификационных работ оформляется протоколом. Протоколы подписываются членами государственной экзаменационной комиссии и председателем государственной экзаменационной комиссии.
]

pagebreak()

heading("Учебно-методическое и информационное обеспечение государственной итоговой аттестации", level: 1)

 v(1em)
 heading("Основная литература", level: 2)
literature_base

 v(1em)
 heading("Дополнительная литература", level: 2)
literature_add

 v(1em)
 heading("Перечень ресурсов информационно-коммуникационной сети «Интернет", level: 2)
internet


heading("Материально-техническое обеспечение итоговой аттестации", level: 1)
mats_tech

}