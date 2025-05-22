import re
import json
from classes import Intent, Entity

with open("patterns.json") as f:
    CONFIG = json.load(f)

def tokenize(text: str):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\$\.\% ]+', ' ', text)
    return [tok for tok in text.split() if tok]

def extract_tickers(text: str):
    # Standard format tickers (2-5 uppercase letters)
    standard_matches = re.findall(r'\b[A-Z]{2,5}\b', text)
    
    # Also look for tickers prefixed with $ (common in social media)
    dollar_matches = re.findall(r'\$([A-Z]{1,5})\b', text)
    
    # Combine the matches
    all_matches = set(standard_matches + dollar_matches)
    
    return [Entity("ticker", match, 1.0) for match in all_matches]

def extract_amounts(text: str):
    matches = re.findall(r'\$\d+(?:\.\d{1,2})?', text)
    return [Entity("amount", match, 1.0) for match in matches]

def extract_percentages(text: str):
    matches = re.findall(r'\d+(?:\.\d{1,2})?%', text)
    return [Entity("percentage", match, 1.0) for match in matches]

def extract_simple_response(text: str):
    text = text.lower().strip()
    
    # Get yes/no responses from config
    yes_words = CONFIG["yes_responses"]
    no_words = CONFIG["no_responses"]
    yes_phrases = CONFIG["yes_phrases"]
    no_phrases = CONFIG["no_phrases"]
    
    # Check for exact matches first
    for word in yes_words:
        if text == word or text.startswith(word + " "):
            return [Entity("simple_response", "yes", 1.0)]
            
    for word in no_words:
        if text == word or text.startswith(word + " "):
            return [Entity("simple_response", "no", 1.0)]
    
    # Check for phrases
    for phrase in yes_phrases:
        if phrase in text:
            return [Entity("simple_response", "yes", 1.0)]
    
    for phrase in no_phrases:
        if phrase in text:
            return [Entity("simple_response", "no", 1.0)]
        
    return []

def extract_entities(text: str):
    entities = []
    entities.extend(extract_tickers(text))
    entities.extend(extract_amounts(text))
    entities.extend(extract_percentages(text))
    entities.extend(extract_simple_response(text))
    
    # If no entities were found, add the text itself as an entity
    if not entities:
        entities.append(Entity("text", text, 0.5))
    
    return entities

def simple_stem(word):
    if len(word) <= 3:
        return word
        
    if word.endswith('s'):
        return word[:-1]
    if word.endswith('es'):
        return word[:-2]
    if word.endswith('ing'):
        return word[:-3]
    if word.endswith('ed'):
        return word[:-2]
    
    return word

def detect_intent(text: str):
    simple_responses = extract_simple_response(text.lower().strip())
    if simple_responses:
        return Intent("fallback", 0.0, simple_responses)
    
    tokens = tokenize(text)
    stemmed_tokens = [simple_stem(token) for token in tokens]
    
    intent_scores = {}
    
    for intent_obj in CONFIG["intents"]:
        intent = intent_obj["intent"]
        keywords = intent_obj["keywords"]
        
        matches = 0
        
        # Check for phrases
        for keyword in keywords:
            if ' ' in keyword and keyword.lower() in text.lower():
                matches += 1.5 
                continue
                
        # Check for individual words
        for keyword in keywords:
            if ' ' not in keyword:  
                if keyword in tokens:
                    matches += 1
                    continue
                    
                stemmed_keyword = simple_stem(keyword)
                if stemmed_keyword in stemmed_tokens:
                    matches += 0.8 
        
        if matches > 0:
            # Normalize by keyword count and add bonus for multiple matches
            score = (matches / len(keywords)) * (1 + 0.1 * matches)
            intent_scores[intent] = score
    
    # Find best matching intent
    if intent_scores:
        best_intent = max(intent_scores.items(), key=lambda score: score[1])
        
        intent_name, score = best_intent
        
        return Intent(intent_name, score, extract_entities(text))
    
    # No good match found
    return Intent("fallback", 0.0, extract_entities(text))


