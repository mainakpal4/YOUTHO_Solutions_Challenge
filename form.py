from flask import Flask, request, jsonify

app = Flask(__name__)

# Simulating user scores (use a database in production)
user_scores = {}

@app.route('/upload', methods=['POST'])
def upload_certificate():
    user_id = request.json.get('user_id')  # Get user ID
    if not user_id:
        return jsonify({"error": "User ID required"}), 400

    user_scores[user_id] = user_scores.get(user_id, 0) + 10  # Increase score by 10
    return jsonify({"message": "Certificate uploaded successfully", "new_score": user_scores[user_id]})

@app.route('/get_score/<user_id>', methods=['GET'])
def get_score(user_id):
    score = user_scores.get(user_id, 0)
    return jsonify({"user_id": user_id, "score": score})

if __name__ == '__main__':
    app.run(debug=True)