import matplotlib.pyplot as plt
from wordcloud import WordCloud

def load_tokens(filepath):
    with open(filepath, "r") as f:
        return [line.strip() for line in f if line.strip()]

tokens = " ".join(load_tokens("output/T.txt"))

normalized_tokens = " ".join(load_tokens("output/T_N.txt"))

wordCloud = WordCloud(width=800, height=400, background_color='white').generate(tokens)

plt.figure(figsize=(10, 5))
plt.title("Word Cloud of Original Tokens")
plt.imshow(wordCloud, interpolation='bilinear')
plt.axis("off")
plt.savefig("output/wordcloud_original.png")

wordCloudNorm = WordCloud(width=800, height=400, background_color='white').generate(normalized_tokens)
plt.figure(figsize=(10, 5))
plt.title("Word Cloud of Normalized Tokens")
plt.imshow(wordCloudNorm, interpolation='bilinear')
plt.axis("off")
plt.savefig("output/wordcloud_normalized.png")
