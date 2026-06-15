"""
utils/tutor.py — LLM tutoring via local Ollama
Gives targeted feedback and hints WITHOUT revealing the correct query.
"""

import json
import urllib.request
import urllib.error

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen2.5-coder:7b"   # change to qwen2.5-coder:3b on lower-spec machines


def _chat(system: str, user: str, max_tokens: int = 600) -> str:
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "stream": False,
        "options": {"temperature": 0.3, "num_predict": max_tokens},
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(OLLAMA_URL, data=data,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            body = json.loads(resp.read().decode("utf-8"))
        return body["message"]["content"].strip()
    except urllib.error.URLError as e:
        raise RuntimeError(
            "Could not reach Ollama at localhost:11434. Make sure Ollama is running "
            f"and you've pulled the model:  ollama pull {MODEL_NAME}\n\nDetails: {e}"
        ) from e


# ── Feedback on a wrong answer ──────────────────────────────────────────────────
FEEDBACK_SYSTEM = """You are a warm, encouraging SQL tutor helping a junior developer learn.

You will be given a challenge description, the student's SQL query, and an internal
reference solution. Your job is to help the student FIX THEIR OWN query.

CRITICAL RULES:
- NEVER reveal, write out, or paste the full correct query. Not even partially as a
  complete clause they can copy wholesale.
- Do NOT give them a copy-paste answer. Guide them to discover it.
- It is fine to name SQL concepts/keywords (JOIN, GROUP BY, IS NULL, etc.) and explain
  what they do, but the student must do the actual writing.

Respond in this friendly structure using short markdown sections:
**What you got right** — genuine specifics about their query.
**What's off** — the single most important conceptual mistake (not a list of nitpicks).
**How to think about it** — a step-by-step nudge toward the fix, in words not code.
**Tiny example** — a SHORT, GENERIC illustrative snippet on unrelated toy tables
  (e.g. table 't' with column 'x') that demonstrates the concept WITHOUT solving their
  exact problem.

Keep it concise and kind. Assume they can do this with one good nudge."""


def get_feedback(challenge: dict, student_sql: str, mismatch_reason: str,
                 run_error: str | None = None) -> str:
    diagnostic = run_error if run_error else mismatch_reason
    user = (
        f"Challenge: {challenge['title']}\n"
        f"Task: {challenge['description']}\n\n"
        f"Schema:\n{challenge['schema']}\n\n"
        f"Student's query:\n{student_sql}\n\n"
        f"Internal reference solution (DO NOT reveal this to the student):\n"
        f"{challenge['correct_answer']}\n\n"
        f"What went wrong when checking: {diagnostic}\n\n"
        f"Give the student targeted feedback following your rules. Remember: never reveal the solution."
    )
    return _chat(FEEDBACK_SYSTEM, user)


# ── Progressive hint ──────────────────────────────────────────────────────────────
HINT_SYSTEM = """You are a SQL tutor giving a SINGLE short hint to nudge a student forward.

CRITICAL RULES:
- NEVER write the full or near-full correct query.
- One or two sentences maximum.
- Point at the concept or keyword they likely need next, not the whole solution.
- Encouraging tone."""


def get_hint(challenge: dict, student_sql: str, hint_level: int) -> str:
    """
    hint_level is 0-based. The challenge bank has curated hints that escalate;
    we serve those directly (they're already answer-safe), and only fall back to
    the LLM if the student exhausts them.
    """
    curated = challenge.get("hints", [])
    if hint_level < len(curated):
        return curated[hint_level]

    # Fallback: generate one more gentle nudge without revealing the answer
    user = (
        f"Task: {challenge['description']}\n"
        f"Schema:\n{challenge['schema']}\n\n"
        f"Student's current attempt:\n{student_sql or '(empty)'}\n\n"
        f"They have already used all curated hints. Give ONE more gentle nudge "
        f"toward the concept they still need. Do NOT reveal the query."
    )
    return _chat(HINT_SYSTEM, user, max_tokens=120)


# ── Similar challenge generator (spaced repetition) ────────────────────────────────
VARIANT_SYSTEM = """You are a SQL teacher creating a practice variant.

Given an existing challenge, invent a NEW practice problem that drills the SAME SQL
concept but with a different scenario/table names/numbers. Return ONLY valid JSON
(no markdown, no backticks) with exactly these keys:
  "title"        : short title
  "description"  : what the student must write a query to do
  "schema"       : one or more CREATE TABLE statements (SQLite)
  "sample_data"  : object mapping each table name to a list of row-arrays matching the schema column order
  "correct_answer": a valid SQLite query that solves it
  "hints"        : array of 3 escalating hint strings that do NOT reveal the full query

Keep tables small (3-6 rows). Make sure correct_answer actually runs against the schema+data."""


def generate_variant(challenge: dict) -> dict:
    user = (
        f"Concept to drill: {challenge['topic']}\n"
        f"Original challenge for reference:\n"
        f"Title: {challenge['title']}\n"
        f"Description: {challenge['description']}\n"
        f"Schema: {challenge['schema']}\n\n"
        f"Create a fresh variant on the SAME concept. Return ONLY the JSON object."
    )
    raw = _chat(VARIANT_SYSTEM, user, max_tokens=900).strip()
    # Strip accidental code fences
    if raw.startswith("```"):
        raw = "\n".join(l for l in raw.splitlines() if not l.strip().startswith("```")).strip()
    data = json.loads(raw)   # may raise; caller handles
    # stamp required fields
    data.setdefault("level", challenge["level"])
    data.setdefault("topic", challenge["topic"])
    data["id"] = f"variant-{challenge['id']}"
    return data
