import json
from classes import Intent
from classes import DialogueManager
from flows import FLOW_HANDLERS

with open("answers.json") as f:
    ANSWERS = json.load(f)

def generate_response(intent: Intent, dialogue_manager: DialogueManager):
    # Get current flow state
    flow_state = dialogue_manager.get_flow_state()
    current_flow = flow_state['flow']
    current_step = flow_state['step']
    
    # First check if we're in an active flow
    if current_flow and current_flow in FLOW_HANDLERS:
        return FLOW_HANDLERS[current_flow](intent, dialogue_manager, current_step, ANSWERS)
    
    # If not in a flow, check for new intents to start flows
    if intent.name == "savings_advice":
        dialogue_manager.start_flow("savings_flow")
        response = ANSWERS["intents"]["savings_advice"]
        return response
        
    elif intent.name == "investment_advice":
        dialogue_manager.start_flow("investment_flow")
        response = ANSWERS["intents"]["investment_advice"]
        return response
        
    elif intent.name == "balance_inquiry":
        dialogue_manager.start_flow("balance_flow")
        response = ANSWERS["intents"]["balance_inquiry"]
        return response
    
    elif intent.name == "ask_budget_advice":
        dialogue_manager.start_flow("budget_flow")
        # Check for amounts mentioned
        amounts = [entity.value for entity in intent.entities if entity.type == "amount"]
        if amounts:
            dialogue_manager.context["budget_amount"] = amounts[0]
            response = f"I see you're looking to budget {amounts[0]}. {ANSWERS['intents']['ask_budget_advice']}"
        else:
            response = ANSWERS["intents"]["ask_budget_advice"]
        return response
        
    elif intent.name == "get_stock_price":
        tickers = [entity.value for entity in intent.entities if entity.type == "ticker"]
        if not tickers:
            return "Please specify a stock ticker symbol (e.g., AAPL for Apple)"
            
        dialogue_manager.start_flow("stock_flow")
        dialogue_manager.context["current_ticker"] = tickers[0]
        
        # Simulated price - in real app, this would call an API
        price = 100.0
        response = ANSWERS["intents"]["get_stock_price"].format(ticker=tickers[0], price=price)
        return response
        
    # For all other intents, return the standard response
    return ANSWERS["intents"].get(intent.name, ANSWERS["intents"]["fallback"])