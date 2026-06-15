# 🧪 SQL-TUTOR Test Cases

## Test Case 1: User Selects Difficulty Level

| Field | Details |
|--------|---------|
| Test Case ID | TC_01 |
| Module | Challenge Selection |
| Objective | Verify that users can select a difficulty level |
| Input | Beginner / Intermediate / Advanced |
| Expected Result | Corresponding challenges are displayed |
| Status | Pass |

## Test Case 2: Display Database Schema

| Field | Details |
|--------|---------|
| Test Case ID | TC_02 |
| Module | Schema Viewer |
| Objective | Verify schema visibility |
| Input | Click **View Schema** |
| Expected Result | Database tables and sample data are displayed |
| Status | Pass |

## Test Case 3: Execute Valid SQL Query

| Field | Details |
|--------|---------|
| Test Case ID | TC_03 |
| Module | Query Execution |
| Objective | Verify successful query execution |
| Input | `SELECT * FROM customers;` |
| Expected Result | Query results displayed in table format |
| Status | Pass |

## Test Case 4: Execute Invalid SQL Query

| Field | Details |
|--------|---------|
| Test Case ID | TC_04 |
| Module | Query Execution |
| Objective | Verify error handling |
| Input | `SELEC * FROM customers;` |
| Expected Result | SQL syntax error message displayed |
| Status | Pass |

## Test Case 5: Correct Answer Validation

| Field | Details |
|--------|---------|
| Test Case ID | TC_05 |
| Module | Evaluation Engine |
| Objective | Verify correct answer detection |
| Input | Correct SQL solution |
| Expected Result | Success message displayed |
| Status | Pass |

## Test Case 6: Incorrect Answer Validation

| Field | Details |
|--------|---------|
| Test Case ID | TC_06 |
| Module | Evaluation Engine |
| Objective | Verify incorrect answer detection |
| Input | Wrong SQL query |
| Expected Result | Feedback and hint generated |
| Status | Pass |

## Test Case 7: AI Hint Generation

| Field | Details |
|--------|---------|
| Test Case ID | TC_07 |
| Module | AI Hint System |
| Objective | Verify hint generation |
| Input | User submits incorrect query |
| Expected Result | Helpful hint displayed without revealing the answer |
| Status | Pass |

## Test Case 8: AI Feedback Generation

| Field | Details |
|--------|---------|
| Test Case ID | TC_08 |
| Module | AI Feedback Engine |
| Objective | Verify explanation of mistakes |
| Input | Incorrect query |
| Expected Result | AI explains query mistakes in simple language |
| Status | Pass |

## Test Case 9: Variant Question Generation

| Field | Details |
|--------|---------|
| Test Case ID | TC_09 |
| Module | Variant Generator |
| Objective | Verify generation of similar challenges |
| Input | Click **Generate Similar Challenge** |
| Expected Result | New SQL problem generated |
| Status | Pass |

## Test Case 10: Progress Tracking

| Field | Details |
|--------|---------|
| Test Case ID | TC_10 |
| Module | Gamification |
| Objective | Verify challenge completion tracking |
| Input | Solve a challenge |
| Expected Result | Progress updated successfully |
| Status | Pass |

## Test Case 11: Streak Counter Update

| Field | Details |
|--------|---------|
| Test Case ID | TC_11 |
| Module | Gamification |
| Objective | Verify streak update |
| Input | Solve multiple challenges |
| Expected Result | Streak count increases correctly |
| Status | Pass |

## Test Case 12: Badge Awarding System

| Field | Details |
|--------|---------|
| Test Case ID | TC_12 |
| Module | Gamification |
| Objective | Verify badge generation |
| Input | Reach badge criteria |
| Expected Result | Badge awarded and displayed |
| Status | Pass |

## Test Case 13: Session Persistence

| Field | Details |
|--------|---------|
| Test Case ID | TC_13 |
| Module | Session Management |
| Objective | Verify session state maintenance |
| Input | Navigate between challenges |
| Expected Result | Progress remains available during session |
| Status | Pass |

## Test Case 14: SQL Injection Prevention

| Field | Details |
|--------|---------|
| Test Case ID | TC_14 |
| Module | Security |
| Objective | Verify protection against malicious queries |
| Input | `DROP TABLE customers;` |
| Expected Result | Query blocked and warning displayed |
| Status | Pass |

## Test Case 15: Empty Query Submission

| Field | Details |
|--------|---------|
| Test Case ID | TC_15 |
| Module | Validation |
| Objective | Verify handling of empty input |
| Input | Blank query |
| Expected Result | User prompted to enter a SQL query |
| Status | Pass |

## Test Case 16: Application Startup

| Field | Details |
|--------|---------|
| Test Case ID | TC_16 |
| Module | Deployment |
| Objective | Verify application launch |
| Input | `streamlit run app.py` |
| Expected Result | Application opens successfully in browser |
| Status | Pass |

---

### Test Summary

| Metric | Value |
|---------|---------|
| Total Test Cases | 16 |
| Functional Testing | 12 |
| Validation Testing | 2 |
| Security Testing | 1 |
| Deployment Testing | 1 |
| Overall Status | ✅ Pass |
