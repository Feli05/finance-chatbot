import re
import json
from classes import Intent, Entity

with open("patterns.json") as f:
    CONFIG = json.load(f)

def collapse_repeats(word: str, max_repeats: int = 2) -> str:
    if len(word) < 2:
        return word

    out = []
    last_char = None
    run_len = 0

    for ch in word:
        if ch == last_char:
            run_len += 1
            if run_len <= max_repeats:
                out.append(ch)
        else:
            last_char = ch
            run_len = 1
            out.append(ch)

    return "".join(out)

def tokenize(text: str):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\$\.\% ]+', ' ', text)
    return [collapse_repeats(tok, max_repeats=2) for tok in text.split() if tok]

def extract_tickers(text: str):
    standard_matches = re.findall(r'\b[A-Z]{2,5}\b', text)
    dollar_matches   = re.findall(r'\$([A-Z]{1,5})\b', text)
    all_matches = set(standard_matches + dollar_matches)
    return [Entity("ticker", m, 1.0) for m in all_matches]

def extract_amounts(text: str):
    matches = re.findall(r'\$\d+(?:\.\d{1,2})?', text)
    return [Entity("amount", m, 1.0) for m in matches]

def extract_simple_response(text: str):
    text = text.lower().strip()

    yes_words   = CONFIG["yes_responses"]
    no_words    = CONFIG["no_responses"]
    yes_phrases = CONFIG["yes_phrases"]
    no_phrases  = CONFIG["no_phrases"]

    for word in yes_words:
        if text == word or text.startswith(word + " "):
            return [Entity("simple_response", "yes", 1.0)]

    for word in no_words:
        if text == word or text.startswith(word + " "):
            return [Entity("simple_response", "no", 1.0)]

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
    entities.extend(extract_simple_response(text))
    if not entities:
        entities.append(Entity("text", text, 0.5))
    return entities

def simple_stem(word):
    if len(word) <= 3:            return word
    if word.endswith('s'):        return word[:-1]
    if word.endswith('es'):       return word[:-2]
    if word.endswith('ing'):      return word[:-3]
    if word.endswith('ed'):       return word[:-2]
    return word

def calculate_partial_match(token, keyword):
    if token.startswith(keyword) or keyword.startswith(token):
        shared_len = min(len(token), len(keyword))
        max_len    = max(len(token), len(keyword))
        return (shared_len / max_len) * 0.7
    return 0.0

def detect_intent(text: str):
    if text.lower().strip() == "exit":
        return Intent("exit", 1.0, [Entity("text", text, 1.0)])

    simple_responses = extract_simple_response(text.lower().strip())
    if simple_responses:
        return Intent("fallback", 0.0, simple_responses)

    text_lower     = text.lower().strip()
    tokens         = tokenize(text_lower)
    stemmed_tokens = [simple_stem(t) for t in tokens]

    intent_scores = {}

    for intent_obj in CONFIG["intents"]:
        intent    = intent_obj["intent"]
        keywords  = intent_obj["keywords"]
        matches   = 0.0

        # phrase match
        for kw in keywords:
            if ' ' in kw and kw.lower() in text_lower:
                matches += 1.5

        # single-word match
        for kw in keywords:
            if ' ' in kw:
                continue
            if kw in tokens:
                matches += 1.0
                continue
            if simple_stem(kw) in stemmed_tokens:
                matches += 0.8
                continue
            for tok in tokens:
                matches += calculate_partial_match(tok, kw)
                if matches:   
                    break

        if matches:
            score = (matches / len(keywords)) * (1 + 0.1 * matches)
            intent_scores[intent] = score

    if intent_scores:
        best_intent, best_score = max(intent_scores.items(),
                                      key=lambda kv: kv[1])
        return Intent(best_intent, best_score, extract_entities(text))

    return Intent("fallback", 0.0, extract_entities(text))