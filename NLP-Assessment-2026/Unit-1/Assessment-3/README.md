# Unit 1: Assessment Tool 3 – Coding Challenge

**Course:** DSA0311 - Natural Language Processing  
**Assessment Tool:** CO1 - Assessment Tool 3 (Coding Challenge)  
**Weightage:** 30% of CIA  
**Bloom's Taxonomy Level:** BL-3 (Application / Analysis)  
**Original Prompt Document:** [`DSA03-NLP_CO1_AT3.docx`](./DSA03-NLP_CO1_AT3.docx)  
**Completed Submission Document:** [`DSA03-NLP_CO1_AT3_Completed.docx`](./DSA03-NLP_CO1_AT3_Completed.docx)

---

## Coding Challenge Overview

This assessment evaluates regular expressions, finite state automata (DFA), and advanced pattern matching across three sections:

| Section | Focus / Title | Modular Script | Output Log |
|---|---|---|---|
| **Section 1 (Q1)** | **Intelligent Email & Password Validator**<br>Regex validation of emails, complex password policies (lookaheads), and 10-digit mobile numbers starting 6–9. | [`section_1_validator.py`](./section_1_validator.py) | [`output/section_1_output.txt`](./output/section_1_output.txt) |
| **Section 2 (Q2)** | **Design a Finite State Automata (FSA) Simulator**<br>Deterministic Finite Automaton (DFA) simulator accepting formal 5-tuple, simulating state paths on strings ending with `'ab'`, and evaluating language membership. | [`section_2_dfa_simulator.py`](./section_2_dfa_simulator.py) | [`output/section_2_output.txt`](./output/section_2_output.txt) |
| **Section 3 (Q3)** | **Smart Pattern Matching Engine**<br>Text search engine using regex for Date search, Phone number search, Hashtags (`#`), Mentions (`@`), Prefixes, Suffixes, and exact Word isolation. | [`section_3_pattern_search.py`](./section_3_pattern_search.py) | [`output/section_3_output.txt`](./output/section_3_output.txt) |

---

## Section Summaries

### [Section 1: Intelligent Email and Password Validator](./section_1_validator.py)
* **Email Validation:** Enforces leading alphabetic character, permissible alphanumeric + dot + underscore local part, alphabetic domain, and restricted TLD extensions (`.com`, `.org`, `.edu`, `.net`, `.in`).
* **Password Validation:** Enforces minimum 8 characters, at least one uppercase letter, at least one lowercase letter, at least one numerical digit, and at least one approved special character (`@`, `#`, `$`, `%`, `&`, `!`) using positive lookahead assertions.
* **Mobile Validation:** Validates exact 10-digit mobile number with leading digit in `6–9`.

### [Section 2: Finite State Automata (DFA) Simulator](./section_2_dfa_simulator.py)
* **Automaton Definition:** $M = (Q, \Sigma, \delta, q_0, F)$ where $Q = \{q_0, q_1, q_2\}$, $\Sigma = \{a, b\}$, $q_0 = \text{start}$, $F = \{q_2\}$.
* **Simulation:** Tracks and prints the exact transition trajectory (e.g. `q0 -> q1 -> q2 -> q1 -> q1 -> q2` for input `abaab`), verifying acceptance for valid strings and rejection for non-matching or out-of-alphabet inputs.

### [Section 3: Smart Pattern Matching Engine](./section_3_pattern_search.py)
* **Search Primitives:**
  1. *Date Search:* Matches `DD/MM/YYYY`, `DD-MM-YYYY`, and standard numeric date patterns.
  2. *Phone Search:* Matches 10-digit phone numbers with optional country code (+91).
  3. *Hashtag Search:* Matches `#\w+` social media tags.
  4. *Mention Search:* Matches `@\w+` user handles.
  5. *Prefix Search:* Identifies words starting with specified prefix query.
  6. *Suffix Search:* Identifies words terminating in specified suffix query (e.g. `-ing`).
  7. *Word Search:* Isolates exact whole words avoiding partial false positives.

---

## Submission Compliance
The final submission document [`DSA03-NLP_CO1_AT3_Completed.docx`](./DSA03-NLP_CO1_AT3_Completed.docx) strictly complies with the global submission rules:
1. **Original Question Pages First:** Preserves all original prompt pages, instructions, cover page, and rubrics tables at the start.
2. **Clear Section Separation:** Inserts a page break and prominent institutional section divider.
3. **Comprehensive Solution Section:** Fully documents Problem Understanding, Specifications, Algorithmic Workflow, Modular Code, Verified Execution Output, and Performance/Test Case Handling for Sections 1, 2, and 3.
