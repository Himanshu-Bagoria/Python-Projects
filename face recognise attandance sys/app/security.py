import os
import sqlite3
from cryptography.fernet import Fernet
import json
import numpy as np

# Generate or load a key for encryption
KEY_FILE = "data/secret.key"

def load_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
    else:
        with open(KEY_FILE, "rb") as key_file:
            key = key_file.read()
    return key

FERNET = Fernet(load_key())

def encrypt_embedding(embedding):
    """Encrypts a list/numpy array embedding."""
    data = json.dumps(embedding.tolist() if isinstance(embedding, np.ndarray) else embedding).encode()
    return FERNET.encrypt(data)

def decrypt_embedding(encrypted_data):
    """Decrypts and returns the embedding list."""
    decrypted_data = FERNET.decrypt(encrypted_data)
    return json.loads(decrypted_data.decode())

def log_event(user_id, action):
    """Logs an attendance or security event in the UsageLogs table."""
    conn = sqlite3.connect("data/database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO UsageLogs (user_id, action) VALUES (?, ?)", (user_id, action))
    conn.commit()
    conn.close()
