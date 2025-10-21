import os
import nltk

os.makedirs("output", exist_ok=True)
stemmer = nltk.SnowballStemmer("english")


#read tokens and lowercase them
with open('T.txt', 'r') as token_file:
    tokens = [line.strip() for line in token_file if line.strip()]
tokens = [token.lower() for token in tokens]


stemmed_tokens = [stemmer.stem(token) for token in tokens]
print(tokens[:10]) 
print(stemmed_tokens[:10])  

with open('output/T_N.txt', 'w') as norm_file:
    for token in stemmed_tokens:
        norm_file.write(token + '\n')