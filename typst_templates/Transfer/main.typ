// logo & csv
#let logo = image("pics/uu_logo_black.png")
#let data = csv("csv/Transfer - List.csv", delimiter: ";")

// minutes
#let info = csv("csv/КМИ-25-420305.csv")
#let filtered-data = data.filter(row => row.at(0) == "КМИ-25-420305")
#let year = "2025/2026 учебный год"

// page settings
#set page(paper: "a4")
#set text(size: 11pt, lang: "ru", font: "Times New Roman")
#set par(justify: true, spacing: 0.25em)
#set block(spacing: 0.25em)
#set heading(numbering: "1.")
#show heading.where(level: 1): set text(size: 11pt, weight: "bold")
#show heading.where(level: 1): set align(center)
#show heading.where(level: 2): set text(size: 11pt, weight: "regular")
#show heading.where(level: 2): set align(left)

// page 
#set text(size: 10pt, lang: "ru", font: "Times New Roman")
#set par(justify: false)
#table(
  columns: (20fr, 10fr),
  stroke: none,
  [
    #v(0.75em)
    #text(font: "Times New Roman", weight: 300)[
      #upper[автономная некоммерческая организация \ высшего образования]
    ]
    #v(0.75em)
    #text(font: "Times New Roman", weight: 700)[
      #upper["универсальный университет"]
    ]
  ], 
  [#logo]
)
#set text(size: 11pt, lang: "ru", font: "Times New Roman")
#set par(justify: true, spacing: 0.25em)
#v(2em)
#align(center)[
  #upper[*протокол № #filtered-data.at(0).at(0) \ заседания аттестационной комиссии*]
  #v(0.5em)
  Факультет бизнеса и маркетинга
]
#v(1em)
#table(
  columns: (10fr, 10fr),
  stroke: none,
  [#align(left)[г. Москва]],
  [#align(right)[#filtered-data.at(0).at(1)]]
)
#v(2em)
*Хуй*
#v(0.5em)
- Бислер Матвей Александрович, дизайнер образовательных программ, департамент академического качества АНО ВО "Универсальный университет" (председатель комиссии)
#v(0.5em)
- Ковшова Наталья Владимировна, руководитель учебного отдела программ высшего образования АНО ВО "Универсальный университет" (член комиссии)
#v(0.5em)
- Мищенко Анна Александровна, менеджер по работе с абитуриентами АНО ВО "Универсальный университет" (член комиссии)
#v(2em)
*Повестка дня*
#v(0.5em)
Перевод обучающегося на #filtered-data.at(0).at(12)-й семестр направления подготовки #filtered-data.at(0).at(10), профиль "#filtered-data.at(0).at(11)"; очная форма обучения; обучение #filtered-data.at(0).at(8)
#v(1.5em)
Сведения об обучающемся: 
#v(0.5em)
#table(
  columns: (12fr, 20fr),
  stroke: (0.5pt + rgb(192,192,192)),
  [фамилия, имя, отчество], [#filtered-data.at(0).at(2)],
  [образовательная организация], [#filtered-data.at(0).at(3)],
  [направление], [#filtered-data.at(0).at(4)],
  [профиль], [#filtered-data.at(0).at(5)],
  [курс обучения], [#filtered-data.at(0).at(6) курс],
  [форма обучения], [#filtered-data.at(0).at(7)]
)
#v(0.5em)
#v(2em)
*Слушали*
#v(0.5em)
Председателя аттестационной комиссии о возможности перевода обучающегося на заявленные направление подготовки, направленность (профиль), курс, семестр, форму обучения. \ 
Обучающийся представил для рассмотрения аттестационной комиссией следующие документы:
- Заявление о переводе от #filtered-data.at(0).at(15);
- Справку об обучении (периоде обучения) Nº #filtered-data.at(0).at(14)
#pagebreak()
*Постановили*
#v(0.5em)
- Перезачесть результаты обучения по следующим дисциплинам и практикам: 
#v(0.5em)
#set text(size: 5.5pt)
#set par(justify: false)

#let passed-info = info.filter(row => row.at(9) == "Перезачтено")

#table(
  columns: 11,
  stroke: (0.5pt + rgb(192,192,192)),
  ..passed-info.flatten()
)
#set text(size: 11pt)
#set par(justify: true)
#v(1em)
#v(0.5em)
#set text(size: 5.5pt)
#set par(justify: false)

#let unpassed-info = info.filter(row => row.at(9) == "Досдача")

#table(
  columns: (3.1fr, 7.9fr, 0.8fr, 0.8fr, 1.1fr, 4fr, 1fr, 1fr, 2.7fr, 2.4fr, 1.75fr),
  stroke: (0.5pt + rgb(192,192,192)),
  ..unpassed-info.flatten()
)
#set text(size: 11pt)
#set par(justify: true)
#v(0.5em)
- Рекомендовать обучающегося к переводу на направление подготовки #filtered-data.at(0).at(10), профиль «#filtered-data.at(0).at(11)», на #filtered-data.at(0).at(12)-й семестр
- Сформировать обучающемуся индивидуальный учебный план
- Установить академическую разницу в размере #filtered-data.at(0).at(9) зачетных единиц
#pagebreak()
#align(bottom + left)[
  #table(
  columns: (1fr, 2fr, 2fr),
  stroke: none,
  [ Председатель\ комиссии \ 
],[#align(bottom)[#line(stroke: 0.03em, length: 100%)]],[#align(right)[#align(bottom)[Матвей Александрович Бислер]]]
)
  #v(3em)
  #table(
  columns: (1fr, 2fr, 2fr),
  stroke: none,
  [ Члены комиссии \ 
],[#align(bottom)[#line(stroke: 0.03em, length: 100%)]],[#align(right)[#align(bottom)[]]]
)
#v(3em)
  #table(
  columns: (1fr, 2fr, 2fr),
  stroke: none,
  [ Члены комиссии \ 
],[#align(bottom)[#line(stroke: 0.03em, length: 100%)]],[#align(right)[#align(bottom)[]]]
)
  #v(3em)
  _С протоколом заседания аттестационной комиссии ознакомлен(-а)_ \
  #v(4em)
  #table(
  columns: (1fr, 2fr, 2fr),
  stroke: none,
  [Обучающийся \ 
],[#align(bottom)[#line(stroke: 0.03em, length: 100%)]],[#align(right)[#align(bottom)[#filtered-data.at(0).at(2)]]]
)
]
