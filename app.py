from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from pymongo import MongoClient
import jwt
import datetime
import threading
import uvicorn
import pyttsx3
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# ------------------ Flask App (User Authentication & Scores) ------------------

flask_app = Flask(_name_)
flask_app.config['SECRET_KEY'] = 'b00334de0d6ed3d77e5c6db80d911dd43fbc23fe92587451403387adf419c2e5'
bcrypt = Bcrypt(flask_app)
CORS(flask_app)

# ✅ Simulated user scores (Replace with database in production)
user_scores = {}

# ✅ MongoDB Setup
try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["UserAuthDB"]
    users_collection = db["users"]
    users_collection.create_index("email", unique=True)
    print("✅ Connected to MongoDB successfully")
except Exception as e:
    print(f"❌ Error connecting to MongoDB: {e}")

# ✅ Register User
@flask_app.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    if users_collection.find_one({"email": email}):
        return jsonify({"message": "Email already exists"}), 400

    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    user_data = {"email": email, "password": hashed_pw}

    try:
        insert_result = users_collection.insert_one(user_data)
        print(f"✅ User inserted with ID: {insert_result.inserted_id}")
        print("✅ User details stored in MongoDB:", user_data)
    except Exception as e:
        print(f"❌ Error inserting user into MongoDB: {e}")
        return jsonify({"message": "Error registering user"}), 500

    return jsonify({"message": "User registered successfully"}), 201

# ✅ Login
@flask_app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    user = users_collection.find_one({"email": email})
    if user is None:
        print(f"❌ Login failed: User not found - {email}")
        return jsonify({"message": "Invalid credentials"}), 401

    print(f"✅ User found: {user}")
    if bcrypt.check_password_hash(user['password'], password):
        token = jwt.encode(
            {'email': email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
            flask_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        print(f"✅ Login successful for {email}")
        return jsonify({"message": "Login successful", "token": token}), 200

    print(f"❌ Invalid password for {email}")
    return jsonify({"message": "Invalid credentials"}), 401

# ✅ Upload Certificate (Update score)
@flask_app.route('/upload', methods=['POST'])
def upload_certificate():
    user_id = request.json.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID required"}), 400

    user_scores[user_id] = user_scores.get(user_id, 0) + 10
    return jsonify({"message": "Certificate uploaded successfully", "new_score": user_scores[user_id]})

# ✅ Get Score
@flask_app.route('/get_score/<user_id>', methods=['GET'])
def get_score(user_id):
    score = user_scores.get(user_id, 0)
    return jsonify({"user_id": user_id, "score": score})

# ------------------ FastAPI App (Chatbot) ------------------

fastapi_app = FastAPI()
fastapi_app.mount("/static", StaticFiles(directory="static"), name="static")

def chatbot_response(input_text):
    responses = {
        "hello": "Hello! How can I help you?",
        "hi": "Hello! How can I help you?",
        "hiii": "Hello! How can I help you?",
        "how are you": "I am doing great. Thank you.",
        "bye": "Goodbye! Come back whenever you need help.",
    }
    response = responses.get(input_text.lower().strip(), "I'm still learning! I'll improve and help you soon.")
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(response)
    engine.runAndWait()
    return response

@fastapi_app.post("/chat")
async def chat(input_data: dict):
    input_text = input_data.get("message", "")
    response = chatbot_response(input_text)
    return {"response": response}

@fastapi_app.get("/")
async def serve_frontend():
    return FileResponse("static/index.html")

# ------------------ Run Flask + FastAPI Simultaneously ------------------

if _name_ == "_main_":
    def run_flask():
        flask_app.run(debug=True, port=5001, use_reloader=False)

    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    uvicorn.run(fastapi_app, host="127.0.0.1", port=5000)
