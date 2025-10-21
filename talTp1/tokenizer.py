import os
from pathlib import Path
import nltk
import re

os.makedirs("output", exist_ok=True)

# define the regex
expReg = nltk.RegexpTokenizer(r"""
[A-Za-z0-9\+\_]+(?:-[A-Za-z0-9\+\_]+)*   # words, with +, _, or - inside
|\d+(?:\.\d+)?(?:e[+\-]?\d+)?%?          # numbers, floats, scientific notation, percentages
|\$?\d+(?:\.\d+)?%?                      # money values like $12.3 or 12.3%
""", flags=re.VERBOSE)


tokens = []

# path to the folder containing the text files
folder = Path('Data')
if not folder.is_dir():
    raise ValueError("The specified folder does not exist.")

# read each file and tokenize its content
for file_path in folder.glob('D*.txt'):
    with open(file_path, 'r') as file:
        content = file.read()
        tokens.extend(expReg.tokenize(content))

# save the tokens
print(f"Total tokens extracted: {len(tokens)}")
with open('output/T.txt', 'w') as token_file:
    for token in tokens:
        token_file.write(token + '\n')
