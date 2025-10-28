import os
from pathlib import Path
import nltk
import re

os.makedirs("output", exist_ok=True)
stemmer = nltk.SnowballStemmer("english")

# define the regex
expReg = nltk.RegexpTokenizer(r"""
[A-Za-z0-9\+\_]+(?:-[A-Za-z0-9\+\_]+)*
|\d+(?:\.\d+)?(?:e[+\-]?\d+)?%?
|\$?\d+(?:\.\d+)?%?
|[\.!?]                
""", flags=re.VERBOSE)

def tokenize_file(file_path: str, normalize=False) -> list[str]:
    tokens = []
    with open(file_path, 'r') as file:
        content = file.read()
        tokens = expReg.tokenize(content)
        tokens = [token.lower() for token in tokens]
    if normalize:
        tokens = [stemmer.stem(token) for token in tokens]
    return tokens

