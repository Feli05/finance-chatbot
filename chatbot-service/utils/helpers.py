def safe_access(data, *keys, default=None):
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current

def extract_intent_entities(intent):
    # Extract simple responses and check for yes/no
    simple_responses = [e for e in intent.entities if e.type == "simple_response"]
    has_yes = False
    has_no = False
    if simple_responses:
        response_value = simple_responses[0].value.lower()
        has_yes = response_value == "yes"
        has_no = response_value == "no"
    
    # Extract and process text entities
    text_entities = [e.value.lower() for e in intent.entities if e.type == "text"]
    combined_text = " ".join(text_entities)
    
    # Extract other entity types
    amounts = [e.value for e in intent.entities if e.type == "amount"]
    tickers = [e.value for e in intent.entities if e.type == "ticker"]
    percentages = [e.value for e in intent.entities if e.type == "percentage"]
    
    return {
        "simple_responses": simple_responses,
        "has_yes": has_yes,
        "has_no": has_no,
        "text_entities": text_entities,
        "combined_text": combined_text,
        "amounts": amounts,
        "tickers": tickers,
        "percentages": percentages
    } 