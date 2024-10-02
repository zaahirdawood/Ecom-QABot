from flask import Flask, request, jsonify
import uuid
from src.ecom_bot.rag import rag


app = Flask(__name__)

@app.route('/question', methods=['POST'])
def process_question():
    data = request.json
    question = data['question']
    if not question:

        return jsonify({"error": "No question provided"}), 400
    
    conversation_id = str(uuid.uuid4())  
    
    answer = rag(question) 
    
    result= {"conversation_id": conversation_id,
             "answer": answer}
    
    
    return jsonify(result)

@app.route('/feedback', methods=['POST'])
def process_feedback():
    data = request.json
    conversation_id = data['conversation_id']
    feedback = data['feedback']
    
    if not conversation_id or feedback not in [1, -1]:
        return jsonify({"error": "Invalid input"}), 400

    result = {
        "message": f"Feedback received for conversation {conversation_id}: {feedback}"
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)


