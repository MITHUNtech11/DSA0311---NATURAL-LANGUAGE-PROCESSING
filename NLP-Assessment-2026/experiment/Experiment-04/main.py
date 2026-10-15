"""
Experiment 4: Finite-State Machine for Morphological Parsing
Aim: Implement a finite-state machine for morphological parsing. In this example, 
     we'll create a simple machine to generate plural forms of English nouns using Python.
"""

from typing import Tuple, Dict

class NounPluralFSM:
    """
    Finite-State Morphological Transducer for English Noun Pluralization.
    
    Models morphological rules as deterministic state transitions based on
    stem terminal characters and morphological classification.
    """
    def __init__(self):
        # State definitions
        self.STATES = {
            "START": "Initial State",
            "IRREGULAR": "Irregular / Stem Mutation",
            "INVARIANT": "Zero-Plural / Invariant",
            "SIBILANT": "Sibilant Suffix State (+es)",
            "Y_CONSONANT": "Consonant + Y Suffix State (y -> ies)",
            "Y_VOWEL": "Vowel + Y Suffix State (+s)",
            "F_FE": "Fricative F/FE State (f/fe -> ves)",
            "O_ENDING": "O-Ending State (+es / +s)",
            "DEFAULT": "Default Regular State (+s)"
        }
        
        # Irregular mapping
        self.irregular_nouns: Dict[str, str] = {
            "child": "children",
            "man": "men",
            "woman": "women",
            "tooth": "teeth",
            "foot": "feet",
            "mouse": "mice",
            "person": "people",
            "ox": "oxen",
            "goose": "geese"
        }
        
        # Invariant (zero-marked plural) nouns
        self.invariant_nouns = {"sheep", "deer", "fish", "series", "species", "aircraft"}
        
        # Sibilant endings: -s, -x, -z, -ch, -sh
        self.sibilants = ("s", "x", "z", "ch", "sh")
        
        # Voicing f/fe -> ves
        self.f_to_ves = {
            "leaf": "leaves",
            "knife": "knives",
            "life": "lives",
            "wife": "wives",
            "wolf": "wolves",
            "half": "halves",
            "thief": "thieves",
            "calf": "calves"
        }

        self.vowels = set("aeiou")

    def parse_and_pluralize(self, noun: str) -> Tuple[str, str, str]:
        """
        Parses singular noun and generates plural form along with the FSM state used.
        Returns: (plural_form, state_name, rule_description)
        """
        w = noun.strip().lower()
        if not w:
            return ("", "ERROR", "Empty input")

        # 1. Check Irregular Lexicon
        if w in self.irregular_nouns:
            return (self.irregular_nouns[w], "IRREGULAR", "Lexical stem mutation")

        # 2. Check Invariant Lexicon
        if w in self.invariant_nouns:
            return (w, "INVARIANT", "Zero-morpheme plural (unchanged)")

        # 3. Check -f / -fe Voicing
        if w in self.f_to_ves:
            return (self.f_to_ves[w], "F_FE", "Voicing shift: 'f/fe' -> 'ves'")

        # 4. Check Sibilants: -s, -x, -z, -ch, -sh
        if any(w.endswith(sib) for sib in self.sibilants):
            return (w + "es", "SIBILANT", "Stem ends with sibilant (append '-es')")

        # 5. Check Ending in 'y'
        if w.endswith("y"):
            if len(w) > 1 and w[-2] in self.vowels:
                return (w + "s", "Y_VOWEL", "Vowel + 'y' sequence (append '-s')")
            else:
                return (w[:-1] + "ies", "Y_CONSONANT", "Consonant + 'y' sequence ('y' -> '-ies')")

        # 6. Check Ending in 'o' preceded by consonant
        if w.endswith("o") and len(w) > 1 and w[-2] not in self.vowels:
            if w in {"potato", "tomato", "hero", "echo", "torpedo"}:
                return (w + "es", "O_ENDING", "Consonant + 'o' (append '-es')")

        # 7. Default Regular Noun
        return (w + "s", "DEFAULT", "Regular morphological default (append '-s')")

def run_experiment():
    print("=" * 80)
    print("EXPERIMENT 4: FINITE-STATE MACHINE FOR MORPHOLOGICAL PARSING (NOUN PLURALS)")
    print("=" * 80)

    fsm = NounPluralFSM()

    test_nouns = [
        # Regular
        "cat", "book", "computer",
        # Sibilants
        "bus", "box", "buzz", "watch", "dish",
        # Consonant + y vs Vowel + y
        "baby", "city", "category", "boy", "day",
        # F / FE endings
        "leaf", "knife", "wolf", "life",
        # Consonant + O
        "hero", "potato",
        # Irregular & Invariant
        "child", "man", "tooth", "mouse", "sheep", "deer", "species"
    ]

    print("\n[FSM Morphological Parsing States]")
    for st, desc in fsm.STATES.items():
        print(f" - {st:<12}: {desc}")

    print("\n" + "=" * 80)
    print("MORPHOLOGICAL PARSING & PLURAL GENERATION RESULTS")
    print("=" * 80)
    print(f"{'Singular Noun':<16} | {'Plural Output':<18} | {'FSM State':<14} | {'Rule Applied'}")
    print("-" * 80)

    for noun in test_nouns:
        plural, state, rule = fsm.parse_and_pluralize(noun)
        print(f"{noun:<16} | {plural:<18} | {state:<14} | {rule}")

    print("=" * 80)
    print("EXPERIMENT 4 COMPLETED SUCCESSFULLY")
    print("=" * 80)

if __name__ == "__main__":
    run_experiment()
