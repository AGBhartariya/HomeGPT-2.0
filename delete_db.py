import os

if os.path.exists("users.db"):
    os.remove("users.db")
    print("users.db deleted successfully.")
else:
    print("users.db does not exist.")
