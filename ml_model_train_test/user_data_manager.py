import json
import os
import hashlib
from datetime import datetime

USERS_FILE = os.path.join(os.path.dirname(__file__), 'users.json')

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_users(users_data):
    with open(USERS_FILE, 'w') as f:
        json.dump(users_data, f, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(first_name, last_name, email, phone, college, branch, year, cgpa, password):
    users = load_users()
    
    if email in users:
        return False, "Email already registered."
    
    users[email] = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone": phone,
        "college": college,
        "branch": branch,
        "year": year,
        "cgpa": cgpa,
        "password": hash_password(password),
        "predictions": []
    }
    
    save_users(users)
    return True, "User created successfully."

def authenticate_user(email, password):
    users = load_users()
    if email not in users:
        return False, None
    
    if users[email]['password'] == hash_password(password):
        user_data = users[email].copy()
        del user_data['password'] # Don't return password hash in session
        return True, user_data
    
    return False, None

def save_prediction(email, input_data, prediction_result, confidence):
    users = load_users()
    if email not in users:
        return False, "User not found."
    
    prediction_record = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "input_data": input_data,
        "prediction": int(prediction_result),
        "confidence": float(confidence)
    }
    
    if "predictions" not in users[email]:
        users[email]["predictions"] = []
        
    users[email]["predictions"].append(prediction_record)
    save_users(users)
    return True, "Prediction saved."
