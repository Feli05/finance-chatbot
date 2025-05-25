from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from chatbot import generate_response
from classes import DialogueManager
from classify_input import detect_intent

load_dotenv()

app = Flask(__name__)

dialogue_manager = DialogueManager()

@app.route('/chat/ask', methods=['POST'])
def get_question(): 
    data = request.json
    message = data.get('message')

    intent = detect_intent(message)
    dialogue_manager.update(intent)
    response_message = generate_response(intent, dialogue_manager)

    print(response_message)

    response = {
        'message': response_message
    }
    
    return jsonify(response), 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5051))
    app.run(host='0.0.0.0', port=port, debug=True) 