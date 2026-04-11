from cryptography.fernet import Fernet

# Generate a proper 32-byte key
key = Fernet.generate_key()
print(f"Copy this exact key: {key.decode()}")
print(f"Key length: {len(key.decode())} characters")