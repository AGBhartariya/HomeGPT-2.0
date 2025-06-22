import pandas as pd
import random

def get_quiz_questions(category="Bollywood", difficulty="Easy", num_questions=5):
    df = pd.read_csv("quiz_questions.csv")
    filtered = df[(df["category"] == category) & (df["difficulty"] == difficulty)]
    questions = filtered.sample(n=min(num_questions, len(filtered))).to_dict(orient="records")
    return questions
