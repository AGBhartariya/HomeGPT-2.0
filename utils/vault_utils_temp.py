# utils/vault_utils_temp.py
import base64
import sqlite3
from cryptography.fernet import Fernet

def load_key():
    with open("secret.key", "rb") as key_file:
        return key_file.read()

key = load_key()
fernet = Fernet(key)

def encrypt_password(password: str) -> str:
    return fernet.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password: str) -> str:
    return fernet.decrypt(encrypted_password.encode()).decode()

def save_password(service, username, password):
    encrypted = encrypt_password(password)
    conn = sqlite3.connect("passwords.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS vault
                 (service TEXT, username TEXT, password TEXT)''')
    c.execute("INSERT INTO vault VALUES (?, ?, ?)", (service, username, encrypted))
    conn.commit()
    conn.close()

def get_passwords():
    conn = sqlite3.connect("passwords.db")
    c = conn.cursor()
    c.execute("SELECT service, username, password FROM vault")
    data = c.fetchall()
    conn.close()
    return [(s, u, decrypt_password(p)) for s, u, p in data]

 
