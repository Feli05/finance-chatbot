import re
import json
from classes import Intent, Entity


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
    
    # More flexible detection for affirmative responses
    if (text.startswith("yes") or 
        text.startswith("yeah") or 
        text.startswith("sure") or 
        text.startswith("i would") or
        "like to know more" in text or
        text == "ok" or 
        text == "okay" or
        text in ["yep", "si", "true", "correct"]):
        return [Entity("simple_response", "yes", 1.0)]
    # More flexible detection for negative responses
    elif (text.startswith("no") or 
          text.startswith("nope") or 
          text == "not" or
          "not interested" in text or
          "don't want" in text or
          text in ["false", "incorrect"]):
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

def detect_intent(text: str):
    # First check for responses that might be follow-ups to previous questions
    text_lower = text.lower().strip()
    
    # Check for simple responses (yes/no) regardless of sentence complexity
    simple_responses = extract_simple_response(text_lower)
    
    if simple_responses:
        # Simple responses will be handled in generate_response by checking the dialogue context
        return Intent("fallback", 0.0, simple_responses)
    
    best_intent = None
    best_confidence = 0.0

    for pattern in PATTERNS:
        match = pattern["regex"].search(text)
        if match:
            # Calculate confidence based on match length and position
            confidence = len(match.group()) / len(text)
            if confidence > best_confidence:
                best_confidence = confidence
                best_intent = pattern["intent"]

    if not best_intent:
        return Intent("fallback", 0.0, extract_entities(text))

    entities = extract_entities(text)
    return Intent(best_intent, best_confidence, entities)

with open("patterns.json") as f:
    PATTERNS = [{"intent": p["intent"], "regex": re.compile(p["pattern"], re.IGNORECASE)} for p in json.load(f)]
