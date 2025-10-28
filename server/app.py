# Flask Backend (app.py)
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

from n_gram_analyzer import calculate_bigrams, calculate_trigrams, calculate_unigrams
from tokenizer import tokenize_file

app = Flask(__name__)
CORS(app)

DATA_FOLDER = 'Data'
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)


def process_tokens_with_boundaries(tokens):
    """Insert sentence boundary tokens <s> and </s> around sentences."""
    processed = []
    previous_token = '.'   
    for token in tokens:        
        if token in ['.', '?', '!']:
            processed.append('</s>')
        elif previous_token in ['.', '?', '!']:
            processed.append('<s>')
            processed.append(token)
        else:
            processed.append(token)
        previous_token = token
    
    return processed

@app.route('/api/files', methods=['GET'])
def get_files():
    """Get list of available token files"""
    files = [f for f in os.listdir(DATA_FOLDER) if f.endswith('.txt')]
    # sort by name
    files.sort()
    return jsonify({'files': files})

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Analyze n-grams from selected file"""
    data = request.json
    filename = data.get('filename')
    token_type = data.get('tokenType', 'normal')
    ngram_type = data.get('ngramType', 'unigram')
    
    if not filename:
        return jsonify({'error': 'No filename provided'}), 400
    
    filepath = os.path.join(DATA_FOLDER, filename)
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
    
    try:
        # Load and process tokens
        normalize = token_type == 'normalized'
        tokens = tokenize_file(filepath, normalize)
        processed_tokens = process_tokens_with_boundaries(tokens)
        
        # Calculate n-grams based on type
        if ngram_type == 'unigram':
            results, total_count = calculate_unigrams(processed_tokens)
        elif ngram_type == 'bigram':
            results, total_count = calculate_bigrams(processed_tokens)
        elif ngram_type == 'trigram':
            results, total_count = calculate_trigrams(processed_tokens)
        else:
            return jsonify({'error': 'Invalid n-gram type'}), 400
        
        return jsonify({
            'results': results,
            'totalCount': total_count,
            'uniqueCount': len(results),
            'ngramType': ngram_type
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)