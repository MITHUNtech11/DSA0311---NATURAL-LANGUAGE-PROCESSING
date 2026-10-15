# Experiment 5: Word Stemming using Porter Stemmer Algorithm

**Course:** DSA0311 - Natural Language Processing  
**Lab Assignment:** Experiment 05  
**Problem Statement:** Use the Porter Stemmer algorithm to perform word stemming on a list of words using python libraries.

---

## Code
```python
"""
Experiment 5: Word Stemming using Porter Stemmer Algorithm
Aim: Use the Porter Stemmer algorithm to perform word stemming on a list of words 
     using Python libraries (NLTK).
"""

from nltk.stem import PorterStemmer, LancasterStemmer, SnowballStemmer

def run_experiment():
    print("=" * 85)
    print("EXPERIMENT 5: WORD STEMMING USING PORTER STEMMER ALGORITHM")
    print("=" * 85)

    # Initialize stemmers
    porter = PorterStemmer()
    lancaster = LancasterStemmer()
    snowball = SnowballStemmer(language="english")

    # Curated word list with morphological families and edge cases
    word_families = [
        # Connection family
        ["connect", "connected", "connecting", "connection", "connections"],
        # Compute family
        ["compute", "computer", "computing", "computation", "computational"],
        # General linguistic variations
        ["programming", "programmer", "programs", "programmable"],
        ["happily", "happiness", "happy", "happier"],
        ["caring", "careful", "careless", "cared"],
        ["organization", "organize", "organizing", "organizer"],
        ["university", "universe", "universal"],
        ["study", "studying", "studies", "studied"]
    ]

    print("\n[Part 1: Porter Stemmer on Word Families]")
    print(f"{'Original Word':<18} | {'Porter Stem':<15}")
    print("-" * 38)
    for family in word_families:
        for word in family:
            stemmed = porter.stem(word)
            print(f"{word:<18} | {stemmed:<15}")
        print("-" * 38)

    # Comparative analysis across popular stemming algorithms
    print("\n[Part 2: Comparative Stemming Benchmark (Porter vs Snowball vs Lancaster)]")
    benchmark_words = [
        "connect", "connection", "connections",
        "trouble", "troubling", "troubled",
        "maximum", "multiply", "multimedia",
        "provision", "provisional",
        "friendship", "friendly", "friend",
        "university", "universe",
        "flying", "flies", "flight"
    ]

    print(f"{'Input Word':<16} | {'Porter (1980)':<16} | {'Snowball (Porter2)':<20} | {'Lancaster (Aggressive)'}")
    print("=" * 85)
    for w in benchmark_words:
        p_stem = porter.stem(w)
        s_stem = snowball.stem(w)
        l_stem = lancaster.stem(w)
        print(f"{w:<16} | {p_stem:<16} | {s_stem:<20} | {l_stem}")
    print("=" * 85)

    # Sentence Stemming Demonstration
    sample_sentence = "The artificial intelligence researchers are developing algorithms for automated translation and understanding."
    print("\n[Part 3: Sentence-Level Stemming Transformation]")
    print(f"Input Sentence:\n\"{sample_sentence}\"\n")
    tokens = sample_sentence.replace(".", "").split()
    stemmed_tokens = [porter.stem(t) for t in tokens]
    print(f"{'Original Token':<18} -> {'Stemmed Token'}")
    print("-" * 40)
    for orig, st in zip(tokens, stemmed_tokens):
        print(f"{orig:<18} -> {st}")

    print("\nReconstructed Stemmed Sequence:")
    print(" ".join(stemmed_tokens))

    print("\n" + "=" * 85)
    print("EXPERIMENT 5 COMPLETED SUCCESSFULLY")
    print("=" * 85)

if __name__ == "__main__":
    run_experiment()
```

---

## Output
```text
=====================================================================================
EXPERIMENT 5: WORD STEMMING USING PORTER STEMMER ALGORITHM
=====================================================================================

[Part 1: Porter Stemmer on Word Families]
Original Word      | Porter Stem    
--------------------------------------
connect            | connect        
connected          | connect        
connecting         | connect        
connection         | connect        
connections        | connect        
--------------------------------------
compute            | comput         
computer           | comput         
computing          | comput         
computation        | comput         
computational      | comput         
--------------------------------------
programming        | program        
programmer         | programm       
programs           | program        
programmable       | programm       
--------------------------------------
happily            | happili        
happiness          | happi          
happy              | happi          
happier            | happier        
--------------------------------------
caring             | care           
careful            | care           
careless           | careless       
cared              | care           
--------------------------------------
organization       | organ          
organize           | organ          
organizing         | organ          
organizer          | organ          
--------------------------------------
university         | univers        
universe           | univers        
universal          | univers        
--------------------------------------
study              | studi          
studying           | studi          
studies            | studi          
studied            | studi          
--------------------------------------

[Part 2: Comparative Stemming Benchmark (Porter vs Snowball vs Lancaster)]
Input Word       | Porter (1980)    | Snowball (Porter2)   | Lancaster (Aggressive)
=====================================================================================
connect          | connect          | connect              | connect
connection       | connect          | connect              | connect
connections      | connect          | connect              | connect
trouble          | troubl           | troubl               | troubl
troubling        | troubl           | troubl               | troubl
troubled         | troubl           | troubl               | troubl
maximum          | maximum          | maximum              | maxim
multiply         | multipli         | multipli             | multiply
multimedia       | multimedia       | multimedia           | multimed
provision        | provis           | provis               | provid
provisional      | provision        | provision            | provid
friendship       | friendship       | friendship           | friend
friendly         | friendli         | friend               | friend
friend           | friend           | friend               | friend
university       | univers          | univers              | univers
universe         | univers          | univers              | univers
flying           | fli              | fli                  | fly
flies            | fli              | fli                  | fli
flight           | flight           | flight               | flight
=====================================================================================

[Part 3: Sentence-Level Stemming Transformation]
Input Sentence:
"The artificial intelligence researchers are developing algorithms for automated translation and understanding."

Original Token     -> Stemmed Token
----------------------------------------
The                -> the
artificial         -> artifici
intelligence       -> intellig
researchers        -> research
are                -> are
developing         -> develop
algorithms         -> algorithm
for                -> for
automated          -> autom
translation        -> translat
and                -> and
understanding      -> understand

Reconstructed Stemmed Sequence:
the artifici intellig research are develop algorithm for autom translat and understand

=====================================================================================
EXPERIMENT 5 COMPLETED SUCCESSFULLY
=====================================================================================
```
