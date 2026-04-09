import requests
import jwt
from cryptography.fernet import Fernet
import time

SECRET_KEY = "your-super-secret-jwt-key"

# ⚠️ IMPORTANT: Replace this with the cipher key from satellite.py
# When you run satellite.py, it will print:
# "🔑 Save this cipher key for ground_station.py: b'...'"
# Copy that exact key here:
CIPHER_KEY = b'REPLACE_THIS_WITH_THE_KEY_FROM_SATELLITE_PY'

cipher = Fernet(CIPHER_KEY)

def send_command(command):
    token = jwt.encode({"role": "ground_station"}, SECRET_KEY, algorithm='HS256')
    encrypted = cipher.encrypt(command.encode()).decode()
    
    response = requests.post(
        'http://localhost:5000/send_command',
        json={"command": encrypted},
        headers={"Authorization": token}
    )
    return response.json()

if __name__ == '__main__':
    print("📡 Ground Station - Sending Test Commands")
    print("-" * 50)
    
    commands = ["CAPTURE_IMAGE", "TRANSMIT_DATA", "ROTATE_10DEG", "POWER_OFF"]
    
    for cmd in commands:
        result = send_command(cmd)
        print(f"📤 Command: {cmd}")
        print(f"📥 Response: {result}")
        print("-" * 30)
        time.sleep(2)