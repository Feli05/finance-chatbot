from classes import Intent
from classes import DialogueManager
from utils.helpers import safe_access

def handle_flow(intent: Intent, dialogue_manager: DialogueManager, step: int, answers: dict):
    flow_data = answers["flows"]["budget_flow"]["steps"]
    # Check if step is within range
    if step >= len(flow_data):
        dialogue_manager.end_flow()
        return answers["fallback"]["step_out_of_range"]
        
    step_data = flow_data[step]
    
    # First response to budget advice request
    if step == 0:
        dialogue_manager.next_flow_step()
        
        # Get any previously mentioned budget amount
        budget_amount = dialogue_manager.context.get("budget_amount", "")
        
        simple_responses = [e for e in intent.entities if e.type == "simple_response"]
        
        # User provided information about their financial goals
        text_entities = [e.value.lower() for e in intent.entities if e.type == "text"]
        combined_text = " ".join(text_entities)
        
        # Check the context of the response
        if "save" in combined_text or "saving" in combined_text:
            dialogue_manager.context["budget_goal"] = "saving"
            if budget_amount:
                return step_data["saving_amount_response"].format(budget_amount=budget_amount)
            else:
                return step_data["saving_response"]
        
        elif "debt" in combined_text or "loan" in combined_text or "pay off" in combined_text:
            dialogue_manager.context["budget_goal"] = "debt"
            return step_data["debt_response"]
        
        elif "emergency" in combined_text or "fund" in combined_text:
            dialogue_manager.context["budget_goal"] = "emergency"
            return step_data["emergency_response"]
        
        # Generic response if we can't determine their specific goal
        else:
            if simple_responses and simple_responses[0].value == "yes":
                return step_data["yes_response"]
            elif simple_responses and simple_responses[0].value == "no":
                dialogue_manager.end_flow()
                return step_data["no_response"]
            else:
                return step_data["default_response"]
    
    # Second step in the budget conversation
    elif step == 1:
        dialogue_manager.next_flow_step()
        budget_goal = dialogue_manager.context.get("budget_goal", "")
        
        simple_responses = [e for e in intent.entities if e.type == "simple_response"]
        
        if budget_goal == "saving":
            if simple_responses and simple_responses[0].value == "yes":
                return safe_access(step_data, "saving", "yes_response")
            else:
                dialogue_manager.end_flow()
                return safe_access(step_data, "saving", "no_response")
        
        elif budget_goal == "debt":
            text_entities = [e.value.lower() for e in intent.entities if e.type == "text"]
            combined_text = " ".join(text_entities)
            
            if "avalanche" in combined_text:
                return safe_access(step_data, "debt", "avalanche_response")
            elif "snowball" in combined_text:
                return safe_access(step_data, "debt", "snowball_response")
            else:
                return safe_access(step_data, "debt", "default_response")
        
        elif budget_goal == "emergency":
            if simple_responses and simple_responses[0].value == "yes":
                return safe_access(step_data, "emergency", "yes_response")
            else:
                dialogue_manager.end_flow()
                return safe_access(step_data, "emergency", "no_response")
        
        else:
            # Generic advice if we couldn't determine their specific goal
            return step_data["default_response"]
    
    # Third step in the budget conversation
    elif step == 2:
        # End the flow after giving specific advice
        dialogue_manager.end_flow()
        
        # Final advice based on their responses
        if "budget_goal" in dialogue_manager.context:
            goal = dialogue_manager.context.get("budget_goal")
            
            if goal == "saving":
                return step_data["saving_final"]
            
            elif goal == "debt":
                return step_data["debt_final"]
            
            elif goal == "emergency":
                return step_data["emergency_final"]
        
        return step_data["default_final"] 