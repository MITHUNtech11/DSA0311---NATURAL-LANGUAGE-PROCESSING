"""
Experiment 3: Morphological Analysis using NLTK
Aim: Write a program that demonstrates how to perform morphological analysis 
     using the NLTK library in Python.
"""

import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

class MorphologicalAnalyzer:
    """
    Performs morphological analysis on input sentences by combining POS tagging,
    affix identification, and WordNet-based lemmatization to extract base morphemes.
    """
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        
    @staticmethod
    def get_wordnet_pos(treebank_tag: str):
        """Maps Penn Treebank POS tags to WordNet POS categories."""
        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN  # Default fallback

    def analyze_word(self, word: str, pos_tag: str):
        """Analyzes word morphemes, base root, and inflectional characteristics."""
        wn_pos = self.get_wordnet_pos(pos_tag)
        lemma = self.lemmatizer.lemmatize(word.lower(), pos=wn_pos)
        
        # Identify morphological features & affixes
        inflection = "Base Form / Root"
        affix = "-"
        w_lower = word.lower()

        if pos_tag.startswith("NNS") and w_lower != lemma:
            inflection = "Noun Plural"
            affix = "-s / -es"
        elif pos_tag in ("VBD", "VBN") and w_lower != lemma:
            inflection = "Verb Past / Participle"
            affix = "-ed" if w_lower.endswith("ed") else "Irregular past"
        elif pos_tag == "VBG" and w_lower.endswith("ing"):
            inflection = "Verb Gerund / Pres. Participle"
            affix = "-ing"
        elif pos_tag == "VBZ" and w_lower != lemma:
            inflection = "Verb 3rd Person Singular"
            affix = "-s / -es"
        elif pos_tag == "JJR" and w_lower.endswith("er"):
            inflection = "Adjective Comparative"
            affix = "-er"
        elif pos_tag == "JJS" and w_lower.endswith("est"):
            inflection = "Adjective Superlative"
            affix = "-est"
        elif pos_tag.startswith("RB") and w_lower.endswith("ly"):
            inflection = "Adverb Derivational"
            affix = "-ly"

        return {
            "surface_token": word,
            "pos_tag": pos_tag,
            "wordnet_pos": wn_pos,
            "root_lemma": lemma,
            "inflection": inflection,
            "affix": affix
        }

    def analyze_text(self, text: str):
        """Tokenizes text and performs morphological breakdown for each token."""
        tokens = word_tokenize(text)
        pos_tagged = nltk.pos_tag(tokens)
        return [self.analyze_word(token, tag) for token, tag in pos_tagged if token.isalnum()]

def run_experiment():
    print("=" * 80)
    print("EXPERIMENT 3: MORPHOLOGICAL ANALYSIS USING NLTK")
    print("=" * 80)

    sample_sentences = [
        "The fastest runners were happily studying linguistic algorithms and analyzing texts.",
        "Children loved playing games while teachers evaluated their innovative ideas."
    ]

    analyzer = MorphologicalAnalyzer()

    for idx, sentence in enumerate(sample_sentences, 1):
        print(f"\n[Sentence {idx}]: \"{sentence}\"")
        analysis_results = analyzer.analyze_text(sentence)

        print("-" * 80)
        print(f"{'Surface Token':<16} | {'POS':<6} | {'Base Lemma':<14} | {'Affix':<10} | {'Morphological Category'}")
        print("-" * 80)
        for r in analysis_results:
            print(f"{r['surface_token']:<16} | {r['pos_tag']:<6} | {r['root_lemma']:<14} | {r['affix']:<10} | {r['inflection']}")
        print("-" * 80)

    print("\n" + "=" * 80)
    print("EXPERIMENT 3 COMPLETED SUCCESSFULLY")
    print("=" * 80)

if __name__ == "__main__":
    run_experiment()
