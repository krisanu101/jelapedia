# 🗺️ JelaPedia
### AI-powered District Information & Trip Planning Assistant for Bangladesh

JelaPedia is a bilingual (Bangla/English) web application covering all 64 districts of
Bangladesh — facts, comparisons, an offline AI search assistant, a trip planner, and a
trivia quiz, all generated from a single structured dataset.



## 📌 Features

- **District Explorer** — browse all 64 districts by division, search by name, view a
  detail page for each (area, population, famous places, food, rivers)
- **AI Search Assistant** — ask a free-text question ("What is Sylhet famous for?") and
  get an answer via **TF-IDF + cosine similarity** (scikit-learn) — a real NLP technique,
  fully offline, **no API key or internet connection required**
- **Voice input** for the AI assistant, using the browser's built-in Web Speech API
- **Compare** — side-by-side comparison of any two districts
- **Trip Planner** — pick your interests (beach, hills, history, rivers, ...) and get
  matching district suggestions with a reason for each
- **Trivia Quiz** — multiple-choice questions generated on the fly from the dataset
  (largest/smallest district, which division, famous-for matching, etc.)
- **Insights Dashboard** — population/area charts by division (Chart.js), rankings
- **Favorites** — bookmark districts (session-based, no login needed)
- **Printable Fact Sheets** — one-click "Print / Save as PDF" per district
- **REST API** — `/api/districts`, `/api/district/<id>`, `/api/ask?q=...` for other apps
- **Full bilingual UI** — every page, label and district fact switches between
  বাংলা and English instantly



## 🧠 How the "AI" search actually works (no API key needed)

Instead of calling an external LLM (which would need a paid API key you'd have to set
up), JelaPedia builds its own small **TF-IDF search index** over all district data at
startup (`backend/ai_search.py`):

1. Each district's name, description, famous places, food and rivers (in both languages)
   are combined into one text document.
2. `TfidfVectorizer` turns all 64 documents into weighted term vectors.
3. A query is vectorized the same way, and **cosine similarity** finds the closest
   matching district.
4. A direct district-name match (e.g. the query contains "Sylhet" or "সিলেট") is checked
   first and given priority, since that's a stronger signal than TF-IDF similarity over a
   short question full of common words like "what", "is", "for".

This is a legitimate, explainable NLP technique — good to talk about in an interview —
and it means the whole app runs with zero ongoing cost and zero external dependencies.

**Note on tokenizing Bangla text:** Python's built-in `re` module's `\w` does *not*
include Bangla vowel signs (matras) as "word" characters, which silently shatters Bangla
words into single letters with a naive `\b\w+\b` tokenizer. `ai_search.py` uses a
whitespace/punctuation-based tokenizer instead to avoid this — worth mentioning if asked
about Bangla NLP challenges.



## 🗂️ Project Structure

jelapedia/
├── start.bat / start.sh      # (no database, no API key needed)
├── README.md
├── CV_AND_INTERVIEW_GUIDE.md
├── data/
│   └── districts.json        # All 64 districts, bilingual, structured data
├── backend/                  # Flask application
│   ├── app.py                  # All routes
│   ├── ai_search.py             # TF-IDF search assistant
│   ├── quiz.py                  # Quiz question generator
│   ├── trip_planner.py          # Interest-based district suggestions
│   ├── translations.py          # Bangla/English UI text
│   ├── config.py
│   └── requirements.txt
└── frontend/                 # Templates & static assets
    ├── templates/
    └── static/css/style.css


## 🛠️ Tech Stack

Python (Flask) · scikit-learn (TF-IDF) · Jinja2 · Bootstrap 5 · Chart.js · Web Speech API

## Data note

District facts (history, famous places, food) are general knowledge and stable.
**Population figures are approximate** (2022 BBS census, rounded) for demo purposes —
verify against [bbs.gov.bd](http://bbs.gov.bd) before any serious/official use.

## Krisanu Das

**Your Name**
www.linkedin.com/in/krisanu-das

