SQL-TUTOR Test Cases
Test Case 1: User Selects Difficulty Level
Test Case ID	TC_01
Module	Challenge Selection
Objective	Verify that users can select a difficulty level
Input	Beginner / Intermediate / Advanced
Expected Result	Corresponding challenges are displayed
Status	Pass
________________________________________
Test Case 2: Display Database Schema
Test Case ID	TC_02
Module	Schema Viewer
Objective	Verify schema visibility
Input	Click "View Schema"
Expected Result	Database tables and sample data are displayed
Status	Pass
________________________________________
Test Case 3: Execute Valid SQL Query
Test Case ID	TC_03
Module	Query Execution
Objective	Verify successful query execution
Input	SELECT * FROM customers;
Expected Result	Query results displayed in table format
Status	Pass
________________________________________
Test Case 4: Execute Invalid SQL Query
Test Case ID	TC_04
Module	Query Execution
Objective	Verify error handling
Input	SELEC * FROM customers;
Expected Result	SQL syntax error message displayed
Status	Pass
________________________________________
Test Case 5: Correct Answer Validation
Test Case ID	TC_05
Module	Evaluation Engine
Objective	Verify correct answer detection
Input	Correct SQL solution
Expected Result	Success message displayed
Status	Pass
________________________________________
Test Case 6: Incorrect Answer Validation
Test Case ID	TC_06
Module	Evaluation Engine
Objective	Verify incorrect answer detection
Input	Wrong SQL query
Expected Result	Feedback and hint generated
Status	Pass
________________________________________


Test Case 7: AI Hint Generation
Test Case ID	TC_07
Module	AI Hint System
Objective	Verify hint generation
Input	User submits incorrect query
Expected Result	Helpful hint displayed without revealing answer
Status	Pass
________________________________________
Test Case 8: AI Feedback Generation
Test Case ID	TC_08
Module	AI Feedback Engine
Objective	Verify explanation of mistakes
Input	Incorrect query
Expected Result	AI explains query mistakes in simple language
Status	Pass
________________________________________
Test Case 9: Variant Question Generation
Test Case ID	TC_09
Module	Variant Generator
Objective	Verify generation of similar challenges
Input	Click "Generate Similar Challenge"
Expected Result	New SQL problem generated
Status	Pass
________________________________________


Test Case 10: Progress Tracking
Test Case ID	TC_10
Module	Gamification
Objective	Verify challenge completion tracking
Input	Solve a challenge
Expected Result	Progress updated successfully
Status	Pass
________________________________________
Test Case 11: Streak Counter Update
Test Case ID	TC_11
Module	Gamification
Objective	Verify streak update
Input	Solve multiple challenges
Expected Result	Streak count increases correctly
Status	Pass
________________________________________
Test Case 12: Badge Awarding System
Test Case ID	TC_12
Module	Gamification
Objective	Verify badge generation
Input	Reach badge criteria
Expected Result	Badge awarded and displayed
Status	Pass
________________________________________


Test Case 13: Session Persistence
Test Case ID	TC_13
Module	Session Management
Objective	Verify session state maintenance
Input	Navigate between challenges
Expected Result	Progress remains available during session
Status	Pass
________________________________________
Test Case 14: SQL Injection Prevention
Test Case ID	TC_14
Module	Security
Objective	Verify protection against malicious queries
Input	DROP TABLE customers;
Expected Result	Query blocked and warning displayed
Status	Pass
________________________________________
Test Case 15: Empty Query Submission
Test Case ID	TC_15
Module	Validation
Objective	Verify handling of empty input
Input	Blank query
Expected Result	User prompted to enter SQL query
Status	Pass
________________________________________


Test Case 16: Application Startup
Test Case ID	TC_16
Module	Deployment
Objective	Verify application launch
Input	streamlit run app.py
Expected Result	Application opens successfully in browser
Status	Pass
