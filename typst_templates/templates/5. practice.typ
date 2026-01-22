#import "0. useful_functions.typ": *
#import "0. method_recommend.typ": *
#import "0. mats_techs.typ": *

#let practice(
  // общая информация
  var01: [],
  var_cycle : [],// 
  doc
  ) = {  

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
    discipline_sem4
  )

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

  
 set par(justify: true, spacing: 0.25em)
  set block(spacing: 0.25em)
  
  set heading(numbering: "1.")
  show heading.where(level: 1): set text(size: 11pt, weight: "bold", hyphenate: false)
  show heading.where(level: 1): set align(left)
  
  show heading.where(level: 2): set text(size: 11pt, weight: "regular")
  show heading.where(level: 2): set align(left)

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
        Ученым советом АНО ВО "Универсальный Университет"  \ в составе образовательной программы высшего образования#new_edition_text
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
      *Рабочая программа практики*
    ] \
     #upper[
      #discipline_code #discipline
    ]
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
  author
  outline()

  pagebreak()

   // стр 3 

 heading[Цели и задачи практики]
  

  heading("Цель практики", level: 2)
  v(0.5em)
  [Практическая подготовка — форма организации образовательной деятельности при освоении образовательной программы в условиях выполнения обучающимися определенных видов работ, связанных с будущей профессиональной деятельностью и направленных на формирование, закрепление, развитие практических навыков и компетенций по профилю соответствующей образовательной программы.
  #v(0.5em)
  Практическая подготовка при проведении практики организуется путем непосредственного выполнения обучающимися определенных видов работ, связанных с будущей профессиональной деятельностью.
]
  

  heading("Задачи практики", level: 2)
  let tasks_list = tasks.split(";")
  for task in tasks_list [
  - #task.trim()]
  heading[Вид и тип практики]

   create-practice-table(module_desc, var_cycle)

  v(2em)
  heading[Место практики в структуре образовательной программы]
  v(1em)
  [Практика включена в учебный план по направлению #direction, профиль "#program_name", входит в #disc_type учебного плана, и изучается в 
  #conclusion_semesters.join(", ") семестре.]

  pagebreak()

  // стр 4 

  heading[Перечень планируемых результатов обучения, соотнесенных с планируемыми результатами освоения образовательной программы]
  
  // Полное использование:
let matching = csv("../csv/matching.csv")
let indicators_merge = csv("../csv/indicators_merge.csv")
let comp_data = get-discipline-competences(matching, discipline_code)
let prepared = prepare-competence-data-with-outcomes(comp_data, indicators_merge)

// Таблица УК/ОПК
if prepared.uk_opk.len() > 0 [
  == Универсальные и общепрофессиональные компетенции
  
  #table(
    columns: (1fr, 1fr, 2fr),
    stroke: (x: none, y: 0.25pt + gray),
    align: left + top,
    row-gutter: (2pt, auto),
    align(center)[#text(size: 9pt)[компетенция]], 
    align(center)[#text(size: 9pt)[индикатор]], 
    align(center)[#text(size: 9pt)[планируемые результаты]],
    ..create-uk-opk-table(prepared.uk_opk)
  )
]

// Таблица ПК
if prepared.pk.len() > 0 [
  == Профессиональные компетенции
  
  #table(
    columns: (1fr, 1fr, 2fr),
    stroke: (x: none, y: 0.25pt + gray),
    align: left + top,
    row-gutter: (2pt, auto),
      align(center)[#text(size: 9pt)[компетенция]], 
    align(center)[#text(size: 9pt)[индикатор]], 
    align(center)[#text(size: 9pt)[планируемые результаты обучения]],
    ..create-pk-table(prepared.pk)
  )
]
  heading[Объем практики и виды работы]
 create-all-workload-tables(module_desc, var_cycle)

  pagebreak()

  // стр 5

  heading[Содержание практики]

 heading("Этапы прохождения практики", level: 2)

create-discipline-content(topics, topics_abstract)

 pagebreak()

 // стр 8 

 heading[Учебно-методическое и информационное обеспечение практики]

 v(1em)
 heading("Основная литература", level: 2)
literature_base

 v(1em)
 heading("Дополнительная литература", level: 2)
literature_add

 v(1em)
 heading("Перечень ресурсов информационно-коммуникационной сети «Интернет", level: 2)
internet

 pagebreak()

 // стр 9 

 heading[Материально-техническое обеспечение практики]

 mats_tech

  pagebreak()
  
  heading[Методические рекомендации по прохождению практики]

  
methods

}
