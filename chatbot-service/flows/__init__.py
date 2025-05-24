from flows.savings_flow import handle_flow as handle_savings_flow
from flows.investment_flow import handle_flow as handle_investment_flow
from flows.balance_flow import handle_flow as handle_balance_flow
from flows.stock_flow import handle_flow as handle_stock_flow
from flows.budget_flow import handle_flow as handle_budget_flow

FLOW_HANDLERS = {
    "savings_flow": handle_savings_flow,
    "investment_flow": handle_investment_flow,
    "balance_flow": handle_balance_flow,
    "stock_flow": handle_stock_flow,
    "budget_flow": handle_budget_flow
} 