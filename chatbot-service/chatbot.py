import json
from classes import Intent
from classes import DialogueManager
from flows import FLOW_HANDLERS

with open("answers.json") as f:
    ANSWERS = json.load(f)

def generate_response(intent: Intent, dialogue_manager: DialogueManager):
    if intent.name == "exit" or intent.name == "thanks":
        dialogue_manager.end_flow()
        return ANSWERS["intents"][intent.name]
    
    flow_state = dialogue_manager.get_flow_state()
    current_flow = flow_state['flow']
    current_step = flow_state['step']
    
    # First check if we're in an active flow
    if current_flow and current_flow in FLOW_HANDLERS:
        return FLOW_HANDLERS[current_flow](intent, dialogue_manager, current_step, ANSWERS)
    
    # If not in a flow, check for new intents to start flows
    if intent.name == "savings_advice":
        dialogue_manager.start_flow("savings_flow")
        return FLOW_HANDLERS["savings_flow"](intent, dialogue_manager, 0, ANSWERS)
        
    elif intent.name == "investment_advice":
        dialogue_manager.start_flow("investment_flow")
        return FLOW_HANDLERS["investment_flow"](intent, dialogue_manager, 0, ANSWERS)
        
    elif intent.name == "balance_inquiry":
        dialogue_manager.start_flow("balance_flow")
        return FLOW_HANDLERS["balance_flow"](intent, dialogue_manager, 0, ANSWERS)
    
    elif intent.name == "ask_budget_advice":
        dialogue_manager.start_flow("budget_flow")
        return FLOW_HANDLERS["budget_flow"](intent, dialogue_manager, 0, ANSWERS)
        
    elif intent.name == "get_stock_price":
        dialogue_manager.start_flow("stock_flow")
        return FLOW_HANDLERS["stock_flow"](intent, dialogue_manager, 0, ANSWERS)
        
    return ANSWERS["intents"].get(intent.name, ANSWERS["intents"]["fallback"])