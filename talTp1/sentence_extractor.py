import os
from pathlib import Path
from nltk.tokenize import RegexpTokenizer
os.makedirs("output", exist_ok=True)

sentence_tokenizer = RegexpTokenizer(r'[^.!?]+[.!?]')

all_sentences = []
articles = []

folder = Path('Data')
if not folder.is_dir():
    raise ValueError("The specified folder does not exist.")

# read each file and tokenize its content
for file_path in folder.glob('D*.txt'):
    with open(file_path, 'r') as file:
        content = file.read()
        articles.append(content)


for article in articles:  # articles = list of all article contents
    sentences = sentence_tokenizer.tokenize(article)
    all_sentences.extend(sentences)

with open("output/S.txt", "w", encoding="utf-8") as f:
    for sentence in all_sentences:
        f.write(sentence.strip() + "\n")
