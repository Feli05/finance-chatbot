from classes import Intent
from classes import DialogueManager
from utils.helpers import safe_access

def handle_flow(intent: Intent, dialogue_manager: DialogueManager, step: int, answers: dict):
    flow_data = answers["flows"]["investment_flow"]["steps"]
    # Check if step is within range
    if step >= len(flow_data):
        dialogue_manager.end_flow()
        return answers["fallback"]["step_out_of_range"]
        
    step_data = flow_data[step]
    
    # First response to investment advice
    if step == 0:
        dialogue_manager.next_flow_step()
        simple_responses = [e for e in intent.entities if e.type == "simple_response"]
        
        # Check for percentage mentions (for risk tolerance or portfolio allocation)
        percentages = [entity.value for entity in intent.entities if entity.type == "percentage"]
        if percentages:
            dialogue_manager.context["investment_percentage"] = percentages[0]
        
        # User said yes to learning more about investments
        if simple_responses and simple_responses[0].value == "yes":
            return step_data["yes_response"]
        
        # User said no
        elif simple_responses and simple_responses[0].value == "no":
            dialogue_manager.end_flow()
            return step_data["no_response"]
            
        # Other response
        else:
            text_entities = [e.value.lower() for e in intent.entities if e.type == "text"]
            combined_text = " ".join(text_entities)
            
            if "stocks" in combined_text:
                dialogue_manager.context["investment_interest"] = "stocks"
                if "investment_percentage" in dialogue_manager.context:
                    percentage = dialogue_manager.context["investment_percentage"]
                    return step_data["stocks_percentage_response"].format(percentage=percentage)
                else:
                    return step_data["stocks_response"]
                
            elif "bonds" in combined_text:
                dialogue_manager.context["investment_interest"] = "bonds"
                if "investment_percentage" in dialogue_manager.context:
                    percentage = dialogue_manager.context["investment_percentage"]
                    return step_data["bonds_percentage_response"].format(percentage=percentage)
                else:
                    return step_data["bonds_response"]
                
            else:
                # If they mentioned a percentage, use it in our response
                if "investment_percentage" in dialogue_manager.context:
                    percentage = dialogue_manager.context["investment_percentage"]
                    stock_percentage = int(percentage.strip('%'))
                    bond_percentage = 100 - stock_percentage
                    return step_data["default_percentage_response"].format(
                        percentage=percentage, 
                        bond_percentage=bond_percentage
                    )
                else:
                    return step_data["default_response"]
    
    # Second step in the investment conversation
    elif step == 1:
        dialogue_manager.next_flow_step()
        investment_interest = dialogue_manager.context.get("investment_interest", "")
        
        simple_responses = [e for e in intent.entities if e.type == "simple_response"]
        
        if investment_interest == "stocks":
            if simple_responses and simple_responses[0].value == "yes":
                return safe_access(step_data, "stocks", "yes_response")
            else:
                dialogue_manager.end_flow()
                return safe_access(step_data, "stocks", "no_response")
            
        elif investment_interest == "bonds":
            if simple_responses and simple_responses[0].value == "yes":
                return safe_access(step_data, "bonds", "yes_response")
            else:
                dialogue_manager.end_flow()
                return safe_access(step_data, "bonds", "no_response")
            
        else:
            if simple_responses and simple_responses[0].value == "yes":
                return safe_access(step_data, "default", "yes_response")
            else:
                return safe_access(step_data, "default", "no_response")
            
    # Third step in the investment conversation
    elif step == 2:
        # End the flow after giving final advice
        dialogue_manager.end_flow()
        return step_data["final_response"] 