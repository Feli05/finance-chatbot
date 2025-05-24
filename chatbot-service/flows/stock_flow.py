from classes import Intent
from classes import DialogueManager
from utils.helpers import extract_intent_entities
from utils.apiStockMarket import get_stock_price

def handle_flow(intent: Intent, dialogue_manager: DialogueManager, step: int, answers: dict):
    flow_data = answers["flows"]["stock_flow"]["steps"]
    if step >= len(flow_data):
        dialogue_manager.end_flow()
        return answers["fallback"]["step_out_of_range"]
        
    step_data = flow_data[step]
    
    # Extract entities using the helper function
    entities = extract_intent_entities(intent)
    has_yes = entities["has_yes"]
    has_no = entities["has_no"]
    tickers = entities["tickers"]
    
    ticker = dialogue_manager.context.get("current_ticker", "")
    
    if step == 0:
        if not tickers:
            return "Please specify a stock ticker symbol (e.g., AAPL for Apple)"
            
        dialogue_manager.context["current_ticker"] = tickers[0]
        
        price = get_stock_price(tickers[0])
        if "error" in price:
            return price["error"]
            
        dialogue_manager.context["current_price"] = price["close"]
        
        dialogue_manager.next_flow_step()
        return answers["intents"]["get_stock_price"].format(
            ticker=tickers[0], 
            price=price["close"]
        )
    
    elif step == 1:
        dialogue_manager.next_flow_step()
        
        if has_yes:
            return step_data["yes_response"].format(ticker=ticker)
        elif has_no:
            dialogue_manager.end_flow()
            return step_data["no_response"]
        else:
            return step_data["default_response"].format(ticker=ticker)
    
    elif step == 2:
        dialogue_manager.next_flow_step()
        
        if has_yes:
            return step_data["yes_response"].format(ticker=ticker)
        else:
            return step_data["default_response"].format(ticker=ticker)
    
    elif step == 3:
        dialogue_manager.end_flow()
        return step_data["final_response"].format(ticker=ticker) 