from classes import Intent
from classes import DialogueManager
from utils.helpers import safe_access

def handle_flow(intent: Intent, dialogue_manager: DialogueManager, step: int, answers: dict):
    flow_data = answers["flows"]["stock_flow"]["steps"]
    # Check if step is within range
    if step >= len(flow_data):
        dialogue_manager.end_flow()
        return answers["fallback"]["step_out_of_range"]
        
    step_data = flow_data[step]
    
    # Get the stock ticker from context
    ticker = dialogue_manager.context.get("current_ticker", "")
    
    # First response after providing stock price
    if step == 0:
        dialogue_manager.next_flow_step()
        simple_responses = [e for e in intent.entities if e.type == "simple_response"]
        
        if simple_responses and simple_responses[0].value == "yes":
            return step_data["yes_response"].format(ticker=ticker)
        elif simple_responses and simple_responses[0].value == "no":
            dialogue_manager.end_flow()
            return step_data["no_response"]
        else:
            return step_data["default_response"].format(ticker=ticker)
    
    # Second response about analyst recommendations
    elif step == 1:
        dialogue_manager.next_flow_step()
        simple_responses = [e for e in intent.entities if e.type == "simple_response"]
        
        if simple_responses and simple_responses[0].value == "yes":
            return step_data["yes_response"].format(ticker=ticker)
        else:
            return step_data["default_response"].format(ticker=ticker)
    
    # Final response about stock risks
    elif step == 2:
        dialogue_manager.end_flow()
        return step_data["final_response"].format(ticker=ticker) 