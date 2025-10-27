from cryptography.fernet import Fernet
from config import ENCRYPTION_KEY
import json

# Initialize Fernet for encryption/decryption
cipher_suite = Fernet(ENCRYPTION_KEY)

def encrypt_data(data_string):
    """Encrypts a string (e.g., API key, JSON config)."""
    if not data_string:
        return None
    encoded_data = data_string.encode()
    encrypted_data = cipher_suite.encrypt(encoded_data)
    return encrypted_data.decode() # Store as text in DB

def decrypt_data(encrypted_data_string):
    """Decrypts a string from the database."""
    if not encrypted_data_string:
        return None
    encrypted_data = encrypted_data_string.encode()
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    return decrypted_data.decode()

def get_mpesa_config(connected_bot_id):
    """
    Retrieves and decrypts the M-Pesa configuration for a connected bot.
    (Requires a database function to fetch the encrypted config JSON)
    """
    # Placeholder: In your full system, you would fetch the encrypted JSON 
    # from the `payment_configs` table here.
    
    # Example data flow:
    # 1. Fetch encrypted_config_json from DB where connected_bot_id = X AND gateway = 'MPESA'
    # 2. decrypted_json_string = decrypt_data(encrypted_config_json)
    # 3. config = json.loads(decrypted_json_string)
    # 4. return config
    
    return {"status": "WIP: Implement DB fetch and decrypt here"}
