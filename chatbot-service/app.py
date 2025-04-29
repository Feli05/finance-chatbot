from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

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

    # Process message, send a default response for now

    response = {
        'message': 'This is a default response'
    }
    return jsonify(response), 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5050))
    app.run(host='0.0.0.0', port=port, debug=True) 