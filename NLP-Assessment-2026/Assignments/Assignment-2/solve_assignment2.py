import numpy as np
import matplotlib.pyplot as plt
import random

# =============================================================================
# QUESTION 1: Berkeley Restaurant Project Add-1 Smoothing Computation
# =============================================================================
words = ['i', 'want', 'to', 'eat', 'chinese', 'food', 'lunch', 'spend']
V = 1446

unigrams = {
    'i': 2533,
    'want': 927,
    'to': 2417,
    'eat': 746,
    'chinese': 158,
    'food': 1093,
    'lunch': 341,
    'spend': 278
}

raw_counts = np.array([
    [5, 827, 0, 9, 0, 0, 0, 2],
    [2, 0, 608, 1, 6, 6, 5, 1],
    [2, 0, 4, 686, 2, 0, 6, 211],
    [0, 0, 2, 0, 16, 2, 42, 0],
    [1, 0, 0, 0, 0, 82, 1, 0],
    [15, 0, 15, 0, 1, 4, 0, 0],
    [2, 0, 0, 0, 0, 1, 0, 0],
    [1, 0, 1, 0, 0, 0, 0, 0]
], dtype=float)

# Raw MLE Probabilities P_MLE(w_i | w_{i-1}) = C(w_{i-1}, w_i) / C(w_{i-1})
raw_probs = np.zeros_like(raw_counts)
for idx, w in enumerate(words):
    raw_probs[idx] = raw_counts[idx] / unigrams[w]

# Add-1 Smoothed Probabilities P*(w_i | w_{i-1}) = (C(w_{i-1}, w_i) + 1) / (C(w_{i-1}) + V)
add1_probs = np.zeros_like(raw_counts)
for idx, w in enumerate(words):
    add1_probs[idx] = (raw_counts[idx] + 1) / (unigrams[w] + V)

# Add-1 Smoothed Counts c*(w_{i-1}, w_i) = (C(w_{i-1}, w_i) + 1) * C(w_{i-1}) / (C(w_{i-1}) + V)
add1_counts = np.zeros_like(raw_counts)
for idx, w in enumerate(words):
    add1_counts[idx] = ((raw_counts[idx] + 1) * unigrams[w]) / (unigrams[w] + V)

print("Q1 computations complete.")

# Plot comparison chart for Question 1
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=300)

im1 = ax1.imshow(raw_counts, cmap='YlGnBu')
ax1.set_xticks(range(8))
ax1.set_yticks(range(8))
ax1.set_xticklabels(words, rotation=45, ha='right', fontsize=9, fontweight='bold')
ax1.set_yticklabels(words, fontsize=9, fontweight='bold')
ax1.set_title('Raw Bigram Counts C(w_{i-1}, w_i)', fontsize=12, fontweight='bold', pad=10)
for i in range(8):
    for j in range(8):
        val = int(raw_counts[i, j])
        ax1.text(j, i, str(val), ha='center', va='center', fontsize=8.5,
                 color='white' if val > 200 else 'black')

im2 = ax2.imshow(add1_counts, cmap='YlGnBu')
ax2.set_xticks(range(8))
ax2.set_yticks(range(8))
ax2.set_xticklabels(words, rotation=45, ha='right', fontsize=9, fontweight='bold')
ax2.set_yticklabels(words, fontsize=9, fontweight='bold')
ax2.set_title('Add-1 Smoothed Counts c*(w_{i-1}, w_i)', fontsize=12, fontweight='bold', pad=10)
for i in range(8):
    for j in range(8):
        val = add1_counts[i, j]
        ax2.text(j, i, f'{val:.1f}', ha='center', va='center', fontsize=8.5,
                 color='white' if val > 150 else 'black')

plt.tight_layout()
chart_path = r'c:\Users\mithu\OneDrive\Desktop\DSA0311 - NATURAL LANGUAGE PROCESSING\NLP-Assessment-2026\Assignments\Assignment-2\add1_smoothing_comparison.png'
plt.savefig(chart_path, bbox_inches='tight')
plt.close()
print("Q1 comparison chart saved to:", chart_path)

# =============================================================================
# QUESTION 2: Bag Generation Program (Demonstration & Verification)
# =============================================================================
class BigramLanguageModel:
    def __init__(self, add_k=1.0):
        self.add_k = add_k
        self.unigram_counts = {}
        self.bigram_counts = {}
        self.vocab = set()
        self.total_words = 0

    def train(self, corpus_sentences):
        for sentence in corpus_sentences:
            tokens = ['<s>'] + [w.lower() for w in sentence] + ['</s>']
            for i in range(len(tokens)):
                w = tokens[i]
                self.unigram_counts[w] = self.unigram_counts.get(w, 0) + 1
                self.total_words += 1
                self.vocab.add(w)
                if i > 0:
                    prev = tokens[i-1]
                    bg = (prev, w)
                    self.bigram_counts[bg] = self.bigram_counts.get(bg, 0) + 1

    def bigram_log_prob(self, w_prev, w_curr):
        c_bg = self.bigram_counts.get((w_prev, w_curr), 0)
        c_ug = self.unigram_counts.get(w_prev, 0)
        v = len(self.vocab)
        prob = (c_bg + self.add_k) / (c_ug + self.add_k * v)
        return np.log(prob)

    def score_sequence(self, word_seq):
        tokens = ['<s>'] + list(word_seq) + ['</s>']
        total_log_prob = 0.0
        for i in range(1, len(tokens)):
            total_log_prob += self.bigram_log_prob(tokens[i-1], tokens[i])
        return total_log_prob

class BagGenerator:
    def __init__(self, lm, beam_width=50):
        self.lm = lm
        self.beam_width = beam_width

    def generate(self, bag_of_words):
        # Beam search for bag generation
        # State: (log_prob, [selected_words], remaining_multiset_tuple)
        n = len(bag_of_words)
        
        # Initial beam: starting after <s>
        # Candidate first words
        unique_starts = set(bag_of_words)
        beam = []
        for w in unique_starts:
            rem = list(bag_of_words)
            rem.remove(w)
            lp = self.lm.bigram_log_prob('<s>', w)
            beam.append((lp, [w], rem))
            
        # Expand step by step
        for step in range(1, n):
            candidates = []
            for lp, seq, rem in beam:
                prev_word = seq[-1]
                used_in_step = set()
                for next_w in rem:
                    if next_w in used_in_step:
                        continue
                    used_in_step.add(next_w)
                    new_rem = list(rem)
                    new_rem.remove(next_w)
                    step_lp = self.lm.bigram_log_prob(prev_word, next_w)
                    candidates.append((lp + step_lp, seq + [next_w], new_rem))
            # Sort and prune to beam width
            candidates.sort(key=lambda x: x[0], reverse=True)
            beam = candidates[:self.beam_width]

        # Final transition to </s>
        final_candidates = []
        for lp, seq, _ in beam:
            end_lp = self.lm.bigram_log_prob(seq[-1], '</s>')
            final_candidates.append((lp + end_lp, seq))
        final_candidates.sort(key=lambda x: x[0], reverse=True)
        return final_candidates[0][1], final_candidates[0][0]

# Sample corpus
training_data = [
    "i want to eat chinese food".split(),
    "i want to spend money on lunch".split(),
    "they want to eat lunch at a restaurant".split(),
    "chinese food is delicious to eat".split(),
    "i want chinese food for lunch today".split(),
    "he likes to spend money on food".split(),
    "we want to eat at a nice restaurant".split(),
    "the nice restaurant serves chinese food".split(),
    "it is a nice night to eat out".split(),
    "a guy and a doll eat lunch together".split()
]

lm = BigramLanguageModel(add_k=0.1)
lm.train(training_data)
generator = BagGenerator(lm, beam_width=50)

test_sentences = [
    "i want to eat chinese food".split(),
    "it is a nice night".split(),
    "we want to eat at a nice restaurant".split()
]

print("\n=== Bag Generator Demonstration ===")
for orig in test_sentences:
    bag = list(orig)
    random.seed(42)
    random.shuffle(bag)
    reconstructed, score = generator.generate(bag)
    print(f"Original:      {' '.join(orig)}")
    print(f"Shuffled Bag:  {' '.join(bag)}")
    print(f"Reconstructed: {' '.join(reconstructed)} (Log-Prob Score: {score:.3f})")
    print(f"Match Success: {orig == reconstructed}\n")
