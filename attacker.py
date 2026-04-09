import requests
import time
import random

def attack():
    print("🔥 ATTACKER SIMULATION STARTED")
    print("⚠️ Trying to bypass security...")
    print("-" * 50)
    
    for i in range(10):
        malicious_commands = [
            "ROTATE_ROTATE_ROTATE",
            "HACK_ACCESS",
            "TRANSMIT_ALL_DATA",
            "POWER_OFF",
            "DELETE_LOGS",
            "UNKNOWN_CMD_XYZ"
        ]
        cmd = random.choice(malicious_commands)
        
        try:
            # Attack with no encryption and fake token
            response = requests.post(
                'http://localhost:5000/send_command',
                json={"command": cmd},
                headers={"Authorization": "fake_token_123"}
            )
            
            if response.status_code == 403:
                print(f"🚨 Attack {i+1}: {cmd} -> BLOCKED by AI Defense")
            elif response.status_code == 401:
                print(f"🚨 Attack {i+1}: {cmd} -> BLOCKED (Invalid Token)")
            else:
                print(f"⚠️ Attack {i+1}: {cmd} -> {response.status_code}: {response.json()}")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ Attack {i+1}: Connection failed - Satellite offline?")
        except Exception as e:
            print(f"❌ Attack {i+1}: Error - {e}")
        
        time.sleep(0.3)  # Rapid fire attacks
    
    print("-" * 50)
    print("🏁 Attack simulation completed")

if __name__ == '__main__':
    attack()