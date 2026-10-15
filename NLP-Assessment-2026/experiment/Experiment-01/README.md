# Experiment 1: Regular Expressions in Python

**Course:** DSA0311 - Natural Language Processing  
**Lab Assignment:** Experiment 01  
**Problem Statement:** Write a program that demonstrates how to use regular expressions in Python to match and search for patterns in text.

---

## Code
```python
"""
Experiment 1: Regular Expressions in Python
Aim: Write a program that demonstrates how to use regular expressions in Python 
     to match and search for patterns in text.
"""

import re

def demonstrate_regex():
    sample_text = (
        "Welcome to NLP Lab 2026! Contact the administrator at admin@saveetha.ac.in "
        "or support@nlp-center.org. For urgent queries, call +91-9876543210 or 044-22334455. "
        "The project submission dates are 2026-10-25 and 2026-11-15. "
        "Natural Language Processing (NLP) enables computers to analyze human text."
    )

    print("=" * 70)
    print("EXPERIMENT 1: REGULAR EXPRESSIONS IN PYTHON")
    print("=" * 70)
    print("\n[Input Sample Text]:\n" + sample_text + "\n")

    # 1. re.search() - Search for the first occurrence of a pattern
    print("-" * 70)
    print("1. re.search() - Search for first occurrence of a date pattern (YYYY-MM-DD)")
    date_pattern = r"\b\d{4}-\d{2}-\d{2}\b"
    search_result = re.search(date_pattern, sample_text)
    if search_result:
        print(f"   Found: '{search_result.group()}' at position {search_result.span()}")

    # 2. re.match() - Match a pattern at the very beginning of the string
    print("-" * 70)
    print("2. re.match() - Match prefix pattern at string start")
    match_result = re.match(r"Welcome\s+to\s+([A-Za-z0-9\s]+)!", sample_text)
    if match_result:
        print(f"   Matched: '{match_result.group()}' | Extracted Group: '{match_result.group(1)}'")

    # 3. re.findall() - Find all email addresses and phone numbers
    print("-" * 70)
    print("3. re.findall() - Extract all occurrences")
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    emails = re.findall(email_pattern, sample_text)
    print(f"   Extracted Emails ({len(emails)}): {emails}")

    phone_pattern = r"(?:\+91[\-\s]?|0\d{2,4}[\-\s]?)?\d{8,10}"
    phones = re.findall(phone_pattern, sample_text)
    print(f"   Extracted Phone Numbers ({len(phones)}): {phones}")

    # 4. re.finditer() - Iterate over all occurrences with span positions
    print("-" * 70)
    print("4. re.finditer() - Find all acronyms / capitalized abbreviations")
    acronym_pattern = r"\b[A-Z]{2,}\b"
    print("   Matches found with positions:")
    for m in re.finditer(acronym_pattern, sample_text):
        print(f"   - Match: '{m.group()}', Start: {m.start()}, End: {m.end()}")

    # 5. re.sub() - Pattern substitution and data sanitization
    print("-" * 70)
    print("5. re.sub() - Mask sensitive contact emails and standardize format")
    masked_text = re.sub(email_pattern, "[CONFIDENTIAL EMAIL]", sample_text)
    print(f"   Sanitized Text Preview:\n   {masked_text[:120]}...")

    # 6. re.split() - Pattern-based splitting
    print("-" * 70)
    print("6. re.split() - Split sentence by punctuation marks")
    sentences = re.split(r"[.!?]\s+", sample_text)
    for idx, s in enumerate(sentences, 1):
        if s.strip():
            print(f"   Sentence {idx}: {s.strip()}")

    print("=" * 70)
    print("EXPERIMENT 1 COMPLETED SUCCESSFULLY")
    print("=" * 70)

if __name__ == "__main__":
    demonstrate_regex()
```

---

## Output
```text
======================================================================
EXPERIMENT 1: REGULAR EXPRESSIONS IN PYTHON
======================================================================

[Input Sample Text]:
Welcome to NLP Lab 2026! Contact the administrator at admin@saveetha.ac.in or support@nlp-center.org. For urgent queries, call +91-9876543210 or 044-22334455. The project submission dates are 2026-10-25 and 2026-11-15. Natural Language Processing (NLP) enables computers to analyze human text.

----------------------------------------------------------------------
1. re.search() - Search for first occurrence of a date pattern (YYYY-MM-DD)
   Found: '2026-10-25' at position (192, 202)
----------------------------------------------------------------------
2. re.match() - Match prefix pattern at string start
   Matched: 'Welcome to NLP Lab 2026!' | Extracted Group: 'NLP Lab 2026'
----------------------------------------------------------------------
3. re.findall() - Extract all occurrences
   Extracted Emails (2): ['admin@saveetha.ac.in', 'support@nlp-center.org']
   Extracted Phone Numbers (2): ['+91-9876543210', '044-22334455']
----------------------------------------------------------------------
4. re.finditer() - Find all acronyms / capitalized abbreviations
   Matches found with positions:
   - Match: 'NLP', Start: 11, End: 14
   - Match: 'NLP', Start: 248, End: 251
----------------------------------------------------------------------
5. re.sub() - Mask sensitive contact emails and standardize format
   Sanitized Text Preview:
   Welcome to NLP Lab 2026! Contact the administrator at [CONFIDENTIAL EMAIL] or [CONFIDENTIAL EMAIL]. For urgent queries, ...
----------------------------------------------------------------------
6. re.split() - Split sentence by punctuation marks
   Sentence 1: Welcome to NLP Lab 2026
   Sentence 2: Contact the administrator at admin@saveetha.ac.in or support@nlp-center.org
   Sentence 3: For urgent queries, call +91-9876543210 or 044-22334455
   Sentence 4: The project submission dates are 2026-10-25 and 2026-11-15
   Sentence 5: Natural Language Processing (NLP) enables computers to analyze human text.
======================================================================
EXPERIMENT 1 COMPLETED SUCCESSFULLY
======================================================================
```
