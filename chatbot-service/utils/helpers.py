def extract_intent_entities(intent):
    simple_responses = [e for e in intent.entities if e.type == "simple_response"]
    has_yes = False
    has_no = False
    if simple_responses:
        response_value = simple_responses[0].value.lower()
        has_yes = response_value == "yes"
        has_no = response_value == "no"
    
    text_entities = [e.value.lower() for e in intent.entities if e.type == "text"]
    combined_text = " ".join(text_entities)
    amounts = [e.value for e in intent.entities if e.type == "amount"]
    tickers = [e.value for e in intent.entities if e.type == "ticker"]
    
    return {
        "simple_responses": simple_responses,
        "has_yes": has_yes,
        "has_no": has_no,
        "text_entities": text_entities,
        "combined_text": combined_text,
        "amounts": amounts,
        "tickers": tickers
    } 