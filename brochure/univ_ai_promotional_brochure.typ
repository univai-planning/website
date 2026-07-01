// Univ.AI promotional brochure.
// Source context:
// - Current site: https://univ.ai/ plus local index.qmd, methods.qmd, verticals.qmd.
// - CricsDB post: https://rahuldave.com/posts/cricsdb/index.html.
// - DeeBase post: https://rahuldave.com/posts/deebase/index.html.
// - ExtractoPrimo: /Users/rahul/Credcore/ExtractoPrimo.
// - meai: /Users/rahul/Credcore/meai.
// - DAIS / legal redlining SOW: /Users/rahul/Downloads/UnivAI-Agentic_AI_for_Contract_Redlining_-_Clean_Copy_-_7-11-25.docx.pdf.
// - Education archive: /Users/rahul/Courses/OrgsCourses/welcome.univ.ai/index.markdown
//   and /Users/rahul/Courses/OrgsCourses/Teacher/univ-ai-courses/*/README.md.

#let navy = rgb("#10263a")
#let blue = rgb("#0f5fa8")
#let teal = rgb("#0b6e69")
#let coral = rgb("#d45d4c")
#let gold = rgb("#d2a72a")
#let cream = rgb("#f6f1e7")
#let paper = rgb("#fffdf8")
#let ink = rgb("#18202a")
#let muted = rgb("#59636f")
#let line-color = rgb("#d9d0c0")

#set document(title: "Univ.AI Promotional Brochure", author: "Univ.AI")
#set page(
  width: 8.5in,
  height: 11in,
  margin: (x: 0.34in, top: 0.34in, bottom: 0.44in),
  fill: cream,
  footer-descent: 22%,
)
#set text(font: "Helvetica", size: 8.6pt, fill: ink)
#set par(justify: false, leading: 0.53em)
#show link: it => text(fill: blue)[#it]

#let gap = v(8pt)
#let small-gap = v(4pt)

#let kicker(body) = text(size: 7.35pt, weight: "bold", fill: coral, tracking: 0.8pt)[#body]

#let big-title(body) = text(size: 27pt, weight: "bold", fill: navy)[#body]

#let page-title(body) = text(size: 20pt, weight: "bold", fill: navy)[#body]

#let subhead(body) = text(size: 10.6pt, fill: muted)[#body]

#let card(body, fill: paper, stroke: line-color, inset: 9pt) = rect(
  width: 100%,
  radius: 7pt,
  fill: fill,
  stroke: 0.7pt + stroke,
  inset: inset,
)[#body]

#let dark-card(body, inset: 12pt) = rect(
  width: 100%,
  radius: 7pt,
  fill: navy,
  inset: inset,
)[#body]

#let stat(value, label, fill: teal) = rect(
  radius: 6pt,
  fill: fill.lighten(82%),
  stroke: 0.5pt + fill.lighten(35%),
  inset: (x: 7pt, y: 6pt),
)[
  #text(size: 17pt, weight: "bold", fill: fill)[#value]
  #v(1pt)
  #text(size: 7.4pt, fill: ink)[#label]
]

#let label(body, fill: coral) = rect(
  radius: 999pt,
  fill: fill.lighten(83%),
  stroke: 0.45pt + fill.lighten(38%),
  inset: (x: 7pt, y: 3pt),
)[#text(size: 7.15pt, weight: "bold", fill: fill.darken(10%))[#body]]

#let image-frame(path, h: 2.55in) = rect(
  width: 100%,
  radius: 7pt,
  fill: paper,
  stroke: 0.7pt + line-color,
  inset: 0pt,
)[#image(path, width: 100%, height: h, fit: "cover")]

#let contain-frame(path, h: 2.55in) = rect(
  width: 100%,
  radius: 7pt,
  fill: paper,
  stroke: 0.7pt + line-color,
  inset: 0pt,
)[#image(path, width: 100%, height: h, fit: "contain")]

#let section-rule() = line(length: 100%, stroke: 0.7pt + line-color)

#let footer(body) = align(center)[
  #text(size: 8.2pt, fill: muted)[#body]
]

#let mini(title, body, fill: paper) = card(inset: 8pt, fill: fill)[
  #text(size: 11.4pt, weight: "bold", fill: navy)[#title]
  #v(3pt)
  #body
]

#let tight-card(tag, title, body, fill: teal) = card(inset: 6.5pt)[
  #label(fill: fill)[#tag]
  #v(3pt)
  #text(size: 10.6pt, weight: "bold", fill: navy)[#title]
  #v(2pt)
  #text(size: 7.55pt)[#body]
]

// Page 1: consulting overview, agentic software proof, healthcare fraud.
#set page(footer: footer[univ.ai | AI consulting, engineering, education, and applied machine learning])

#grid(
  columns: (1fr, 1fr),
  gutter: 18pt,
  [
    #image("assets/brochure/univai-logo-blue.png", width: 1.45in)
    #v(10pt)
    #kicker[APPLIED AI CONSULTING]
    #v(5pt)
    #big-title[AI systems for messy, high-value business problems.]
    #v(6pt)
    #subhead[
      Univ.AI combines machine-learning depth, software engineering, and
      business translation to build systems that survive contact with real
      workflows.
    ]
    #v(10pt)
    #dark-card(inset: 11pt)[
      #text(size: 14pt, weight: "bold", fill: paper)[From model idea to working operation]
      #v(4pt)
      #text(fill: paper.lighten(2%))[
        We define the right problem, design the model and data path, translate
        technical metrics into business KPIs, and deploy usable workflows with
        the people who will actually run them.
      ]
    ]
  ],
  [
    #image-frame("assets/brochure/healthcare-fraud-prevention.png", h: 3.45in)
    #v(7pt)
    #dark-card(inset: 10pt)[
      #text(size: 12.5pt, weight: "bold", fill: paper)[Where Univ.AI fits]
      #v(5pt)
      #grid(
        columns: (1fr, 1fr),
        gutter: 7pt,
        [#label[Custom AI]],
        [#label(fill: teal)[Agentic systems]],
        [#label(fill: gold)[AI research]],
        [#label(fill: teal)[Deployment]],
      )
      #v(7pt)
      #text(fill: paper)[Healthcare, finance, law, pharma, energy, and other technical domains where the model has to become an operational system.]
    ]
  ],
)

#v(8pt)

#grid(
  columns: (1.08fr, 0.92fr),
  gutter: 14pt,
  [
    #contain-frame("assets/brochure/extractoprimo-dashboard.png", h: 2.35in)
    #v(5pt)
    #card(inset: 8pt)[
      #label(fill: teal)[AGENTIC SOFTWARE]
      #v(5pt)
      #text(size: 12.8pt, weight: "bold", fill: navy)[ExtractoPrimo: evaluation loop for agents]
      #v(4pt)
      ExtractoPrimo benchmarks model, prompt, setup, and agent combinations
      across documents. It tracks runs, prompt versions, judges, human review,
      composite scores, Elo comparisons, MLflow traces, and next actions for
      iterative extraction quality.
    ]
  ],
  [
    #card(inset: 8pt)[
      #label[HEALTHCARE INSURANCE]
      #v(5pt)
      #text(size: 12.8pt, weight: "bold", fill: navy)[Fraud prevention for claims operations]
      #v(4pt)
      For a major healthcare insurance company, Univ.AI's work focused on
      surfacing suspicious claim patterns, designing review-ready analytics,
      and supporting investigators with model outputs that fit real claims
      workflows.
      #v(6pt)
      #grid(
        columns: (1fr, 1fr),
        gutter: 6pt,
        [#label(fill: teal)[Claims anomalies]],
        [#label(fill: gold)[Audit workflows]],
      )
    ]
    #v(7pt)
    #contain-frame("assets/brochure/extractoprimo-secondary.png", h: 1.62in)
  ],
)

#pagebreak()

// Page 2: finance, legal, oil.
#set page(footer: footer[univ.ai | consulting for finance, legal, healthcare, energy, and research teams])

#kicker[FINANCE / HEALTH / LEGAL / OIL]
#v(5pt)
#page-title[Applied AI for regulated, technical, and document work.]
#v(5pt)
#subhead[
  Univ.AI pairs modeling skill with domain constraints: audit trails, document
  citations, physical plausibility, deployment inside enterprise systems, and
  human review where it matters.
]

#v(9pt)

#grid(
  columns: (1fr, 1fr),
  gutter: 14pt,
  [
    #card(inset: 9pt, fill: rgb("#fbf7ef"))[
      #label(fill: gold)[FINANCE]
      #v(5pt)
      #text(size: 13pt, weight: "bold", fill: navy)[Risk, recommendations, and operating models]
      #v(4pt)
      We build data and model workflows for high-stakes decisions: risk
      scoring, anomaly detection, recommender systems, financial document
      extraction, model monitoring, and stakeholder-ready dashboards.
      #v(7pt)
      #grid(
        columns: (1fr, 1fr),
        gutter: 6pt,
        [#label(fill: teal)[Risk analytics]],
        [#label(fill: gold)[Decision support]],
      )
    ]
    #v(8pt)
    #card(inset: 9pt)[
      #label[LEGAL / CREDIT]
      #v(5pt)
      #text(size: 13pt, weight: "bold", fill: navy)[Document intelligence with citations]
      #v(4pt)
      For insurance, credit and legal workflows, Univ.AI develops systems that search,
      reason over, and cite long contracts and loan documents, turning dense
      PDFs into structured, reviewable answers.
      #v(7pt)
      #grid(
        columns: (1fr, 1fr),
        gutter: 6pt,
        [#label(fill: teal)[Contract QA]],
        [#label(fill: gold)[Cited answers]],
      )
    ]
    #v(20pt)
    #card(inset: 9pt, fill: teal.lighten(84%), stroke: teal.lighten(35%))[
      #text(size: 12.2pt, weight: "bold", fill: teal.darken(12%))[Implementation spine]
      #v(3pt)
      #text(size: 8.25pt)[Experiment tracking, data analysis and drift detection, model monitoring, continual learning, source citations, deployment handoffs, and documentation that client teams can keep using.]
    ]
  ],
  [
    #image-frame("assets/brochure/oilfield-reservoir-modeling.png", h: 3.55in)
    #v(6pt)
    #card(inset: 9pt)[
      #label(fill: teal)[ENERGY / OILFIELD]
      #v(5pt)
      #text(size: 13pt, weight: "bold", fill: navy)[CNN approximations for reservoir physics]
      #v(4pt)
      For an oil company, Univ.AI used convolutional neural networks to
      approximate Darcy-equation behavior: estimating pressure and water
      saturation, and therefore oil saturation, across rock strata from
      reservoir inputs.
      #v(7pt)
      #grid(
        columns: (1fr, 1fr),
        gutter: 6pt,
        [#label(fill: teal)[Pressure fields]],
        [#label(fill: gold)[Water/oil saturation]],
      )
    ]
  ],
)

#v(10pt)

#dark-card(inset: 10pt)[
  #grid(
    columns: (1fr, 1fr, 1fr),
    gutter: 10pt,
    [
      #text(size: 12pt, weight: "bold", fill: paper)[Compliant by design]
      #v(3pt)
      #text(size: 8.1pt, fill: paper)[Auditability, privacy, access control, and review workflows are part of the product design.]
    ],
    [
      #text(size: 12pt, weight: "bold", fill: paper)[Technically thorough]
      #v(3pt)
      #text(size: 8.1pt, fill: paper)[We work with model architecture, data strategy, validation, and deployment details.]
    ],
    [
      #text(size: 12pt, weight: "bold", fill: paper)[Production level]
      #v(3pt)
      #text(size: 8.1pt, fill: paper)[The output is code, tools, dashboards, documentation, and a team that can use them.]
    ],
  )
]

#pagebreak()

// Page 3: education and software portfolio.
#set page(footer: footer[univ.ai | education heritage plus production software delivery])

#kicker[EDUCATION + SOFTWARE]
#v(5pt)
#page-title[We build the tools and teach the teams.]
#v(5pt)
#subhead[
  Univ.AI now runs corporate courses and workshops. Before that, Univ.AI was a
  full AI school with a long-form curriculum, capstones, and project-based
  learning.
]

#v(7pt)

#grid(
  columns: (1fr, 1fr),
  gutter: 12pt,
  [
    #contain-frame("assets/brochure/univai-course-map.png", h: 3.05in)
  ],
  [
    #contain-frame("assets/brochure/cricsdb-home.png", h: 3.05in)
  ],
)

#v(7pt)

#grid(
  columns: (1fr, 1fr),
  gutter: 8pt,
  [
    #tight-card(fill: gold)[CORPORATE COURSES][Training for teams][Workshops for engineering, analytics, product, and leadership teams adopting AI.]
  ],
  [
    #tight-card(fill: coral)[FORMER FULL AI SCHOOL][Capability curriculum][A 48-week Master AI path plus capstone across foundations, data science, NLP, generative AI, RL, Bayesian statistics, and causal inference.]
  ],
  [
    #tight-card(fill: teal)[ANALYTICS DATABASE][CricsDB][FastAPI, React, Semiotic, and SQLite turning ball-by-ball cricket data into deep-linked team, player, matchup, and scorecard views.]
  ],
  [
    #tight-card(fill: teal)[EASY DATABASE ACCESS][DeeBase][Async SQLAlchemy with dataclass tables, FK navigation, full-text search, migrations, and FastAPI CRUD routers.]
  ],
  [
    #tight-card(fill: teal)[AGENTIC SOFTWARE][MEAI][FastAPI and Meilisearch document analysis for XML/PDF uploads, credit-loan prompts, agentic retrieval, structured answers, and source-region citations.]
  ],
  [
    #tight-card(fill: teal)[AGENTIC SOFTWARE][DAIS][Agentic contract review for legal teams: clause classification, prompt-tuned redliner and judge LLMs, editable Word redlines, rationale, and reviewer signoff.]
  ],
)

#pagebreak()

// Page 4: method and CTA.
#set page(footer: footer[univ.ai | rahuldave\@univ.ai])

#kicker[OUR METHOD]
#v(5pt)
#page-title[A practical path from problem to production.]
#v(5pt)
#subhead[
  Bring Univ.AI a data-rich business problem, a model that needs to become a
  product, or a team that needs to level up.
]

#v(9pt)

#page-title[Our method]
#v(7pt)

#grid(
  columns: (1fr, 1fr),
  gutter: 10pt,
  [
    #card(inset: 9pt)[
      #label[1. PROBLEM DEFINITION]
      #v(5pt)
      #text(size: 12.5pt, weight: "bold", fill: navy)[Start with business reality]
      #v(4pt)
      Identify pain points, define success metrics aligned with business KPIs,
      map existing processes and systems, and set scope and timeline.
    ]
  ],
  [
    #card(inset: 9pt)[
      #label(fill: teal)[2. MODEL CONSTRUCTION]
      #v(5pt)
      #text(size: 12.5pt, weight: "bold", fill: navy)[Build the model and data path]
      #v(4pt)
      Develop data strategy, model architecture, training and validation,
      inference design, and performance optimization.
    ]
  ],
  [
    #card(inset: 9pt)[
      #label(fill: gold)[3. BUSINESS TRANSLATION]
      #v(5pt)
      #text(size: 12.5pt, weight: "bold", fill: navy)[Make model metrics meaningful]
      #v(4pt)
      Translate model behavior into cost, risk, quality, growth, or service
      metrics. Design experiments and capture outcomes from real users.
    ]
  ],
  [
    #card(inset: 9pt)[
      #label(fill: blue)[4. DEPLOYMENT]
      #v(5pt)
      #text(size: 12.5pt, weight: "bold", fill: navy)[Integrate, monitor, and train]
      #v(4pt)
      Support system integration, inference optimization, monitoring, team
      training, customer data collection, and ongoing maintenance.
    ]
  ],
)

#v(10pt)

#grid(
  columns: (1fr, 1fr, 1fr),
  gutter: 9pt,
  [
    #card(inset: 8pt, fill: rgb("#fbf7ef"))[
      #text(size: 12pt, weight: "bold", fill: navy)[Engagements can include]
      #v(4pt)
      Custom AI builds, research spikes, prototypes, production hardening, and
      team enablement.
    ]
  ],
  [
    #card(inset: 8pt, fill: rgb("#fbf7ef"))[
      #text(size: 12pt, weight: "bold", fill: navy)[Typical outputs]
      #v(4pt)
      Code, APIs, dashboards, experiment traces, model docs, workflows, and
      training material.
    ]
  ],
  [
    #card(inset: 8pt, fill: rgb("#fbf7ef"))[
      #text(size: 12pt, weight: "bold", fill: navy)[Next step]
      #v(4pt)
      Email #text(weight: "bold", fill: blue)[rahuldave\@univ.ai] with the
      problem, data context, and desired business outcome.
    ]
  ],
)

#v(10pt)

#dark-card(inset: 12pt)[
  #grid(
    columns: (1fr, 0.78fr),
    gutter: 15pt,
    [
      #text(size: 15.5pt, weight: "bold", fill: paper)[Let's turn your AI opportunity into a working system.]
      #v(5pt)
      #text(fill: paper)[We are careful in the project engagements we accept so that we can guarantee their success. For consulting, corporate courses, or even a fast technical scoping conversation, please contact us.]
    ],
    [
      #align(right)[
        #text(size: 9.5pt, fill: paper)[Email]
        #v(3pt)
        #link("mailto:rahuldave@univ.ai")[
          #text(size: 17pt, weight: "bold", fill: paper)[rahuldave\@univ.ai]
        ]
        #v(7pt)
        #text(size: 9.5pt, fill: paper)[Website]
        #v(3pt)
        #link("https://univ.ai")[
          #text(size: 10.6pt, weight: "bold", fill: paper)[https://univ.ai]
        ]
      ]
    ],
  )
]
