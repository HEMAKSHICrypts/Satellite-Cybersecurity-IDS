from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
from cryptography.fernet import Fernet
import pickle
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Load AI model
with open('isolation_forest.pkl', 'rb') as f:
    model = pickle.load(f)

# Secret keys
SECRET_KEY = "your-super-secret-jwt-key"
# FIXED KEY - Never changes (Save this once)
CIPHER_KEY = b'3vAGLpQZXWboSOyNMcpXy65wVZkCz3cPF5iLui_aiGM='
cipher = Fernet(CIPHER_KEY)

print(f"🔑 Using FIXED cipher key: {CIPHER_KEY.decode()}")

# Blocked IPs for self-healing
blocked_ips = set()
failed_attempts = {}

def calculate_anomaly_score(command_data):
    df = pd.DataFrame([command_data])
    score = model.decision_function(df)[0]
    return score

def get_risk_level(score):
    if score < -0.6:
        return "CRITICAL"
    elif score < -0.4:
        return "HIGH"
    elif score < -0.2:
        return "MEDIUM"
    else:
        return "LOW"

@app.route('/send_command', methods=['POST'])
def send_command():
    client_ip = request.remote_addr
    
    # Self-healing: Check if IP is blocked
    if client_ip in blocked_ips:
        return jsonify({"status": "BLOCKED", "reason": "IP is banned"}), 403
    
    try:
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"status": "UNAUTHORIZED"}), 401
        
        # Verify JWT
        jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        
        # Decrypt command
        encrypted_cmd = request.json.get('command')
        command = cipher.decrypt(encrypted_cmd.encode()).decode()
        
        # Extract features for AI
        hour = datetime.now().hour
        cmd_map = {'CAPTURE':0, 'TRANSMIT':1, 'ROTATE':2, 'POWER':3}
        cmd_type = cmd_map.get(command.split()[0], 0)
        
        features = {
            'hour': hour,
            'cmd_type': cmd_type,
            'interval': 10,
            'unknown_ip': 1 if client_ip not in ['192.168.1.1', '127.0.0.1'] else 0
        }
        
        score = calculate_anomaly_score(features)
        risk = get_risk_level(score)
        
        # Self-healing: Block if HIGH or CRITICAL
        if risk in ["HIGH", "CRITICAL"]:
            blocked_ips.add(client_ip)
            return jsonify({
                "status": "ATTACK_BLOCKED",
                "risk": risk,
                "score": float(score)
            }), 403
        
        return jsonify({
            "status": "EXECUTED",
            "command": command,
            "risk": risk,
            "score": float(score)
        })
    
    except jwt.InvalidTokenError:
        return jsonify({"status": "INVALID_TOKEN"}), 401
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ONLINE", "blocked_ips": len(blocked_ips)})

if __name__ == '__main__':
    print("🛰️ Satellite Defense System Running on Port 5000")
    app.run(host='0.0.0.0', port=5000, debug=True)