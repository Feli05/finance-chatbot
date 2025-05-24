from classes import Intent
from classes import DialogueManager
from utils.helpers import safe_access

def handle_flow(intent: Intent, dialogue_manager: DialogueManager, step: int, answers: dict):
    flow_data = answers["flows"]["balance_flow"]["steps"]
    if step >= len(flow_data):
        dialogue_manager.end_flow()
        return answers["fallback"]["step_out_of_range"]
        
    step_data = flow_data[step]
    
    if step == 0:
        dialogue_manager.next_flow_step()
        simple_responses = [e for e in intent.entities if e.type == "simple_response"]
        
        if simple_responses and simple_responses[0].value == "yes":
            return step_data["yes_response"]
        elif simple_responses and simple_responses[0].value == "no":
            dialogue_manager.end_flow()
            return step_data["no_response"]
        else:
            return step_data["default_response"]
    
    elif step == 1:
        dialogue_manager.next_flow_step()
        
        text_entities = [e.value.lower() for e in intent.entities if e.type == "text"]
        combined_text = " ".join(text_entities)
        
        if "alert" in combined_text:
            return step_data["alerts_response"]
        elif "review" in combined_text:
            return step_data["review_response"]
        elif "categor" in combined_text or "track" in combined_text:
            return step_data["categorize_response"]
        else:
            return step_data["default_response"]
    
    elif step == 2:
        dialogue_manager.end_flow()
        return step_data["final_response"] 