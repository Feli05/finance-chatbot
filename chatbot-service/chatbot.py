import re
import json
from classes import Intent
from classes import DialogueManager

def generate_response(intent: Intent, dialogue_manager: DialogueManager):
    # Get current flow state - this is the key to maintaining conversation
    flow_state = dialogue_manager.get_flow_state()
    current_flow = flow_state['flow']
    current_step = flow_state['step']
    
    # First check if we're in an active flow
    if current_flow:
        # Handle savings flow
        if current_flow == "savings_flow":
            return handle_savings_flow(intent, dialogue_manager, current_step)
        
        # Handle investment flow
        elif current_flow == "investment_flow":
            return handle_investment_flow(intent, dialogue_manager, current_step)
            
        # Handle balance inquiry flow
        elif current_flow == "balance_flow":
            return handle_balance_flow(intent, dialogue_manager, current_step)
            
        # Handle stock price flow
        elif current_flow == "stock_flow":
            return handle_stock_flow(intent, dialogue_manager, current_step)
            
        # Handle budget advice flow
        elif current_flow == "budget_flow":
            return handle_budget_flow(intent, dialogue_manager, current_step)
    
    # If not in a flow, check for new intents to start flows
    if intent.name == "savings_advice":
        dialogue_manager.start_flow("savings_flow")
        response = ANSWERS["savings_advice"]
        return response
        
    elif intent.name == "investment_advice":
        dialogue_manager.start_flow("investment_flow")
        response = ANSWERS["investment_advice"]
        return response
        
    elif intent.name == "balance_inquiry":
        dialogue_manager.start_flow("balance_flow")
        response = ANSWERS["balance_inquiry"]
        return response
    
    elif intent.name == "ask_budget_advice":
        dialogue_manager.start_flow("budget_flow")
        # Check for amounts mentioned
        amounts = [entity.value for entity in intent.entities if entity.type == "amount"]
        if amounts:
            dialogue_manager.context["budget_amount"] = amounts[0]
            response = f"I see you're looking to budget {amounts[0]}. {ANSWERS['ask_budget_advice']}"
        else:
            response = ANSWERS["ask_budget_advice"]
        return response
        
    elif intent.name == "get_stock_price":
        tickers = [entity.value for entity in intent.entities if entity.type == "ticker"]
        if not tickers:
            return "Please specify a stock ticker symbol (e.g., AAPL for Apple)"
            
        dialogue_manager.start_flow("stock_flow")
        dialogue_manager.context["current_ticker"] = tickers[0]
        
        # Simulated price - in real app, this would call an API
        price = 100.0
        response = ANSWERS["get_stock_price"].format(ticker=tickers[0], price=price)
        return response
        
    # For all other intents, just return the standard response
    return ANSWERS.get(intent.name, ANSWERS["fallback"])

def handle_savings_flow(intent: Intent, dialogue_manager: DialogueManager, step: int):
    # First message after savings advice was requested
    if step == 0:
        dialogue_manager.next_flow_step()
        simple_responses = [e for e in intent.entities if e.type == "simple_response"]
        
        # User said yes to discussing savings
        if simple_responses and simple_responses[0].value == "yes":
            return "Perfect! Let's discuss your savings goals. Are you saving for short-term goals like an emergency fund, or longer-term goals like retirement?"
        
        # User said no to discussing savings
        elif simple_responses and simple_responses[0].value == "no":
            dialogue_manager.end_flow()
            return "No problem. Is there something else I can help you with regarding your finances?"
        
        # User provided other information
        else:
            text_entities = [e.value.lower() for e in intent.entities if e.type == "text"]
            combined_text = " ".join(text_entities)
            
            if "emergency" in combined_text or "short" in combined_text:
                dialogue_manager.context["savings_goal"] = "emergency"
                return "Emergency funds are critical! Financial experts recommend saving 3-6 months of expenses. Would you like tips on building your emergency fund faster?"
            
            elif "retirement" in combined_text or "long" in combined_text:
                dialogue_manager.context["savings_goal"] = "retirement"
                return "Planning for retirement is smart! The earlier you start, the more your money can grow. Are you currently contributing to any retirement accounts?"
            
            else:
                return "I see. For effective savings, I need to understand your goals. Are you saving for something in the near future, or a long-term goal like retirement?"
    
    # Second step in the savings conversation
    elif step == 1:
        dialogue_manager.next_flow_step()
        savings_goal = dialogue_manager.context.get("savings_goal", "")
        
        simple_responses = [e for e in intent.entities if e.type == "simple_response"]
        
        if savings_goal == "emergency":
            # User asked for emergency fund tips
            if simple_responses and simple_responses[0].value == "yes":
                return "Great! To build your emergency fund faster: 1) Set up automatic transfers to savings, 2) Save your tax refunds and bonuses, 3) Cut unnecessary expenses and redirect that money to savings. Would you like a recommended budget breakdown?"
            else:
                dialogue_manager.end_flow()
                return "I understand. Let me know if you need any other financial advice in the future."
                
        elif savings_goal == "retirement":
            # User asked about retirement accounts
            if simple_responses and simple_responses[0].value == "yes":
                return "Excellent! Make sure you're maximizing any employer match, diversifying your investments, and increasing contributions whenever possible. Would you like to know about different retirement account options?"
            else:
                return "Starting a retirement account is a great first step. Look into employer-sponsored plans like 401(k)s or individual options like IRAs. Would you like more specific advice?"
                
        else:
            # Generic advice if we couldn't determine the goal
            return "For effective saving, I recommend the 50/30/20 rule: 50% of income for needs, 30% for wants, and 20% for savings and debt repayment. Would you like more specific advice for your situation?"
    
    # Third step in the savings conversation        
    elif step == 2:
        # End the flow after giving final advice
        dialogue_manager.end_flow()
        return "I hope this advice helps with your savings goals! Remember, consistency is key. Is there anything else I can help with regarding your finances?"

def handle_investment_flow(intent: Intent, dialogue_manager: DialogueManager, step: int):
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
            return "Excellent! For beginners, I recommend starting with index funds which offer broad market exposure with lower fees. Are you interested in stocks, bonds, or a mix of both?"
        
        # User said no
        elif simple_responses and simple_responses[0].value == "no":
            dialogue_manager.end_flow()
            return "No problem. Let me know if you have other financial questions in the future."
            
        # Other response
        else:
            text_entities = [e.value.lower() for e in intent.entities if e.type == "text"]
            combined_text = " ".join(text_entities)
            
            if "stocks" in combined_text:
                dialogue_manager.context["investment_interest"] = "stocks"
                if "investment_percentage" in dialogue_manager.context:
                    percentage = dialogue_manager.context["investment_percentage"]
                    return f"Allocating {percentage} to stocks can provide good growth potential but with increased volatility. For beginners, ETFs that track major indices like the S&P 500 are a good starting point. Would you like to know more about specific stock ETFs?"
                else:
                    return "Stocks offer higher growth potential but with more volatility. For beginners, ETFs that track major indices like the S&P 500 are a good starting point. Would you like to know more about specific stock ETFs?"
                
            elif "bonds" in combined_text:
                dialogue_manager.context["investment_interest"] = "bonds"
                if "investment_percentage" in dialogue_manager.context:
                    percentage = dialogue_manager.context["investment_percentage"]
                    return f"Allocating {percentage} to bonds can provide stability and income in your portfolio. Bonds typically offer more stability than stocks, but with lower growth potential. Would you like to know more about bond investments?"
                else:
                    return "Bonds typically offer more stability and income than stocks, but with lower growth potential. They're good for preserving capital and generating income. Would you like to know more about bond investments?"
                
            else:
                # If they mentioned a percentage, use it in our response
                if "investment_percentage" in dialogue_manager.context:
                    percentage = dialogue_manager.context["investment_percentage"]
                    stock_percentage = int(percentage.strip('%'))
                    bond_percentage = 100 - stock_percentage
                    return f"A portfolio with {percentage} in stocks and {bond_percentage}% in bonds could be a reasonable mix, depending on your risk tolerance and time horizon. Would you like to know more about building a balanced portfolio?"
                else:
                    return "I recommend a diversified portfolio with both stocks and bonds, with the ratio depending on your risk tolerance and time horizon. Would you like to know more about building a balanced portfolio?"
    
    # Second step in the investment conversation
    elif step == 1:
        dialogue_manager.next_flow_step()
        investment_interest = dialogue_manager.context.get("investment_interest", "")
        
        simple_responses = [e for e in intent.entities if e.type == "simple_response"]
        
        if investment_interest == "stocks":
            if simple_responses and simple_responses[0].value == "yes":
                return "Popular stock ETFs include SPY (tracks S&P 500), QQQ (tracks Nasdaq-100), and VTI (total US stock market). These give you broad exposure with a single purchase. Would you like information on how to start investing in these?"
            else:
                dialogue_manager.end_flow()
                return "I understand. Feel free to ask if you have more questions about investing in the future."
                
        elif investment_interest == "bonds":
            if simple_responses and simple_responses[0].value == "yes":
                return "For bond exposure, consider ETFs like AGG (US aggregate bonds), BND (total bond market), or VCSH (short-term corporate bonds). These offer diversification across many bonds. Would you like to know about the risks associated with bonds?"
            else:
                dialogue_manager.end_flow()
                return "I understand. Let me know if you have other questions about investing."
                
        else:
            # Generic advice about balanced portfolios
            return "A classic balanced portfolio might be 60% stocks and 40% bonds, adjusted based on your age and risk tolerance. As you get closer to needing the money, you'd typically shift more toward bonds. Would you like to know about automating your investments?"
                
    # Third step in the investment conversation
    elif step == 2:
        # End the flow after giving final advice
        dialogue_manager.end_flow()
        return "I hope this helps with your investment decisions! Remember that investing is for the long term, and consistency often matters more than timing. Is there anything else I can help with?"

def handle_balance_flow(intent: Intent, dialogue_manager: DialogueManager, step: int):
    # First response to balance inquiry
    if step == 0:
        dialogue_manager.next_flow_step()
        simple_responses = [e for e in intent.entities if e.type == "simple_response"]
        
        # User said yes to learning about account management
        if simple_responses and simple_responses[0].value == "yes":
            return "Great! To manage your accounts effectively, I recommend: 1) Setting up automatic alerts for low balances, 2) Reviewing your accounts weekly, 3) Using tools that categorize your spending. Would you like more specific advice on any of these areas?"
        
        # User said no
        elif simple_responses and simple_responses[0].value == "no":
            dialogue_manager.end_flow()
            return "No problem. Let me know if you have other financial questions."
            
        # Other response
        else:
            dialogue_manager.end_flow()
            return "I understand. Managing your accounts is important for financial health. Feel free to ask specific questions about budgeting or account management anytime."
    
    # Second step in the balance conversation
    elif step == 1:
        dialogue_manager.next_flow_step()
        
        # Check what area they're interested in
        text_entities = [e.value.lower() for e in intent.entities if e.type == "text"]
        combined_text = " ".join(text_entities)
        
        if "alert" in combined_text or "notification" in combined_text:
            return "Setting up balance alerts is easy! Most banking apps let you set thresholds like 'notify me when balance drops below $500.' This helps avoid overdrafts and keeps you aware of your finances. Is there a specific bank you use?"
            
        elif "review" in combined_text or "weekly" in combined_text:
            return "Weekly account reviews are crucial. Set aside 15 minutes each week to check transactions, look for errors, and ensure your spending aligns with your budget. Many banks offer spending summaries to make this easier. Do you currently review your accounts regularly?"
            
        elif "categor" in combined_text or "spending" in combined_text:
            return "Tools like Mint, YNAB, or even your bank's mobile app can automatically categorize spending to show where your money goes. This helps identify areas to cut back. Have you tried any budgeting apps before?"
            
        else:
            # End the flow if we can't identify their interest
            dialogue_manager.end_flow()
            return "For effective account management, consistent monitoring and planning are key. Start with weekly reviews and automated alerts, then consider using budgeting tools for deeper insights. Let me know if you have more specific questions!"
    
    # Third step in the balance conversation
    elif step == 2:
        # End the flow after giving specific advice
        dialogue_manager.end_flow()
        return "I hope this information helps you manage your accounts more effectively! Maintaining awareness of your finances is the first step toward financial freedom. Is there anything else I can help with?"

def handle_stock_flow(intent: Intent, dialogue_manager: DialogueManager, step: int):
    # First message after getting stock price
    ticker = dialogue_manager.context.get("current_ticker", "the stock")
    
    if step == 0:
        dialogue_manager.next_flow_step()
        simple_responses = [e for e in intent.entities if e.type == "simple_response"]
        
        # User wants more info about the stock
        if simple_responses and simple_responses[0].value == "yes":
            return f"{ticker} has shown strong performance recently with a positive trend in the last quarter. The company reported earnings above expectations. Would you like to know about analyst recommendations for {ticker}?"
        
        # User doesn't want more info
        elif simple_responses and simple_responses[0].value == "no":
            dialogue_manager.end_flow()
            return "No problem. Let me know if you want to check any other stock prices or have other financial questions."
            
        # Other response
        else:
            dialogue_manager.end_flow()
            return f"I've provided the current price for {ticker}. If you'd like more detailed analysis or information about other stocks, just let me know."
    
    # Second step in the stock conversation
    elif step == 1:
        dialogue_manager.next_flow_step()
        simple_responses = [e for e in intent.entities if e.type == "simple_response"]
        
        # User wants analyst recommendations
        if simple_responses and simple_responses[0].value == "yes":
            return f"Analysts currently have mixed opinions on {ticker}. Some see growth potential based on upcoming product launches, while others are concerned about market competition. The average price target is about 15% above the current price. Would you like to know about the risks associated with this stock?"
        
        # User doesn't want recommendations
        else:
            dialogue_manager.end_flow()
            return f"I understand. Remember that stock prices fluctuate and past performance doesn't guarantee future results. Let me know if you have other questions about {ticker} or other stocks."
    
    # Third step in the stock conversation
    elif step == 2:
        # End the flow after giving risk information
        dialogue_manager.end_flow()
        return f"The main risks for {ticker} include market competition, regulatory challenges, and general market volatility. Always consider your investment timeframe and risk tolerance before investing. Is there anything else you'd like to know about investing?"

def handle_budget_flow(intent: Intent, dialogue_manager: DialogueManager, step: int):
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
                return f"Great! If you want to save {budget_amount}, let's create a plan. The 50/30/20 rule is a good starting point: 50% for necessities, 30% for wants, and 20% for savings. Would you like a more detailed breakdown?"
            else:
                return "Saving is an excellent goal! The 50/30/20 rule is a good starting point: 50% for necessities, 30% for wants, and 20% for savings. Would you like to know more about this approach?"
        
        elif "debt" in combined_text or "loan" in combined_text or "pay off" in combined_text:
            dialogue_manager.context["budget_goal"] = "debt"
            return "Paying off debt is a smart financial decision. I recommend using either the avalanche method (paying off highest interest first) or the snowball method (paying off smallest debts first). Which approach sounds more appealing to you?"
        
        elif "emergency" in combined_text or "fund" in combined_text:
            dialogue_manager.context["budget_goal"] = "emergency"
            return "Building an emergency fund is crucial! Aim for 3-6 months of expenses. Would you like some tips to build this fund more quickly?"
        
        # Generic response if we can't determine their specific goal
        else:
            if simple_responses and simple_responses[0].value == "yes":
                return "Great! Let's talk about your budget. First, what's your primary financial goal right now? Are you trying to save money, pay off debt, or create an emergency fund?"
            elif simple_responses and simple_responses[0].value == "no":
                dialogue_manager.end_flow()
                return "No problem. If you need budgeting advice in the future, just let me know."
            else:
                return "To create an effective budget, let's start with your financial goals. Are you trying to save for something specific, pay off debt, or build an emergency fund?"
    
    # Second step in the budget conversation
    elif step == 1:
        dialogue_manager.next_flow_step()
        budget_goal = dialogue_manager.context.get("budget_goal", "")
        
        simple_responses = [e for e in intent.entities if e.type == "simple_response"]
        
        if budget_goal == "saving":
            if simple_responses and simple_responses[0].value == "yes":
                return "Here's a more detailed breakdown: From your income, allocate 50% to needs (rent, utilities, groceries), 30% to wants (entertainment, dining out), and 20% to savings and debt repayment. Track all expenses for a month to see where your money goes. Would you like specific expense-tracking tools recommendations?"
            else:
                dialogue_manager.end_flow()
                return "The 50/30/20 rule provides a simple framework to manage your finances. Adjust percentages based on your specific situation and goals. Is there anything else I can help with?"
        
        elif budget_goal == "debt":
            text_entities = [e.value.lower() for e in intent.entities if e.type == "text"]
            combined_text = " ".join(text_entities)
            
            if "avalanche" in combined_text:
                return "The avalanche method is mathematically optimal. List all debts by interest rate, make minimum payments on all, and put extra money toward the highest-interest debt. Would you like a tool recommendation to help manage this approach?"
            elif "snowball" in combined_text:
                return "The snowball method is great for motivation. List debts from smallest to largest balance, make minimum payments on all, and put extra money toward the smallest debt. Would you like a tool recommendation to help manage this approach?"
            else:
                return "Both methods work well. Avalanche saves more money long-term by targeting high-interest debt first. Snowball provides quick wins by eliminating small debts first, which can be motivating. Which method interests you more?"
        
        elif budget_goal == "emergency":
            if simple_responses and simple_responses[0].value == "yes":
                return "To build an emergency fund faster: 1) Set up automatic transfers to savings on payday, 2) Save all unexpected income (tax refunds, bonuses), 3) Cut unnecessary expenses temporarily and redirect that money to savings. Would you like to know about high-yield savings accounts for your emergency fund?"
            else:
                dialogue_manager.end_flow()
                return "Having an emergency fund is essential for financial security. Aim to save a small amount consistently until you reach your goal. Is there anything else I can help with?"
        
        else:
            # Generic advice if we couldn't determine their specific goal
            return "Creating a budget starts with tracking all income and expenses for a month. Once you know where your money is going, you can make informed decisions about where to cut back. Would you like some recommendations for budgeting tools to help with this?"
    
    # Third step in the budget conversation
    elif step == 2:
        # End the flow after giving specific advice
        dialogue_manager.end_flow()
        
        # Final advice based on their responses
        if "budget_goal" in dialogue_manager.context:
            goal = dialogue_manager.context.get("budget_goal")
            
            if goal == "saving":
                return "Great tools for expense tracking include Mint, YNAB (You Need A Budget), or even a simple spreadsheet. The key is consistency in tracking and reviewing your spending regularly. Is there anything else I can help with?"
            
            elif goal == "debt":
                return "Apps like Debt Payoff Planner or Undebt.it can help you implement either the avalanche or snowball method. They provide visual progress tracking which can be motivating. Remember, consistency is key to becoming debt-free. Is there anything else I can help with?"
            
            elif goal == "emergency":
                return "High-yield savings accounts at online banks typically offer better interest rates than traditional banks, helping your emergency fund grow faster. Look for accounts with no monthly fees and easy access in emergencies. Is there anything else I can help with?"
        
        return "Remember that a budget is a living document that should be adjusted as your income and expenses change. Review it regularly and make adjustments as needed. Is there anything else I can help with regarding your finances?"

# Load patterns for matching user intents
with open("patterns.json") as f:
    PATTERNS = [{"intent": p["intent"], "regex": re.compile(p["pattern"], re.IGNORECASE)} for p in json.load(f)]

# Load response templates
with open("answers.json") as f:
    ANSWERS = json.load(f)