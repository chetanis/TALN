
import os
os.makedirs("output", exist_ok=True)


def load_tokens(filepath):
    with open(filepath, "r") as f:
        return [line.strip() for line in f if line.strip()]

tokens = load_tokens('T.txt')
tokens_normalized = load_tokens('T_N.txt')

vocab = sorted(set(tokens))
vocab_normalized = sorted(set(tokens_normalized))

with open('output/V.txt', "w") as f:
    for word in vocab:
        f.write(word + "\n")

with open('output/V_N.txt', "w") as f:
    for word in vocab_normalized:
        f.write(word + "\n")

print(f"tokens size: {len(tokens)}")
print(f"Vocabulary size: {len(vocab)}")