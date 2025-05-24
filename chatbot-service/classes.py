from datetime import datetime

class Entity:
    def __init__(self, type: str, value: str, confidence: float = 1.0):
        self.type = type
        self.value = value
        self.confidence = confidence
        
class Intent:
    def __init__(self, name: str, confidence: float, entities: list[Entity]):
        self.name = name
        self.confidence = confidence
        self.entities = entities


class DialogueManager:
    def __init__(self):
        self.history = []  
        self.context = {}  
        self.max_history = 10
        self.current_flow = None   
        self.flow_step = 0         

    def update(self, intent: Intent):
        self.history.append((intent, datetime.now()))
        if len(self.history) > self.max_history:
            self.history.pop(0)
        
        self._update_context(intent)

    def _update_context(self, intent: Intent):
        # Store last mentioned tickers
        tickers = [e.value for e in intent.entities if e.type == "ticker"]
        if tickers:
            self.context["last_tickers"] = tickers

        # Store last mentioned amount
        amounts = [e.value for e in intent.entities if e.type == "amount"]
        if amounts:
            self.context["last_amount"] = amounts[-1]
            
        # Store last mentioned percentage
        percentages = [e.value for e in intent.entities if e.type == "percentage"]
        if percentages:
            self.context["last_percentage"] = percentages[-1]

    def get_context(self):
        return self.context

    def last_intent(self):
        return self.history[-1][0] if self.history else None
        
    def start_flow(self, flow_name):
        self.current_flow = flow_name
        self.flow_step = 0
        
    def next_flow_step(self):
        if self.current_flow:
            self.flow_step += 1
            
    def reset_flow_step(self, step):
        if self.current_flow:
            self.flow_step = step
            
    def get_flow_state(self):
        return {
            'flow': self.current_flow,
            'step': self.flow_step
        }
        
    def end_flow(self):
        self.current_flow = None
        self.flow_step = 0


