import re
import json
from classes import Intent
from classes import DialogueManager

def generate_response(intent: Intent, dialogue_manager: DialogueManager):
    context = dialogue_manager.get_context()
    
    if intent.name == "get_stock_price":
        tickers = [entity.value for entity in intent.entities if entity.type == "ticker"]
        if not tickers and "last_tickers" in context:
            tickers = context["last_tickers"]
        
        if not tickers:
            return "Digues-me el símbol de l'acció (p.ex. AAPL)."
        
        resp_parts = []
        
        for ticker in tickers:
            # Simulated price - in real app, this would call an API
            price = 100.0
            resp_parts.append(ANSWERS[intent.name].format(ticker=ticker, price=price))

        return "  ".join(resp_parts)

    elif intent.name == "ask_budget_advice":
        amounts = [entity.value for entity in intent.entities if entity.type == "amount"]
        if amounts:
            return f"Veig que vols gestionar {amounts[0]}. {ANSWERS[intent.name]}"
        return ANSWERS[intent.name]

    return ANSWERS.get(intent.name, ANSWERS["fallback"])

# Load patterns for matching user intents
with open("patterns.json") as f:
    PATTERNS = [{"intent": p["intent"], "regex": re.compile(p["pattern"], re.IGNORECASE)} for p in json.load(f)]

# Load response templates
with open("answers.json") as f:
    ANSWERS = json.load(f)
