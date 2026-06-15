"""
utils/engine.py — per-challenge in-memory DB, read-only execution, answer comparison
"""

import sqlite3
import re
import pandas as pd


# ── Safety: block anything that isn't a read-only SELECT/CTE ────────────────────
_BLOCKED = re.compile(
    r"\b(DROP|DELETE|UPDATE|INSERT|TRUNCATE|ALTER|CREATE|REPLACE|ATTACH|DETACH|PRAGMA|VACUUM|REINDEX)\b",
    re.IGNORECASE,
)


class QueryError(Exception):
    pass


def _is_safe(sql: str) -> tuple[bool, str]:
    s = sql.strip().rstrip(";").strip()
    if not s:
        return False, "Query is empty."
    first = s.split()[0].upper() if s.split() else ""
    if first not in ("SELECT", "WITH"):
        return False, f"Only SELECT / WITH queries are allowed (got {first})."
    if _BLOCKED.search(s):
        return False, "Query contains a blocked keyword (write/DDL operations are not allowed)."
    if ";" in s:
        return False, "Multiple statements are not allowed."
    return True, ""


def build_challenge_db(challenge: dict) -> sqlite3.Connection:
    """
    Create a fresh in-memory SQLite DB for a single challenge,
    apply its schema, and load its sample_data. Returns a live connection.
    """
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()

    # Apply schema (may contain multiple CREATE TABLE statements)
    cur.executescript(challenge["schema"])

    # Load sample data: { table_name: [ [row], [row], ... ] }
    for table, rows in challenge["sample_data"].items():
        if not rows:
            continue
        ncols = len(rows[0])
        placeholders = ",".join(["?"] * ncols)
        cur.executemany(f"INSERT INTO {table} VALUES ({placeholders})", rows)

    conn.commit()
    return conn


def _run(conn: sqlite3.Connection, sql: str) -> pd.DataFrame:
    """Execute a read-only query on the given connection, return a DataFrame."""
    ok, reason = _is_safe(sql)
    if not ok:
        raise QueryError(reason)
    try:
        return pd.read_sql_query(sql, conn)
    except Exception as e:
        raise QueryError(str(e))


def run_student_query(challenge: dict, student_sql: str) -> pd.DataFrame:
    """Run the student's query against a fresh isolated DB."""
    conn = build_challenge_db(challenge)
    try:
        return _run(conn, student_sql)
    finally:
        conn.close()


def _normalize(df: pd.DataFrame, ignore_order: bool) -> pd.DataFrame:
    """
    Normalize a result frame for comparison:
    - reset column names to positions (so aliases don't have to match exactly)
    - optionally sort rows so row order doesn't matter
    """
    out = df.copy()
    out.columns = range(len(out.columns))   # compare by position, not name
    if ignore_order:
        out = out.sort_values(by=list(out.columns), kind="mergesort").reset_index(drop=True)
    else:
        out = out.reset_index(drop=True)
    return out


def evaluate(challenge: dict, student_sql: str) -> dict:
    """
    Run both the student query and the correct answer on identical fresh DBs,
    compare result sets, and return a structured verdict.

    Returns dict with keys:
      ok            : bool  (did the student query run at all)
      correct       : bool  (do the result sets match)
      error         : str|None
      student_df    : DataFrame|None
      expected_df   : DataFrame
      reason        : str  (human-readable explanation of mismatch type)
    """
    # Detect whether the expected query cares about order (has ORDER BY)
    order_matters = "ORDER BY" in challenge["correct_answer"].upper()

    # Expected result (always runnable)
    conn_e = build_challenge_db(challenge)
    try:
        expected_df = _run(conn_e, challenge["correct_answer"])
    finally:
        conn_e.close()

    # Student result
    try:
        student_df = run_student_query(challenge, student_sql)
    except QueryError as e:
        return {
            "ok": False, "correct": False, "error": str(e),
            "student_df": None, "expected_df": expected_df,
            "reason": "Your query did not run.",
        }

    # Compare
    exp_n = _normalize(expected_df, ignore_order=not order_matters)
    stu_n = _normalize(student_df, ignore_order=not order_matters)

    if exp_n.shape != stu_n.shape:
        reason = (
            f"Shape mismatch: expected {exp_n.shape[0]} rows × {exp_n.shape[1]} cols, "
            f"got {stu_n.shape[0]} rows × {stu_n.shape[1]} cols."
        )
        return {
            "ok": True, "correct": False, "error": None,
            "student_df": student_df, "expected_df": expected_df, "reason": reason,
        }

    # Values: compare cell-by-cell as strings (avoids float/int dtype noise)
    try:
        same = exp_n.astype(str).reset_index(drop=True).equals(
            stu_n.astype(str).reset_index(drop=True)
        )
    except Exception:
        same = False

    return {
        "ok": True,
        "correct": bool(same),
        "error": None,
        "student_df": student_df,
        "expected_df": expected_df,
        "reason": "Result set matches the expected output." if same
                  else "Rows/values differ from the expected output.",
    }
