# Natural Language Processing Lab Experiments

**Course:** DSA0311 - Natural Language Processing  
**Academic Year:** 2026  
**Completed Submission Document:** [`DSA03-NLP_Lab_Experiments_1_to_5_Completed.docx`](./DSA03-NLP_Lab_Experiments_1_to_5_Completed.docx)  
**Original Prompt Document:** [`lab_program_list(1).docx`](./lab_program_list(1).docx)

---

## Lab Experiments (1 to 5)

| Exp # | Experiment Title | Directory & Code | Output Log |
|---|---|---|---|
| **01** | Regular Expressions for Pattern Matching and Searching | [`Experiment-01/main.py`](./Experiment-01/main.py) | [`Experiment-01/output.txt`](./Experiment-01/output.txt) |
| **02** | Finite State Automaton (DFA) Ending with 'ab' | [`Experiment-02/main.py`](./Experiment-02/main.py) | [`Experiment-02/output.txt`](./Experiment-02/output.txt) |
| **03** | Morphological Analysis using NLTK | [`Experiment-03/main.py`](./Experiment-03/main.py) | [`Experiment-03/output.txt`](./Experiment-03/output.txt) |
| **04** | Finite-State Machine for Morphological Parsing (Noun Plurals) | [`Experiment-04/main.py`](./Experiment-04/main.py) | [`Experiment-04/output.txt`](./Experiment-04/output.txt) |
| **05** | Word Stemming using Porter Stemmer Algorithm | [`Experiment-05/main.py`](./Experiment-05/main.py) | [`Experiment-05/output.txt`](./Experiment-05/output.txt) |

---

## Experiment Summaries

### [Experiment 1: Regular Expressions in Python](./Experiment-01/README.md)
* **Goal:** Demonstrates regular expression operations in Python using the `re` module.
* **Key Functions:** `re.search()`, `re.match()`, `re.findall()`, `re.finditer()`, `re.sub()`, `re.split()`.
* **Applications:** Date pattern extraction, prefix matching, email and phone extraction, acronym detection, email masking, and sentence tokenization.

### [Experiment 2: Finite State Automaton (DFA)](./Experiment-02/README.md)
* **Goal:** Implement a Deterministic Finite Automaton recognizing strings ending with `'ab'` over $\Sigma = \{a, b\}$.
* **Automaton Specs:** $Q = \{q_0, q_1, q_2\}$, Start State $= q_0$, Final State $= \{q_2\}$.
* **Testing:** Evaluates acceptance, state sequence traces, rejection on invalid endings, and error handling for out-of-alphabet characters.

### [Experiment 3: Morphological Analysis using NLTK](./Experiment-03/README.md)
* **Goal:** Perform linguistic morphological analysis on English text using NLTK.
* **Key Pipeline:** Word tokenization $\to$ POS tagging $\to$ Penn Treebank to WordNet mapping $\to$ Lemma extraction $\to$ Affix and inflectional category identification.

### [Experiment 4: Finite-State Machine for Morphological Parsing](./Experiment-04/README.md)
* **Goal:** FSM morphological transducer to generate plural forms of English nouns.
* **Rule States:** Irregular lexical mutation, Invariant / zero-plural nouns, Sibilant stems (`+es`), Consonant + y (`ies`), Vowel + y (`+s`), Voicing fricatives (`f/fe` $\to$ `ves`), and Default regular nouns (`+s`).

### [Experiment 5: Word Stemming using Porter Stemmer Algorithm](./Experiment-05/README.md)
* **Goal:** Apply the Porter Stemmer algorithm to reduce inflected/derived words to their root stems.
* **Coverage:** Stemming morphological word families, comparative analysis against Snowball (Porter2) and Lancaster stemmers, and sentence-level text transformation.

---

## Final Submission Document Compliance
The final submission document [`DSA03-NLP_Lab_Experiments_1_to_5_Completed.docx`](./DSA03-NLP_Lab_Experiments_1_to_5_Completed.docx) strictly adheres to the submission rules:
1. **Original Question Pages First:** The entire original syllabus content from `lab_program_list(1).docx` is preserved at the top.
2. **Page Break & Section Divider:** A clean divider and page break separates the syllabus and solutions.
3. **Streamlined Structure:** Each experiment strictly presents the **Code** and **Output** blocks formatted in clean monospace styles.
