"""
app.py — SQL Tutor Agent
Run: streamlit run app.py
"""

import json
import time
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="SQL Tutor Agent", page_icon="🎓", layout="wide")

from utils.engine   import evaluate, run_student_query, QueryError
from utils.tutor    import get_feedback, get_hint, generate_variant
from utils.progress import (
    init_progress, check_badges, update_streak, record_mistake,
    common_mistakes, badge_label,
)

# ── Load challenges ───────────────────────────────────────────────────────────
DATA = Path(__file__).parent / "data" / "challenges.json"
CHALLENGES = json.loads(DATA.read_text())["challenges"]
BY_ID = {c["id"]: c for c in CHALLENGES}

LEVEL_BADGE = {
    "Beginner":     ("🌱", "#16a34a", "#dcfce7"),
    "Intermediate": ("🚀", "#2563eb", "#dbeafe"),
    "Advanced":     ("🔥", "#dc2626", "#fee2e2"),
}

# ── Session state ─────────────────────────────────────────────────────────────
if "progress" not in st.session_state:
    st.session_state.progress = init_progress()
if "current_id" not in st.session_state:
    st.session_state.current_id = CHALLENGES[0]["id"]
if "hint_level" not in st.session_state:
    st.session_state.hint_level = {}          # challenge_id -> next hint index
if "start_time" not in st.session_state:
    st.session_state.start_time = {}          # challenge_id -> ts
if "variant" not in st.session_state:
    st.session_state.variant = None
if "editor_text" not in st.session_state:
    st.session_state.editor_text = ""

P = st.session_state.progress

# ── Styles ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.title-xl { font-size: 2rem; font-weight: 800; color: #0f172a; margin-bottom: 0; }
.subtitle { color: #64748b; margin-top: -4px; }
.chal-item { padding: 6px 4px; border-radius: 6px; }
.badge-pill {
  display:inline-block; padding:2px 9px; border-radius:12px;
  font-size:0.72rem; font-weight:700;
}
.schema-box {
  background:#0f172a; color:#e2e8f0; padding:0.8rem 1rem; border-radius:8px;
  font-family:monospace; font-size:0.82rem; white-space:pre-wrap; line-height:1.5;
}
.feedback-box {
  background:#f0f9ff; border-left:4px solid #0ea5e9; padding:1rem 1.2rem;
  border-radius:0 8px 8px 0;
}
.hint-box {
  background:#fffbeb; border-left:4px solid #f59e0b; padding:0.7rem 1rem;
  border-radius:0 8px 8px 0; color:#92400e;
}
.correct-box {
  background:#f0fdf4; border-left:4px solid #22c55e; padding:1rem 1.2rem;
  border-radius:0 8px 8px 0; color:#166534; font-weight:600;
}
.new-badge {
  background:#fef3c7; border:1px solid #fcd34d; border-radius:8px;
  padding:0.5rem 0.9rem; margin:3px 0; font-weight:700; color:#92400e;
}
</style>
""", unsafe_allow_html=True)


def level_pill(level: str) -> str:
    icon, fg, bg = LEVEL_BADGE[level]
    return f'<span class="badge-pill" style="color:{fg};background:{bg};">{icon} {level}</span>'


# ════════════════════════════════════════════════════════════════════════════════
#  SIDEBAR — challenge list + progress
# ════════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 📚 Challenges")

    solved_n = len(P["solved"])
    st.progress(solved_n / len(CHALLENGES), text=f"{solved_n}/{len(CHALLENGES)} solved")

    # Streak + hints
    c1, c2 = st.columns(2)
    c1.metric("🔥 Streak", f"{P['streak']}d")
    c2.metric("💡 Hints used", P["hints_used"])

    st.divider()

    # Group by level
    for level in ["Beginner", "Intermediate", "Advanced"]:
        st.markdown(f"**{LEVEL_BADGE[level][0]} {level}**")
        for c in [c for c in CHALLENGES if c["level"] == level]:
            solved = c["id"] in P["solved"]
            attempted = c["id"] in P["attempted"]
            mark = "✅" if solved else ("✏️" if attempted else "⬜")
            label = f"{mark} {c['id']}. {c['title']}"
            if st.button(label, key=f"nav_{c['id']}", use_container_width=True):
                st.session_state.current_id = c["id"]
                st.session_state.variant = None
                st.session_state.editor_text = ""
                st.rerun()

    st.divider()
    st.markdown("## 🏅 Badges")
    if P["badges"]:
        for bid in P["badges"]:
            st.markdown(f'<div class="new-badge">{badge_label(bid)}</div>', unsafe_allow_html=True)
    else:
        st.caption("No badges yet — solve a challenge to earn your first!")

    cm = common_mistakes(P)
    if cm:
        st.divider()
        st.markdown("## 🔎 Your tricky topics")
        for topic, n in cm:
            st.caption(f"• {topic} — {n} slip(s)")


# ════════════════════════════════════════════════════════════════════════════════
#  MAIN — current challenge
# ════════════════════════════════════════════════════════════════════════════════
# Use variant if one was generated, else the selected challenge
challenge = st.session_state.variant or BY_ID[st.session_state.current_id]
cid = challenge["id"]

# start timer on first view
if cid not in st.session_state.start_time:
    st.session_state.start_time[cid] = time.time()

st.markdown('<p class="title-xl">🎓 SQL Tutor Agent</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Practice SQL with instant, answer-safe feedback.</p>', unsafe_allow_html=True)

# Header row
hdr_l, hdr_r = st.columns([3, 1])
with hdr_l:
    variant_tag = " (variant)" if st.session_state.variant else ""
    st.markdown(f"### {challenge['title']}{variant_tag}")
    st.markdown(level_pill(challenge["level"]) + f"  &nbsp; <code>{challenge['topic']}</code>",
                unsafe_allow_html=True)
with hdr_r:
    if st.session_state.variant and st.button("← Back to original"):
        st.session_state.variant = None
        st.session_state.editor_text = ""
        st.rerun()

st.write(challenge["description"])

with st.expander("📐 Schema & sample data", expanded=True):
    st.markdown(f'<div class="schema-box">{challenge["schema"]}</div>', unsafe_allow_html=True)
    # show sample data
    import pandas as pd
    for tbl, rows in challenge["sample_data"].items():
        st.caption(f"Table: **{tbl}**")
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

# ── Code editor ────────────────────────────────────────────────────────────────
student_sql = st.text_area(
    "✍️ Your SQL query",
    value=st.session_state.editor_text,
    height=150,
    key=f"editor_{cid}",
    placeholder="SELECT ...",
)

b1, b2, b3, b4 = st.columns(4)
run_clicked   = b1.button("▶ Run Query", use_container_width=True)
check_clicked = b2.button("✅ Check Answer", type="primary", use_container_width=True)
hint_clicked  = b3.button("💡 Get Hint", use_container_width=True)
similar_clicked = b4.button("🔁 Similar Challenge", use_container_width=True)


# ── RUN: just execute and show output, no grading ──────────────────────────────
if run_clicked:
    if not student_sql.strip():
        st.warning("Type a query first.")
    else:
        P["attempted"].add(cid)
        try:
            df = run_student_query(challenge, student_sql)
            st.markdown("**Query output:**")
            st.dataframe(df, use_container_width=True)
            st.caption(f"{len(df)} row(s) returned.")
        except QueryError as e:
            st.error(f"Query error: {e}")


# ── CHECK: grade against expected output ───────────────────────────────────────
if check_clicked:
    if not student_sql.strip():
        st.warning("Type a query first.")
    else:
        P["attempted"].add(cid)
        update_streak(P)
        result = evaluate(challenge, student_sql)

        # show both outputs side by side
        colA, colB = st.columns(2)
        with colA:
            st.markdown("**Your output**")
            if result["student_df"] is not None:
                st.dataframe(result["student_df"], use_container_width=True)
            else:
                st.error(result["error"])
        with colB:
            st.markdown("**Expected output**")
            st.dataframe(result["expected_df"], use_container_width=True)

        if result["correct"]:
            elapsed = int(time.time() - st.session_state.start_time.get(cid, time.time()))
            P["solved"].add(cid)
            st.markdown(
                f'<div class="correct-box">🎉 Correct! Solved in {elapsed}s. '
                f'Result set matches exactly.</div>',
                unsafe_allow_html=True,
            )
            newly = check_badges(P, BY_ID)
            for label in newly:
                st.markdown(f'<div class="new-badge">🏅 New badge: {label}</div>',
                            unsafe_allow_html=True)
            st.balloons()
        else:
            # record + ask the LLM for answer-safe feedback
            record_mistake(P, challenge, result["reason"])
            st.markdown(f"_{result['reason']}_")
            with st.spinner("🧑‍🏫 Tutor is reviewing your query…"):
                try:
                    fb = get_feedback(
                        challenge, student_sql, result["reason"], result.get("error")
                    )
                    st.markdown(f'<div class="feedback-box">{fb}</div>',
                                unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Could not reach the tutor model: {e}")


# ── HINT: serve escalating, answer-safe hints ──────────────────────────────────
if hint_clicked:
    P["attempted"].add(cid)
    lvl = st.session_state.hint_level.get(cid, 0)
    try:
        hint = get_hint(challenge, student_sql, lvl)
        st.session_state.hint_level[cid] = lvl + 1
        P["hints_used"] += 1
        st.markdown(f'<div class="hint-box">💡 <strong>Hint {lvl+1}:</strong> {hint}</div>',
                    unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Could not get a hint: {e}")


# ── SIMILAR: LLM generates a same-concept variant ──────────────────────────────
if similar_clicked:
    with st.spinner("✨ Creating a fresh variant on the same concept…"):
        try:
            base = BY_ID[st.session_state.current_id]   # always vary from the original
            variant = generate_variant(base)
            # validate it actually runs
            chk = evaluate(variant, variant["correct_answer"])
            if not chk["correct"]:
                st.warning("The generated variant didn't validate cleanly — try again.")
            else:
                st.session_state.variant = variant
                st.session_state.editor_text = ""
                st.rerun()
        except Exception as e:
            st.error(f"Couldn't generate a variant: {e}")
