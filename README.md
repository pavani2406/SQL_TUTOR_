# 🎓 SQL Tutor Agent

Demo video link :  https://drive.google.com/file/d/1hd26a5eI6JlM4oi4XOvU8X2TV7tXD-Of/view?usp=sharing

An interactive web app that poses SQL challenges, runs your answer against an isolated
in-memory database, compares it to the expected output, and gives **targeted, answer-safe
feedback** — a hint and an explanation that guide you without handing over the solution.

---
# Team mmebers:

## 👥 Team Members

| S.No | Name | Role | Email |
|------|------|------|--------|
| 1 | Y. Gnana Pavani | Frontend Developer & Backend Developer | yg.pavani2004@gmail.com |
| 2 | D. Sri Lakshmi | Backend Developer & Database Manager | sreelaxmi7017@gmail.com |
| 3 | Shaik Aisha Afreen | AI Integration, Testing & Documentation | shaikaishaafreen@gmail.com |

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


### 1. Install Python deps
```bash
pip install -r requirements.txt
pip install streamlit
pip install pandas
pip install google-generativeai

```
### 2. Install Ollama

Download Ollama from:

https://ollama.com

Pull the model:

```bash
ollama pull qwen2.5-coder:3b
```

Start Ollama:

```bash
ollama serve
```

### 3. Run
```bash
streamlit run app.py
```


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

## 🛠️ Tools & Technologies

We used the following tools:

- Python 3.10+
- Streamlit (Web UI)
- SQLite (Database Engine)
- Pandas (Data Processing)
- JSON (Challenge Storage)
- Ollama (Local LLM Runtime)
- Qwen2.5-Coder 3B (AI Model for Feedback, Hints & Challenge Generation)

## Libraries Used

Our project uses the following Python libraries:

📌 Core Libraries:

import json
→ Used to load SQL challenges from JSON file

import time
→ Used for tracking solving time and streaks

from pathlib import Path
→ Used to handle file paths for project structure

import urllib.request
→ Used for fetching external resources if needed

import urllib.error
→ Handles errors while fetching data

from datetime import date
→ Used for tracking daily streaks

import sqlite3
→ Core database engine for executing SQL queries

import re
→ Used for pattern matching and SQL validation

import pandas as pd
→ Used for displaying query results in table format

---

## Architecture Overview 

The system follows a modular architecture:

🖥️ Frontend Layer

Built using Streamlit

Handles UI, input, and display


⚙️ Backend Layer

Python engine processes SQL queries

SQLite database stores sample data


📊 Evaluation Layer

Compares student output vs expected output


🧠 AI Layer

Generates:

Hints

Feedback

Similar questions



💾 Session Layer

Uses Streamlit session state for:

progress tracking

hints

streaks

current challenge

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

## 🧠 AI Capability Demonstrated

### Intelligent SQL Tutoring
- Evaluates student SQL queries.
- Detects syntax and logical errors.
- Compares outputs with expected results.
- Provides contextual hints without revealing answers.

### Personalized Feedback
- Identifies common SQL mistakes.
- Explains errors in simple language.
- Suggests improvements step-by-step.

### Automated Assessment
- Executes user queries on a sample database.
- Validates correctness automatically.
- Generates targeted learning recommendations.

### Adaptive Learning Support
- Encourages independent problem-solving.
- Helps students understand SQL concepts through guided hints.
- Creates an interactive learning experience.

---



## ⚙️ Assumptions

- Users possess basic SQL knowledge.
- Sample databases are preconfigured.
- Expected outputs exist for every challenge.
- Ollama is installed and running locally.
- Qwen2.5-Coder model is available locally.
- Submitted queries are intended for learning purposes.

## ⚠️ Limitations

- Feedback quality depends on the LLM response.
- Extremely complex queries may receive generic hints.
- Supports predefined SQL practice datasets only.
- Requires Ollama and Qwen2.5-Coder to be installed locally.
- Not intended for production database environments.

## 🔒 Safety

Every student query runs in a throwaway **in-memory** database — never against real data.
A guard rejects anything that isn't a `SELECT`/`WITH` and blocks
`DROP/DELETE/UPDATE/INSERT/ALTER/CREATE/…` plus multi-statement injection.

---

## Conclusio
The SQL Tutor project is designed to help beginners strengthen their understanding of SQL through hands-on practice. By providing interactive challenges, real-time query evaluation, and instant feedback

