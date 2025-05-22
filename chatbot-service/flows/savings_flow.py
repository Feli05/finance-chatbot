from classes import Intent
from classes import DialogueManager
from utils.helpers import safe_access

def handle_flow(intent: Intent, dialogue_manager: DialogueManager, step: int, answers: dict):
    flow_data = answers["flows"]["savings_flow"]["steps"]
    # Check if step is within range
    if step >= len(flow_data):
        dialogue_manager.end_flow()
        return answers["fallback"]["step_out_of_range"]
    
    step_data = flow_data[step]
    
    # First message after savings advice was requested
    if step == 0:
        dialogue_manager.next_flow_step()
        simple_responses = [e for e in intent.entities if e.type == "simple_response"]
        
        # User said yes to discussing savings
        if simple_responses and simple_responses[0].value == "yes":
            return step_data["yes_response"]
        
        # User said no to discussing savings
        elif simple_responses and simple_responses[0].value == "no":
            dialogue_manager.end_flow()
            return step_data["no_response"]
        
        # User provided other information
        else:
            text_entities = [e.value.lower() for e in intent.entities if e.type == "text"]
            combined_text = " ".join(text_entities)
            
            if "emergency" in combined_text or "short" in combined_text:
                dialogue_manager.context["savings_goal"] = "emergency"
                return step_data["emergency_response"]
            
            elif "retirement" in combined_text or "long" in combined_text:
                dialogue_manager.context["savings_goal"] = "retirement"
                return step_data["retirement_response"]
            
            else:
                return step_data["default_response"]
    
    # Second step in the savings conversation
    elif step == 1:
        dialogue_manager.next_flow_step()
        savings_goal = dialogue_manager.context.get("savings_goal", "")
        
        simple_responses = [e for e in intent.entities if e.type == "simple_response"]
        
        if savings_goal == "emergency":
            # User asked for emergency fund tips
            if simple_responses and simple_responses[0].value == "yes":
                return safe_access(step_data, "emergency", "yes_response")
            else:
                dialogue_manager.end_flow()
                return safe_access(step_data, "emergency", "no_response")
                
        elif savings_goal == "retirement":
            # User asked about retirement accounts
            if simple_responses and simple_responses[0].value == "yes":
                return safe_access(step_data, "retirement", "yes_response")
            else:
                return safe_access(step_data, "retirement", "no_response")
                
        else:
            # Generic advice if we couldn't determine the goal
            return step_data.get("default_response")
    
    # Third step in the savings conversation        
    elif step == 2:
        # End the flow after giving final advice
        dialogue_manager.end_flow()
        return step_data.get("final_response") 