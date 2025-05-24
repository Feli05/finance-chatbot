from classes import Intent
from classes import DialogueManager
from utils.helpers import extract_intent_entities

def handle_flow(intent: Intent, dialogue_manager: DialogueManager, step: int, answers: dict):
    flow_data = answers["flows"]["balance_flow"]["steps"]
    if step >= len(flow_data):
        dialogue_manager.end_flow()
        return answers["fallback"]["step_out_of_range"]
        
    entities = extract_intent_entities(intent)
    combined_text = entities["combined_text"]
    has_yes = entities["has_yes"]
    has_no = entities["has_no"]
    
    step_data = flow_data[step]
    
    if step == 0:
        dialogue_manager.next_flow_step()
        return step_data["initial_message"]
    
    elif step == 1:
        dialogue_manager.next_flow_step()
        
        if has_yes:
            return step_data["yes_response"]
        elif has_no:
            dialogue_manager.end_flow()
            return step_data["no_response"]
        else:
            return step_data["default_response"]
    
    elif step == 2:
        dialogue_manager.end_flow()
        
        if "alert" in combined_text:
            return step_data["alerts_response"]
        elif "review" in combined_text:
            return step_data["review_response"]
        elif "categor" in combined_text or "track" in combined_text:
            return step_data["categorize_response"]
        else:
            return step_data["default_response"] 