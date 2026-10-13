"""
NLTK Demonstration Script
=========================
Course: DSA0311 - Natural Language Processing
Purpose: Demonstrate core NLTK capabilities on sample sentences:
  1. Sentence & Word Tokenization
  2. Stopword Filtering
  3. Stemming (Porter, Lancaster, Snowball)
  4. Lemmatization (WordNet with POS context)
  5. Part-of-Speech (POS) Tagging
  6. Named Entity Recognition (NER / Chunking)
  7. N-grams (Bigrams & Trigrams)
  8. Frequency Distribution (FreqDist)
  9. Sentiment Analysis (VADER)
"""

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import PorterStemmer, LancasterStemmer, SnowballStemmer, WordNetLemmatizer
from nltk import pos_tag, ne_chunk
from nltk.util import ngrams
from nltk.probability import FreqDist
from nltk.sentiment import SentimentIntensityAnalyzer


def ensure_nltk_resources():
    """Ensure all required NLTK datasets and models are downloaded."""
    resources = [
        "punkt",
        "punkt_tab",
        "stopwords",
        "wordnet",
        "averaged_perceptron_tagger",
        "averaged_perceptron_tagger_eng",
        "maxent_ne_chunker",
        "maxent_ne_chunker_tab",
        "words",
        "vader_lexicon",
    ]
    for res in resources:
        try:
            nltk.download(res, quiet=True)
        except Exception as e:
            print(f"Notice: Failed to download {res}: {e}")


def get_wordnet_pos(treebank_tag):
    """Map POS tag to first character lemmatize() accepts."""
    if treebank_tag.startswith("J"):
        return wordnet.ADJ
    elif treebank_tag.startswith("V"):
        return wordnet.VERB
    elif treebank_tag.startswith("N"):
        return wordnet.NOUN
    elif treebank_tag.startswith("R"):
        return wordnet.ADV
    else:
        return wordnet.NOUN


def run_pipeline():
    ensure_nltk_resources()

    sample_paragraph = (
        "Natural Language Processing with NLTK is remarkably versatile and exciting to learn. "
        "Dr. Eleanor Smith visited Google headquarters in Mountain View, California on July 14, 2024. "
        "The striped bats are hanging upside down while flying swiftly through old abandoned caves. "
        "Although the food service was slow and frustrating, the dessert tasted surprisingly exquisite!"
    )

    print("=" * 80)
    print(" NLTK DEMONSTRATION ON SAMPLE SENTENCES")
    print("=" * 80)
    print(f"\n[Original Text]:\n{sample_paragraph}\n")

    # 1. Sentence Tokenization
    print("-" * 80)
    print("1. SENTENCE TOKENIZATION (`sent_tokenize`)")
    print("-" * 80)
    sentences = sent_tokenize(sample_paragraph)
    for idx, sent in enumerate(sentences, 1):
        print(f"  Sentence {idx}: {sent}")

    # 2. Word Tokenization & Punctuation Handling
    print("\n" + "-" * 80)
    print("2. WORD TOKENIZATION (`word_tokenize`)")
    print("-" * 80)
    sample_sentence = sentences[1]
    tokens = word_tokenize(sample_sentence)
    print(f"  Input Sentence: \"{sample_sentence}\"")
    print(f"  Tokens ({len(tokens)}): {tokens}")

    # 3. Stopword Removal
    print("\n" + "-" * 80)
    print("3. STOPWORDS REMOVAL (`stopwords.words('english')`)")
    print("-" * 80)
    stop_words = set(stopwords.words("english"))
    all_tokens = [w for sent in sentences for w in word_tokenize(sent)]
    filtered_words = [w for w in all_tokens if w.isalpha() and w.lower() not in stop_words]
    removed_words = [w for w in all_tokens if w.isalpha() and w.lower() in stop_words]
    print(f"  Total alphabetical tokens: {len([w for w in all_tokens if w.isalpha()])}")
    print(f"  Filtered tokens (content words, first 15): {filtered_words[:15]}")
    print(f"  Detected stopwords (sample): {list(set(removed_words))[:10]}")

    # 4. Stemming Comparison
    print("\n" + "-" * 80)
    print("4. STEMMING COMPARISON (Porter vs Lancaster vs Snowball)")
    print("-" * 80)
    test_words = ["hanging", "flying", "caves", "remarkably", "exquisite", "frustrating", "abandoned", "stripes"]
    porter = PorterStemmer()
    lancaster = LancasterStemmer()
    snowball = SnowballStemmer("english")

    print(f"  {'Original Word':<15} | {'Porter':<15} | {'Lancaster':<15} | {'Snowball':<15}")
    print("  " + "-" * 63)
    for w in test_words:
        print(f"  {w:<15} | {porter.stem(w):<15} | {lancaster.stem(w):<15} | {snowball.stem(w):<15}")

    # 5. Lemmatization with POS context
    print("\n" + "-" * 80)
    print("5. LEMMATIZATION (`WordNetLemmatizer` with POS Awareness)")
    print("-" * 80)
    lemmatizer = WordNetLemmatizer()
    morph_sentence = sentences[2]
    morph_tokens = word_tokenize(morph_sentence)
    pos_tagged_tokens = pos_tag(morph_tokens)

    print(f"  Input Sentence: \"{morph_sentence}\"")
    print(f"  {'Token':<12} | {'POS Tag':<8} | {'Default Lemmatize':<18} | {'POS-Aware Lemmatize'}")
    print("  " + "-" * 65)
    for token, tag in pos_tagged_tokens:
        if token.isalpha():
            wn_pos = get_wordnet_pos(tag)
            lemma_def = lemmatizer.lemmatize(token.lower())
            lemma_pos = lemmatizer.lemmatize(token.lower(), pos=wn_pos)
            print(f"  {token:<12} | {tag:<8} | {lemma_def:<18} | {lemma_pos}")

    # 6. Part-of-Speech Tagging
    print("\n" + "-" * 80)
    print("6. PART-OF-SPEECH (POS) TAGGING (`pos_tag`)")
    print("-" * 80)
    first_sent_tokens = word_tokenize(sentences[0])
    first_sent_pos = pos_tag(first_sent_tokens)
    print(f"  Sentence: \"{sentences[0]}\"")
    print(f"  POS Tags: {first_sent_pos}")

    # 7. Named Entity Recognition (NER)
    print("\n" + "-" * 80)
    print("7. NAMED ENTITY RECOGNITION (`ne_chunk`)")
    print("-" * 80)
    ner_sentence = sentences[1]
    ner_tokens = word_tokenize(ner_sentence)
    ner_pos = pos_tag(ner_tokens)
    ner_tree = ne_chunk(ner_pos)
    print(f"  Sentence: \"{ner_sentence}\"")
    print("  Extracted Named Entities:")
    found_entities = False
    for subtree in ner_tree:
        if hasattr(subtree, "label"):
            entity_name = " ".join([token for token, tag in subtree.leaves()])
            entity_type = subtree.label()
            print(f"    - [{entity_type}]: {entity_name}")
            found_entities = True
    if not found_entities:
        print("    (No named entities detected)")

    # 8. N-grams (Bigrams & Trigrams)
    print("\n" + "-" * 80)
    print("8. N-GRAM EXTRACTION (`ngrams`)")
    print("-" * 80)
    sample_clean_tokens = [w.lower() for w in word_tokenize(sentences[0]) if w.isalpha()]
    bigrams_list = list(ngrams(sample_clean_tokens, 2))
    trigrams_list = list(ngrams(sample_clean_tokens, 3))
    print(f"  Clean Tokens: {sample_clean_tokens}")
    print(f"  Bigrams (2-grams): {bigrams_list[:5]} ... (total {len(bigrams_list)})")
    print(f"  Trigrams (3-grams): {trigrams_list[:4]} ... (total {len(trigrams_list)})")

    # 9. Frequency Distribution (FreqDist)
    print("\n" + "-" * 80)
    print("9. FREQUENCY DISTRIBUTION (`FreqDist`)")
    print("-" * 80)
    all_clean_words = [w.lower() for w in all_tokens if w.isalpha()]
    fdist = FreqDist(all_clean_words)
    print(f"  Total Words: {fdist.N()}, Unique Vocabulary: {fdist.B()}")
    print(f"  Top 5 Most Common Words: {fdist.most_common(5)}")

    # 10. Sentiment Analysis with VADER
    print("\n" + "-" * 80)
    print("10. SENTIMENT ANALYSIS (`SentimentIntensityAnalyzer` / VADER)")
    print("-" * 80)
    sia = SentimentIntensityAnalyzer()
    for idx, sent in enumerate(sentences, 1):
        scores = sia.polarity_scores(sent)
        comp = scores["compound"]
        label = "POSITIVE" if comp >= 0.05 else ("NEGATIVE" if comp <= -0.05 else "NEUTRAL")
        print(f"  Sentence {idx}: \"{sent}\"")
        print(f"    -> Scores: {scores} => Sentiment: {label}")

    print("\n" + "=" * 80)
    print(" NLTK DEMONSTRATION COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    run_pipeline()
