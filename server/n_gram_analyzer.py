def calculate_unigrams(tokens):
    unigram_dict = {}
    for token in tokens:
        unigram_dict[token] = unigram_dict.get(token, 0) + 1
    
    results = []
    nb_tokens = len(tokens)
    for token, count in unigram_dict.items():
        results.append({
            'ngram': token,
            'count': count,
            'probability': count / nb_tokens
        })
    
    results.sort(key=lambda x: x['count'], reverse=True)
    return results, nb_tokens

def calculate_bigrams(tokens):
    # Calculate unigram counts for conditional probability
    unigram_dict = {}
    for token in tokens:
        unigram_dict[token] = unigram_dict.get(token, 0) + 1
    
    # Calculate bigram counts
    bigram_dict = {}
    for i in range(len(tokens) - 1):
        bigram = f"{tokens[i]} {tokens[i+1]}"
        bigram_dict[bigram] = bigram_dict.get(bigram, 0) + 1
    
    results = []
    nb_bigrams = len(tokens) - 1
    nb_tokens = len(tokens)
    
    for bigram, count in bigram_dict.items():
        w1, w2 = bigram.split(' ', 1)
        
        # Conditional probability: P(w2|w1) = count(w1 w2) / count(w1)
        conditional_prob = count / unigram_dict[w1]
        
        # Joint probability using chain rule: P(w1 w2) = P(w1) * P(w2|w1)
        joint_prob = (unigram_dict[w1] / nb_tokens) * conditional_prob
        
        results.append({
            'ngram': bigram,
            'count': count,
            'conditional_probability': conditional_prob,  # P(w2|w1)
            'probability': joint_prob  # P(w1, w2)
        })
    
    results.sort(key=lambda x: x['count'], reverse=True)
    return results, nb_bigrams

def calculate_trigrams(tokens):
    # Calculate unigram counts
    unigram_dict = {}
    for token in tokens:
        unigram_dict[token] = unigram_dict.get(token, 0) + 1
    
    # Calculate bigram counts for conditional probability
    bigram_dict = {}
    for i in range(len(tokens) - 1):
        bigram = f"{tokens[i]} {tokens[i+1]}"
        bigram_dict[bigram] = bigram_dict.get(bigram, 0) + 1
    
    # Calculate trigram counts
    trigram_dict = {}
    for i in range(len(tokens) - 2):
        trigram = f"{tokens[i]} {tokens[i+1]} {tokens[i+2]}"
        trigram_dict[trigram] = trigram_dict.get(trigram, 0) + 1
    
    results = []
    nb_trigrams = len(tokens) - 2
    nb_tokens = len(tokens)
    
    for trigram, count in trigram_dict.items():
        parts = trigram.split(' ', 2)
        w1, w2, w3 = parts[0], parts[1], parts[2]
        bigram_context = f"{w1} {w2}"
        
        # Conditional probability: P(w3|w1 w2) = count(w1 w2 w3) / count(w1 w2)
        conditional_prob = count / bigram_dict[bigram_context]
        
        # Joint probability using chain rule: P(w1 w2 w3) = P(w1) * P(w2|w1) * P(w3|w1 w2)
        p_w1 = unigram_dict[w1] / nb_tokens
        bigram_w1_w2 = f"{w1} {w2}"
        p_w2_given_w1 = bigram_dict[bigram_w1_w2] / unigram_dict[w1]
        joint_prob = p_w1 * p_w2_given_w1 * conditional_prob
        
        results.append({
            'ngram': trigram,
            'count': count,
            'conditional_probability': conditional_prob,  # P(w3|w1 w2)
            'probability': joint_prob  # P(w1, w2, w3)
        })
    
    results.sort(key=lambda x: x['count'], reverse=True)
    return results, nb_trigrams