import re
import json
from classes import Intent, Entity


def tokenize(text: str):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\$\.\% ]+', ' ', text)
    return [tok for tok in text.split() if tok]

def extract_tickers(text: str):
    matches = re.findall(r'\b[A-Z]{2,5}\b', text)
    return [Entity("ticker", match) for match in matches]

def extract_amounts(text: str):
    matches = re.findall(r'\$\d+(?:\.\d{1,2})?', text)
    return [Entity("amount", match) for match in matches]

def extract_percentages(text: str):
    matches = re.findall(r'\d+(?:\.\d{1,2})?%', text)
    return [Entity("percentage", match) for match in matches]

def extract_entities(text: str):
    entities = []
    entities.extend(extract_tickers(text))
    entities.extend(extract_amounts(text))
    entities.extend(extract_percentages(text))
    return entities

def detect_intent(text: str):
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
        return Intent("fallback", 0.0, [])

    entities = extract_entities(text)
    return Intent(best_intent, best_confidence, entities)

with open("patterns.json") as f:
    PATTERNS = [{"intent": p["intent"], "regex": re.compile(p["pattern"], re.IGNORECASE)} for p in json.load(f)]
