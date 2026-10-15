# Unit 1: Natural Language Processing Assessments

**Course:** DSA0311 - Natural Language Processing  
**Academic Year:** 2026  
**Bloom's Taxonomy Level:** BL-3 (Application / Analysis)

---

## Documents & Submissions

### 1. Assessment Tool 1: Application Based Questions (40% Weightage)
* **Completed Submission Document:** [`DSA03-NLP_CO1_AT1_Completed.docx`](./DSA03-NLP_CO1_AT1_Completed.docx)
* **Original Prompt Document:** [`DSA03-NLP_CO1_AT1_Original.docx`](./DSA03-NLP_CO1_AT1_Original.docx)

### 2. Assessment Tool 3: Coding Challenge (30% Weightage)
* **Completed Submission Document:** [`DSA03-NLP_CO1_AT3_Completed.docx`](./DSA03-NLP_CO1_AT3_Completed.docx) (also in [`Assessment-3/DSA03-NLP_CO1_AT3_Completed.docx`](./Assessment-3/DSA03-NLP_CO1_AT3_Completed.docx))
* **Original Prompt Document:** [`Assessment-3/DSA03-NLP_CO1_AT3.docx`](./Assessment-3/DSA03-NLP_CO1_AT3.docx)

---

## Assessment Tool 1 - Application Based Problems
* **[Assessment-1 (Q1)](./Assessment-1/main.py)** - Section 1: Regular Expressions – Resume Information Extraction
  * *Features:* Candidate Name, Email, Mobile (+91 support), Skills (Python, Java, SQL, ML, NLP), Experience parsing, structured summary, and eligibility filtering (>= 2 yrs + Python).
* **[Assessment-2 (Q2)](./Assessment-2/main.py)** - Section 2: Regular Expressions – Product Search System
  * *Features:* Exact search, Prefix search, Suffix search, Partial keyword search, Case-insensitive matching, and statistical match frequency reporting.
* **[Assessment-3 (Q3)](./Assessment-3/main.py)** - Section 3: Regular Expressions – University Registration System
  * *Features:* Student Register Number verification, Institutional Email validation (`@saveetha.com`, `@university.ac.in`), Course Code (`DSA03`), Semester (1–8 bounds), Mobile Number, field-level diagnostics, and final registration audit report.

---

## Assessment Tool 3 - Coding Challenge Problems
* **[Section 1 (Q1)](./Assessment-3/section_1_validator.py)** - Intelligent Email & Password Validator
  * *Features:* Strict email validation (`^[a-zA-Z][a-zA-Z0-9._]*@[a-zA-Z]+\.(com|org|edu|net|in)$`), password lookahead complexity enforcement (>=8 chars, upper, lower, digit, special `@,#,$,%,&,!`), and 10-digit mobile verification (`^[6-9]\d{9}$`).
* **[Section 2 (Q2)](./Assessment-3/section_2_dfa_simulator.py)** - Finite State Automata (DFA) Simulator
  * *Features:* General 5-tuple $(Q, \Sigma, \delta, q_0, F)$ DFA engine recognizing strings ending with `'ab'`, step-by-step state trajectory generation (e.g., `q0 -> q1 -> q2 -> q1 -> q1 -> q2`), and automated acceptance/rejection decisions.
* **[Section 3 (Q3)](./Assessment-3/section_3_pattern_search.py)** - Smart Pattern Matching Engine
  * *Features:* High-throughput search primitives supporting Date extraction, Phone number extraction, Hashtags (`#`), User Mentions (`@`), Prefixes, Suffixes, and exact Word boundary matching with span index reporting.
