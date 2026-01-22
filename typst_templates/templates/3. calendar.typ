#import "0. useful_functions.typ": *
#let calendar(
  // общая информация
  var01: [], // 
  doc
  ) = {

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
    [#align(right)[#upper[*утвержден*] \
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
      *Календарный учебный график*
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
    [образовательный стандарт:], [ФГОС ВО по направлению подготовки #direction (#level), приказ Министерства образования и науки России от #fgos_date № #fgos_number],
    [форма обучения:], [#form_of_study],
    [срок обучения (в годах): ], [#duration_years],
    [год набора:], [#start_year]
  )

  align(bottom + center)[
    Москва, 2025
  ]

}