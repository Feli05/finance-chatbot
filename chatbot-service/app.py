from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from chatbot import generate_response
from classes import DialogueManager
from classify_input import detect_intent

load_dotenv()

app = Flask(__name__)

# Create a global dialogue manager instance
dialogue_manager = DialogueManager()

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    try:
        return jsonify({
            'status': 'healthy',
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
        }), 500

# Endpoint to receive messages from the web service
@app.route('/chat/ask', methods=['POST'])
def get_question():
    """ 
    Receive data from the web service and process it to generate a response. 
    """   
    data = request.json
    message = data.get('message')

    # Process message using the new intent-based system
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