from classes import Intent
from classes import DialogueManager
from utils.helpers import extract_intent_entities

def handle_flow(intent: Intent, dialogue_manager: DialogueManager, step: int, answers: dict):
    flow_data = answers["flows"]["budget_flow"]["steps"]
    if step >= len(flow_data):
        dialogue_manager.end_flow()
        return answers["fallback"]["step_out_of_range"]
    
    entities = extract_intent_entities(intent)
    has_yes = entities["has_yes"]
    has_no = entities["has_no"]
    combined_text = entities["combined_text"]
    amounts = entities["amounts"]
        
    step_data = flow_data[step]

    if step == 0:
        if amounts:
            dialogue_manager.context["budget_amount"] = amounts[0]
            response = step_data["amount_greeting"].format(budget_amount=amounts[0])
        else:
            response = step_data["initial_greeting"]
        
        dialogue_manager.next_flow_step()
        return response
    
    elif step == 1:
        if "save" in combined_text or "saving" in combined_text:
            dialogue_manager.context["budget_goal"] = "saving"
            dialogue_manager.next_flow_step()
            return step_data["saving_response"]
            
        elif "debt" in combined_text or "loan" in combined_text or "pay" in combined_text:
            dialogue_manager.context["budget_goal"] = "debt"
            dialogue_manager.next_flow_step()
            return step_data["debt_response"]
            
        elif "emergency" in combined_text or "fund" in combined_text:
            dialogue_manager.context["budget_goal"] = "emergency"
            dialogue_manager.next_flow_step()
            return step_data["emergency_response"]
            
        else:
            dialogue_manager.context["budget_goal"] = "general"
            dialogue_manager.next_flow_step()
            return step_data["default_response"]
    
    elif step == 2:
        dialogue_manager.end_flow()
        budget_goal = dialogue_manager.context.get("budget_goal", "general")
        
        if has_yes:
            if budget_goal == "emergency":
                return step_data["account_response"]
            else:
                return step_data["tool_response"]
        elif has_no:
            return step_data["final_response"]
        else:
            return step_data["default_response"] 