"""
Bag Generator Program: Sentence Reconstruction from an Unordered Bag of Words
=============================================================================
Course: DSA03 - Natural Language Processing
Assignment: Assignment 2, Question 2
Institution: SIMATS School of Engineering (Approved by AICTE | IET-UK)

Description:
Given an unordered multiset (bag) of words from an English sentence, this
program employs an N-gram language model (bigram with Laplace / Add-k smoothing)
and a Beam Search decoder to reconstruct the most probable original word order.

Task Formulation:
  W* = argmax_{W in Permutations(Bag)} P(W)
     = argmax_{W} [ P(w_1 | <s>) * prod_{i=2}^k P(w_i | w_{i-1}) * P(</s> | w_k) ]
"""

import math
import random
from collections import defaultdict, Counter
from typing import List, Tuple, Set

class NGramLanguageModel:
    """
    Bigram Language Model with Add-k (Laplace) Smoothing.
    Learns transition probabilities between adjacent word pairs from a training corpus.
    """
    def __init__(self, add_k: float = 0.5):
        self.add_k = add_k
        self.unigram_counts = Counter()
        self.bigram_counts = Counter()
        self.vocab = set()
        self.total_tokens = 0

    def train(self, corpus: List[List[str]]):
        """Train language model on a list of tokenized sentences."""
        for sentence in corpus:
            # Wrap sentence with explicit start and end boundary markers
            tokens = ['<s>'] + [w.lower() for w in sentence] + ['</s>']
            for i in range(len(tokens)):
                token = tokens[i]
                self.unigram_counts[token] += 1
                self.total_tokens += 1
                self.vocab.add(token)
                if i > 0:
                    prev_token = tokens[i - 1]
                    self.bigram_counts[(prev_token, token)] += 1

    @property
    def vocab_size(self) -> int:
        return len(self.vocab)

    def log_prob(self, w_prev: str, w_curr: str) -> float:
        """
        Compute smoothed bigram conditional log-probability log P(w_curr | w_prev):
        P*(w_curr | w_prev) = (C(w_prev, w_curr) + k) / (C(w_prev) + k * |V|)
        """
        w_prev_l = w_prev.lower()
        w_curr_l = w_curr.lower()
        
        c_bigram = self.bigram_counts.get((w_prev_l, w_curr_l), 0)
        c_unigram = self.unigram_counts.get(w_prev_l, 0)
        
        # Smoothed probability calculation
        numerator = c_bigram + self.add_k
        denominator = c_unigram + (self.add_k * self.vocab_size)
        prob = numerator / denominator
        return math.log(prob)

    def score_sequence(self, sequence: List[str]) -> float:
        """Score a complete sentence hypothesis including <s> and </s> boundaries."""
        tokens = ['<s>'] + [w.lower() for w in sequence] + ['</s>']
        total_log_prob = 0.0
        for i in range(1, len(tokens)):
            total_log_prob += self.log_prob(tokens[i - 1], tokens[i])
        return total_log_prob


class BagGenerator:
    """
    Bag Generator: Recovers sentence order from a multiset (bag) of words using
    heuristic Beam Search over the factorial permutation space.
    """
    def __init__(self, lm: NGramLanguageModel, beam_width: int = 50):
        self.lm = lm
        self.beam_width = beam_width

    def generate(self, bag: List[str]) -> Tuple[List[str], float]:
        """
        Finds the highest-scoring sequence of the words in `bag`.
        Returns: (reconstructed_word_list, total_log_prob)
        """
        n = len(bag)
        if n == 0:
            return [], 0.0
        if n == 1:
            score = self.lm.score_sequence(bag)
            return list(bag), score

        # Initialize beam with each unique candidate first word
        # State tuple: (accumulated_log_prob, [ordered_words], remaining_words_list)
        beam = []
        unique_starters = set(bag)
        for w in unique_starters:
            remaining = list(bag)
            remaining.remove(w)
            # Transition score from start marker <s> to w
            init_score = self.lm.log_prob('<s>', w)
            beam.append((init_score, [w], remaining))

        # Iteratively expand beam through all positions
        for step in range(1, n):
            candidates = []
            for accum_score, partial_seq, remaining in beam:
                last_word = partial_seq[-1]
                used_in_expansion = set()
                for next_word in remaining:
                    if next_word in used_in_expansion:
                        continue
                    used_in_expansion.add(next_word)
                    
                    new_remaining = list(remaining)
                    new_remaining.remove(next_word)
                    step_score = self.lm.log_prob(last_word, next_word)
                    new_accum_score = accum_score + step_score
                    candidates.append((new_accum_score, partial_seq + [next_word], new_remaining))

            # Prune candidates to top beam_width hypotheses
            candidates.sort(key=lambda item: item[0], reverse=True)
            beam = candidates[:self.beam_width]

        # Final step: Transition from final word to sentence terminal marker </s>
        completed_hypotheses = []
        for accum_score, full_seq, _ in beam:
            last_word = full_seq[-1]
            terminal_score = self.lm.log_prob(last_word, '</s>')
            total_score = accum_score + terminal_score
            completed_hypotheses.append((total_score, full_seq))

        completed_hypotheses.sort(key=lambda item: item[0], reverse=True)
        best_score, best_sequence = completed_hypotheses[0]
        return best_sequence, best_score


def main():
    print("=" * 70)
    print("DSA03 NLP Assignment 2 - Bag Generation Program Demonstration")
    print("=" * 70)

    # 1. Sample Domain Corpus
    raw_corpus = [
        "I want to eat Chinese food",
        "I want to spend money on lunch",
        "They want to eat lunch at a restaurant",
        "Chinese food is delicious to eat",
        "I want Chinese food for lunch today",
        "He likes to spend money on food",
        "We want to eat at a nice restaurant",
        "The nice restaurant serves Chinese food",
        "It is a nice night to eat out",
        "A guy and a doll eat lunch together",
        "This crap game is over a garage in Fifty-second Street",
        "Nobody ever takes the newspapers she sells",
        "He is a tall skinny guy with a mournful voice",
        "When a guy and a doll get to taking peeks back and forth"
    ]
    corpus = [s.split() for s in raw_corpus]

    # 2. Train Bigram Model
    lm = NGramLanguageModel(add_k=0.2)
    lm.train(corpus)
    print(f"[*] Language Model Trained: {len(corpus)} sentences | Vocab size: {lm.vocab_size} tokens")

    # 3. Test Sentences to Scramble and Reconstruct
    test_cases = [
        "I want to eat Chinese food",
        "It is a nice night",
        "We want to eat at a nice restaurant",
        "Nobody ever takes the newspapers she sells"
    ]

    generator = BagGenerator(lm, beam_width=100)

    print("\n[*] Reordering Scrambled Word Bags:")
    print("-" * 70)

    for i, sentence_str in enumerate(test_cases, start=1):
        original_tokens = sentence_str.split()
        bag = list(original_tokens)
        
        # Deterministically scramble bag
        random.seed(100 + i)
        random.shuffle(bag)

        reconstructed, score = generator.generate(bag)
        is_exact_match = (reconstructed == original_tokens)

        print(f"Test Case {i}:")
        print(f"  Original:      {' '.join(original_tokens)}")
        print(f"  Scrambled Bag: {' '.join(bag)}")
        print(f"  Reconstructed: {' '.join(reconstructed)}")
        print(f"  Log Likelihood: {score:.4f}")
        print(f"  Exact Match:    {'SUCCESS (Match!)' if is_exact_match else 'PARTIAL'}")
        print("-" * 70)

if __name__ == "__main__":
    main()
