from classes import Intent
from classes import DialogueManager
from utils.helpers import extract_intent_entities

def handle_flow(intent: Intent, dialogue_manager: DialogueManager, step: int, answers: dict):
    flow_data = answers["flows"]["savings_flow"]["steps"]
    if step >= len(flow_data):
        dialogue_manager.end_flow()
        return answers["fallback"]["step_out_of_range"]
    
    entities = extract_intent_entities(intent)
    has_yes = entities["has_yes"]
    has_no = entities["has_no"]
    combined_text = entities["combined_text"]
    
    step_data = flow_data[step]
    
    if step == 0:
        dialogue_manager.next_flow_step()
        return step_data["initial_message"]
    
    elif step == 1:
        if has_no:
            dialogue_manager.end_flow()
            return step_data["no_response"]
        elif has_yes:
            dialogue_manager.next_flow_step()
            return step_data["yes_response"]
        else:
            return step_data["default_response"]
    
    elif step == 2:
        dialogue_manager.next_flow_step()
        
        if "emergency" in combined_text.lower() or "short" in combined_text.lower():
            dialogue_manager.context["savings_goal"] = "emergency"
            return step_data["emergency_response"]
        elif "retirement" in combined_text.lower() or "long" in combined_text.lower():
            dialogue_manager.context["savings_goal"] = "retirement"
            return step_data["retirement_response"]
        else:
            return step_data["default_response"]
    
    elif step == 3:
        dialogue_manager.end_flow()
        savings_goal = dialogue_manager.context.get("savings_goal", "")
        
        if has_no:
            return step_data["no_response"]
        elif has_yes:
            if savings_goal == "emergency":
                return step_data["emergency_response"]
            elif savings_goal == "retirement":
                return step_data["retirement_response"]
            else:
                return step_data["final_response"]
        else:
            return step_data["final_response"] 