import json
import os
from cryptography.fernet import Fernet

# Set up encryption key
KEY_FILE = "secret.key"
if not os.path.exists(KEY_FILE):
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
else:
    with open(KEY_FILE, "rb") as f:
        key = f.read()
cipher = Fernet(key)

PASSWORD_FILE = "passwords.json"

def initialize_passwords_file():
    """Ensure the passwords file exists and is valid JSON."""
    if not os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, "w") as f:
            json.dump({"passwords": []}, f)
    else:
        try:
            with open(PASSWORD_FILE, "r") as f:
                json.load(f)
        except json.JSONDecodeError:
            with open(PASSWORD_FILE, "w") as f:
                json.dump({"passwords": []}, f)

def save_password(site, password, user):
    """Encrypt and save a password for a site and user."""
    initialize_passwords_file()
    try:
        with open(PASSWORD_FILE, "r+") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {"passwords": []}
            encrypted_password = cipher.encrypt(password.encode()).decode()
            # Check if entry exists
            found = False
            for entry in data["passwords"]:
                if entry["site"] == site and entry["user"] == user:
                    entry["password"] = encrypted_password
                    found = True
                    break
            if not found:
                data["passwords"].append({
                    "site": site,
                    "user": user,
                    "password": encrypted_password
                })
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()
        return True
    except Exception as e:
        print(f"Error saving password: {e}")
        return False

def retrieve_password(site, user):
    """Retrieve and decrypt a password for a site and user."""
    initialize_passwords_file()
    try:
        with open(PASSWORD_FILE, "r") as f:
            data = json.load(f)
        for entry in data["passwords"]:
            if entry["site"] == site and entry["user"] == user:
                try:
                    decrypted = cipher.decrypt(entry["password"].encode()).decode()
                    return decrypted
                except Exception as e:
                    print(f"Error decrypting password: {e}")
                    return None
        return None
    except Exception as e:
        print(f"Error retrieving password: {e}")
        return None

# Dummy function for compatibility; does nothing
def capture_live_image(user):
    return None
