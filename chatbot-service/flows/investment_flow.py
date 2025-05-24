from classes import Intent
from classes import DialogueManager
from utils.helpers import extract_intent_entities

def handle_flow(intent: Intent, dialogue_manager: DialogueManager, step: int, answers: dict):
    flow_data = answers["flows"]["investment_flow"]["steps"]
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
        if has_no:
            dialogue_manager.end_flow()
            return step_data["no_response"]
        
        return step_data["timeframe_question"]
    
    elif step == 2:
        if "short" in combined_text:
            dialogue_manager.context["investment_timeframe"] = "short"
        elif "medium" in combined_text:
            dialogue_manager.context["investment_timeframe"] = "medium"
        else:
            dialogue_manager.context["investment_timeframe"] = "long"
            
        dialogue_manager.next_flow_step()
        return step_data["risk_question"]
    
    elif step == 3:
        if "low" in combined_text or "conservative" in combined_text:
            dialogue_manager.context["risk_tolerance"] = "low"
        elif "high" in combined_text or "aggressive" in combined_text:
            dialogue_manager.context["risk_tolerance"] = "high"
        else:
            dialogue_manager.context["risk_tolerance"] = "medium"
            
        dialogue_manager.next_flow_step()
        return step_data["goal_question"]
    
    elif step == 4:
        if "retirement" in combined_text:
            dialogue_manager.context["investment_goal"] = "retirement"
        elif "education" in combined_text or "college" in combined_text:
            dialogue_manager.context["investment_goal"] = "education"
        elif "home" in combined_text or "house" in combined_text:
            dialogue_manager.context["investment_goal"] = "home"
        else:
            dialogue_manager.context["investment_goal"] = "wealth"
        
        timeframe = dialogue_manager.context.get("investment_timeframe", "medium")
        risk = dialogue_manager.context.get("risk_tolerance", "medium")
        goal = dialogue_manager.context.get("investment_goal", "wealth")
        
        response_key = f"{timeframe}_{risk}_{goal}"
        
        dialogue_manager.end_flow()
        
        if response_key in step_data["portfolio_recommendations"]:
            return step_data["portfolio_recommendations"][response_key]
        else:
            return step_data["default_recommendation"] 