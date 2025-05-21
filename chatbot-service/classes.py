#create a class for intent and entity and dialogue manager
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
        self.last_question = None  # Track the last question asked to the user
        self.current_flow = None   # Track the current conversation flow
        self.flow_step = 0         # Track the step within the current flow

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
    
    def set_last_question(self, question_type, options=None):
        """Record the last question asked to the user with potential expected answers"""
        self.last_question = {
            'type': question_type,
            'options': options
        }
        
    def get_last_question(self):
        """Get information about the last question asked to the user"""
        return self.last_question
        
    def start_flow(self, flow_name):
        """Start a new conversation flow"""
        self.current_flow = flow_name
        self.flow_step = 0
        
    def next_flow_step(self):
        """Move to the next step in the current flow"""
        if self.current_flow:
            self.flow_step += 1
            
    def get_flow_state(self):
        """Get the current flow state"""
        return {
            'flow': self.current_flow,
            'step': self.flow_step
        }
        
    def end_flow(self):
        """End the current conversation flow"""
        self.current_flow = None
        self.flow_step = 0


