import nltk

for resource in ['punkt', 'punkt_tab', 'stopwords']:
    try:
        nltk.data.find(f'tokenizers/{resource}')
        print(f"NLTK resource '{resource}' is already available.")
    except LookupError:
        print(f"Downloading NLTK resource: {resource}")
        nltk.download(resource)
