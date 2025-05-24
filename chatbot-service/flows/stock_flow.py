from classes import Intent
from classes import DialogueManager
from utils.helpers import extract_intent_entities
from utils.apiStockMarket import get_stock_price

def handle_flow(intent: Intent, dialogue_manager: DialogueManager, step: int, answers: dict):
    flow_data = answers["flows"]["stock_flow"]["steps"]
    if step >= len(flow_data):
        dialogue_manager.end_flow()
        return answers["fallback"]["step_out_of_range"]
        
    entities = extract_intent_entities(intent)
    combined_text = entities["combined_text"]
    has_yes = entities["has_yes"]
    has_no = entities["has_no"]
    tickers = entities["tickers"]
    
    ticker = dialogue_manager.context.get("current_ticker", "")
    step_data = flow_data[step]
    
    if step == 0:
        dialogue_manager.next_flow_step()
        return step_data["initial_message"]
            
    elif step == 1:
        wants_top_stocks = "top stocks" in combined_text.lower() or ("top" in combined_text.lower() and "stocks" in combined_text.lower())
        
        if has_no:
            dialogue_manager.end_flow()
            return step_data["no_response"]
        
        if wants_top_stocks:
            return step_data["top_stocks_message"]
            
        if tickers:
            ticker = tickers[0].upper()
            dialogue_manager.context["current_ticker"] = ticker
            
            stock_data = get_stock_price(ticker)
            if "error" in stock_data:
                return step_data["error_message"].format(ticker=ticker)
                
            price = stock_data["close"]
            open_price = stock_data.get("open", 0)
            change = price - open_price
            is_positive = change >= 0
            
            dialogue_manager.context["current_price"] = price
            dialogue_manager.context["is_positive"] = is_positive
            
            dialogue_manager.next_flow_step()
            return step_data["price_message"].format(
                ticker=ticker, 
                price=round(price, 2)
            )
        
        return step_data["default_response"]
    
    elif step == 2:
        if has_yes:
            is_positive = dialogue_manager.context.get("is_positive", False)
            
            if is_positive:
                performance = "positive performance"
                sentiment = "good"
            else:
                performance = "negative performance"
                sentiment = "concerning"
            
            dialogue_manager.next_flow_step()
            return step_data["yes_response"].format(
                ticker=ticker,
                performance=performance,
                sentiment=sentiment
            )
            
        elif has_no:
            dialogue_manager.end_flow()
            return step_data["no_response"]
        else:
            return step_data["default_response"].format(ticker=ticker)
    
    elif step == 3:
        if has_yes:
            dialogue_manager.reset_flow_step(1)
            return step_data["yes_response"]
        elif has_no:
            dialogue_manager.end_flow()
            return step_data["no_response"]
        else:
            dialogue_manager.end_flow()
            return step_data["final_response"] 