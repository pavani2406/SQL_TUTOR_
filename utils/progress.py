"""
utils/progress.py — progress tracking, badges, streaks (session-state based)
"""

from datetime import date


def init_progress() -> dict:
    return {
        "attempted": set(),       # challenge ids attempted
        "solved": set(),          # challenge ids solved
        "hints_used": 0,
        "mistakes": [],           # list of {challenge_id, topic, note}
        "badges": set(),
        "last_practice_date": None,
        "streak": 0,
    }


# ── Badge rules ───────────────────────────────────────────────────────────────
# Each badge: (id, label, predicate(progress, challenges_by_id) -> bool)
def _solved_topics(progress, by_id):
    return {by_id[cid]["topic"] for cid in progress["solved"] if cid in by_id}

def _solved_levels(progress, by_id):
    levels = {}
    for cid in progress["solved"]:
        if cid in by_id:
            lvl = by_id[cid]["level"]
            levels[lvl] = levels.get(lvl, 0) + 1
    return levels


BADGE_DEFS = [
    ("first_solve", "🎯 First Blood — first challenge solved",
     lambda p, b: len(p["solved"]) >= 1),
    ("first_join", "🔗 First JOIN Solved",
     lambda p, b: any("JOIN" in b[c]["topic"].upper() for c in p["solved"] if c in b)),
    ("subquery_master", "🧩 Subquery Master",
     lambda p, b: any("SUBQUERY" in b[c]["topic"].upper() for c in p["solved"] if c in b)),
    ("window_wizard", "🪟 Window Wizard",
     lambda p, b: any("WINDOW" in b[c]["topic"].upper() for c in p["solved"] if c in b)),
    ("cte_crafter", "🏗️ CTE Crafter",
     lambda p, b: any("CTE" in b[c]["topic"].upper() for c in p["solved"] if c in b)),
    ("beginner_clear", "🌱 Beginner Cleared",
     lambda p, b: _solved_levels(p, b).get("Beginner", 0) >= 7),
    ("intermediate_clear", "🚀 Intermediate Cleared",
     lambda p, b: _solved_levels(p, b).get("Intermediate", 0) >= 7),
    ("advanced_clear", "🏆 Advanced Cleared",
     lambda p, b: _solved_levels(p, b).get("Advanced", 0) >= 6),
    ("no_hints", "💪 Five Without a Hint",
     lambda p, b: len(p["solved"]) >= 5 and p["hints_used"] == 0),
    ("half_way", "⭐ Halfway There — 10 solved",
     lambda p, b: len(p["solved"]) >= 10),
    ("completionist", "👑 Completionist — all 20 solved",
     lambda p, b: len(p["solved"]) >= 20),
]


def check_badges(progress: dict, by_id: dict) -> list[str]:
    """Return list of NEWLY awarded badge labels (and mutate progress['badges'])."""
    newly = []
    for bid, label, pred in BADGE_DEFS:
        if bid not in progress["badges"] and pred(progress, by_id):
            progress["badges"].add(bid)
            newly.append(label)
    return newly


def badge_label(bid: str) -> str:
    for b, label, _ in BADGE_DEFS:
        if b == bid:
            return label
    return bid


def update_streak(progress: dict) -> None:
    """Update the daily-practice streak counter."""
    today = date.today()
    last = progress["last_practice_date"]
    if last == today:
        return
    if last is None:
        progress["streak"] = 1
    else:
        delta = (today - last).days
        if delta == 1:
            progress["streak"] += 1
        elif delta > 1:
            progress["streak"] = 1
    progress["last_practice_date"] = today


def record_mistake(progress: dict, challenge: dict, note: str) -> None:
    progress["mistakes"].append({
        "challenge_id": challenge["id"],
        "topic": challenge.get("topic", "?"),
        "note": note,
    })


def common_mistakes(progress: dict, top_n: int = 3) -> list[tuple[str, int]]:
    """Return the most frequent mistake topics."""
    from collections import Counter
    counts = Counter(m["topic"] for m in progress["mistakes"])
    return counts.most_common(top_n)
