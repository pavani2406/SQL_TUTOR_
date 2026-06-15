# 🎓 SQL Tutor Agent
**SQL-10 | AI Implementation Protocol — Student Project**

An interactive web app that poses SQL challenges, runs your answer against an isolated
in-memory database, compares it to the expected output, and gives **targeted, answer-safe
feedback** — a hint and an explanation that guide you without handing over the solution.

Runs **100% free and locally** using Ollama (no API key, no cloud cost).

---

## 📦 Project Structure

```
sqltutor/
├── app.py                  # Streamlit UI
├── requirements.txt
├── data/
│   └── challenges.json     # 20 challenges across 3 levels
└── utils/
    ├── engine.py           # in-memory DB builder, read-only exec, answer comparison
    ├── tutor.py            # LLM feedback / hints / variant generation (Ollama)
    └── progress.py         # progress tracking, badges, streaks
```

---

## 🚀 Setup

### 1. Install Ollama (one time)
Download from [ollama.com](https://ollama.com), install, then pull the model:
```bash
ollama pull qwen2.5-coder:7b
```
(Lower-spec machine? Use `qwen2.5-coder:3b` and change `MODEL_NAME` in `utils/tutor.py`.)

### 2. Install Python deps
```bash
pip install -r requirements.txt
```

### 3. Run
```bash
streamlit run app.py
```
Make sure Ollama is running (tray icon present) before clicking *Check Answer* or *Get Hint*.

---

## 🧩 The Challenge Bank

20 challenges in `challenges.json`, each fully self-contained:

| Field | Purpose |
|---|---|
| `id`, `level`, `topic`, `title` | metadata + difficulty badge |
| `description` | what the student must write |
| `schema` | CREATE TABLE statement(s) for this challenge |
| `sample_data` | rows loaded into the in-memory DB |
| `correct_answer` | reference solution (never shown to the student) |
| `hints` | 3 escalating, answer-safe hints |

**Coverage:** 7 Beginner (SELECT, WHERE, COUNT, DISTINCT, SUM, LIKE, LIMIT),
7 Intermediate (INNER/LEFT JOIN, GROUP BY/HAVING, subquery, CASE, dates),
6 Advanced (ROW_NUMBER, RANK, CTE, running totals, self-join, LAG).

---

## ⚙️ How It Works

```
Pick a challenge
      │
      ▼
Fresh in-memory SQLite DB built from the challenge's schema + sample_data
      │
      ▼
Student writes SQL ──► Run Query (preview output, no grading)
      │
      ▼
Check Answer:
  • student query runs in an isolated read-only DB
  • correct_answer runs in an identical fresh DB
  • result sets compared (column-position + row-set; order-aware only if the
    expected query uses ORDER BY)
      │
      ├── match  → ✅ correct, award badges, update streak
      └── differ → 🧑‍🏫 LLM gives answer-safe feedback:
                     what's right · the missing concept ·
                     a step-by-step nudge · a generic toy example
```

### Answer-safe feedback
The tutor is explicitly instructed **never to reveal the reference query** — it names
concepts and illustrates with unrelated toy tables, so the student still does the writing.

### Hints
Curated escalating hints are served first (already answer-safe). If exhausted, the LLM
generates one more gentle nudge.

### Similar Challenge (spaced repetition)
Generates a brand-new problem on the **same concept** with different tables/data, then
auto-validates that its reference answer actually runs before showing it.

---

## 🏅 Progress & Gamification

- **Progress bar:** `X / 20 solved`
- **Streak:** consecutive days of practice
- **Badges:** First Blood, First JOIN Solved, Subquery Master, Window Wizard, CTE Crafter,
  level-clear badges, "Five Without a Hint", Halfway There, Completionist
- **Tricky topics:** tracks your most common mistake areas

Progress lives in Streamlit session state (resets when the app restarts).

---

## 🔒 Safety

Every student query runs in a throwaway **in-memory** database — never against real data.
A guard rejects anything that isn't a `SELECT`/`WITH` and blocks
`DROP/DELETE/UPDATE/INSERT/ALTER/CREATE/…` plus multi-statement injection.

---

## 🧪 Quick Tests
```bash
# All 20 reference answers self-validate as correct
python -c "import json; from utils.engine import evaluate; \
chs=json.load(open('data/challenges.json'))['challenges']; \
print('PASS' if all(evaluate(c,c['correct_answer'])['correct'] for c in chs) else 'FAIL')"
```
