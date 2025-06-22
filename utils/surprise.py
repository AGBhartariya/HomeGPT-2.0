import os
import random

def get_daily_quote():
    quotes = [
        "You’re my favorite notification every day 💬",
        "Every day with you is my favorite memory 💛",
        "Love doesn’t count the miles, it counts the memories 🛤️",
        "A hug in code is still a hug 🤗",
        "Forever connected by heart, not by cables ❤️"
    ]
    return random.choice(quotes)

def get_random_photo():
    photo_folder = "assets/photos"
    photos = [os.path.join(photo_folder, f) for f in os.listdir(photo_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    return random.choice(photos) if photos else None
