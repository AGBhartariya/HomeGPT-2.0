import requests
import random
import html

def get_quiz_question():
    try:
        res = requests.get("https://opentdb.com/api.php?amount=1&type=multiple")
        data = res.json()
        question = html.unescape(data['results'][0]['question'])
        correct = html.unescape(data['results'][0]['correct_answer'])
        incorrect = [html.unescape(ans) for ans in data['results'][0]['incorrect_answers']]
        options = incorrect + [correct]
        random.shuffle(options)
        return question, correct, options
    except:
        return None, None, []