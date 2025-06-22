import pandas as pd
import random

def get_quiz_questions(category="Bollywood", difficulty="Easy", num_questions=5):
    df = pd.read_csv("quiz_questions.csv")
    filtered = df[(df["category"] == category) & (df["difficulty"] == difficulty)]
    questions = filtered.sample(n=min(num_questions, len(filtered))).to_dict(orient="records")
    return questions

import streamlit as st
import random

def word_scramble_game():
    st.subheader("🔤 Word Scramble")
    st.write("Unscramble the word! Can you guess it?")

    word_list = [
    "apple", "banana", "orange", "grape", "peach", "mango", "lemon", "melon", "kiwi", "pear",
    "chair", "table", "bed", "sofa", "lamp", "desk", "shelf", "stool", "rug", "couch",
    "car", "bike", "bus", "train", "plane", "boat", "scooter", "truck", "van", "taxi",
    "cat", "dog", "mouse", "horse", "sheep", "goat", "tiger", "lion", "monkey", "zebra",
    "book", "pen", "pencil", "paper", "eraser", "ruler", "notebook", "marker", "crayon", "stapler",
    "milk", "water", "juice", "soda", "coffee", "tea", "soup", "bread", "rice", "pizza",
    "phone", "laptop", "tablet", "camera", "speaker", "printer", "screen", "monitor", "keyboard", "mouse",
    "shirt", "pants", "shorts", "dress", "skirt", "shoes", "socks", "hat", "gloves", "jacket",
    "door", "window", "wall", "floor", "ceiling", "roof", "stairs", "balcony", "garage", "garden",
    "egg", "cheese", "butter", "jam", "honey", "salt", "sugar", "pepper", "oil", "vinegar",
    "cloud", "rain", "snow", "storm", "wind", "sun", "fog", "hail", "ice", "lightning",
    "bag", "wallet", "purse", "backpack", "suitcase", "belt", "watch", "ring", "bracelet", "necklace",
    "movie", "music", "song", "dance", "game", "puzzle", "quiz", "race", "match", "show",
    "doctor", "nurse", "teacher", "student", "driver", "chef", "police", "guard", "pilot", "farmer",
    "school", "college", "office", "library", "hospital", "market", "restaurant", "theater", "stadium", "zoo",
    "air", "fire", "water", "earth", "space", "time", "light", "dark", "sound", "energy",
    "happy", "sad", "angry", "tired", "excited", "nervous", "bored", "scared", "proud", "calm",
    "clean", "dirty", "hot", "cold", "dry", "wet", "soft", "hard", "empty", "full"
    ]


    # Initialize session states
    if "scramble_round" not in st.session_state:
        st.session_state.scramble_round = 0
    if "scramble_score" not in st.session_state:
        st.session_state.scramble_score = 0
    if "scramble_streak" not in st.session_state:
        st.session_state.scramble_streak = 0
    if "scramble_best_streak" not in st.session_state:
        st.session_state.scramble_best_streak = 0
    if "scramble_new" not in st.session_state:
        st.session_state.scramble_new = True
    if "scramble_correct" not in st.session_state:
        st.session_state.scramble_correct = False

    # Generate new word if needed
    if st.session_state.scramble_new:
        while True:
            word = random.choice(word_list)
            scrambled = "".join(random.sample(word, len(word)))
            if scrambled != word:
                break
        st.session_state.scramble_word = word
        st.session_state.scrambled = scrambled
        st.session_state.scramble_attempts = 0
        st.session_state.scramble_new = False
        st.session_state.scramble_correct = False

    st.write(f"Scrambled word: **{st.session_state.scrambled}**")

    guess = st.text_input("Your guess:", key=f"scramble_guess_{st.session_state.scramble_round}")

    col1, col2 = st.columns([1, 1])
    with col1:
        submit = st.button("✅ Submit", key=f"scramble_submit_{st.session_state.scramble_round}")
    with col2:
        skip = st.button("⏭️ Skip", key=f"scramble_skip_{st.session_state.scramble_round}")

    if submit:
        st.session_state.scramble_attempts += 1
        if guess.lower() == st.session_state.scramble_word:
            points = max(10 - st.session_state.scramble_attempts + 1, 1)
            st.session_state.scramble_score += points
            st.session_state.scramble_streak += 1
            st.session_state.scramble_correct = True

            if st.session_state.scramble_streak > st.session_state.scramble_best_streak:
                st.session_state.scramble_best_streak = st.session_state.scramble_streak

            st.success(f"🎉 Correct! The word was '{st.session_state.scramble_word}'. Attempts: {st.session_state.scramble_attempts}, Points: {points}")
            st.info(f"🔥 Streak: {st.session_state.scramble_streak} | 🥇 Best: {st.session_state.scramble_best_streak}")
        else:
            st.session_state.scramble_streak = 0
            st.error("❌ Incorrect. Try again!")

    if skip:
        st.warning(f"⏭️ Skipped! The word was '{st.session_state.scramble_word}'.")
        st.session_state.scramble_streak = 0
        st.session_state.scramble_round += 1
        st.session_state.scramble_new = True
        st.experimental_rerun()

    # ✅ Show "Play Again" ONLY if the word was correctly guessed
    if st.session_state.scramble_correct:
        if st.button("🔄 Play Again", key=f"scramble_restart_{st.session_state.scramble_round}"):
            st.session_state.scramble_round += 1
            st.session_state.scramble_new = True
            st.session_state.scramble_correct = False
            st.experimental_rerun()

    # Show stats
    st.markdown("---")
    st.write(f"🏆 Score: **{st.session_state.scramble_score}**")
    st.write(f"🔥 Current Streak: **{st.session_state.scramble_streak}**")
    st.write(f"🥇 Best Streak: **{st.session_state.scramble_best_streak}**")


def math_challenge_game():
    st.subheader("➕ Math Challenge")
    st.write("Try to solve each math puzzle. Let’s see how far you can go!")

    operators = ["+", "-", "*", "/", "**"]

    # Initialize state variables
    if "math_score" not in st.session_state:
        st.session_state.math_score = 0
    if "math_attempts" not in st.session_state:
        st.session_state.math_attempts = 0
    if "math_streak" not in st.session_state:
        st.session_state.math_streak = 0
    if "math_best_streak" not in st.session_state:
        st.session_state.math_best_streak = 0

    # Generate new question
    if "math_question" not in st.session_state or st.session_state.get("math_new", True):
        op = random.choice(operators)

        if op == "+":
            num1, num2 = random.randint(10, 99), random.randint(10, 99)
            answer = num1 + num2
            q = f"{num1} + {num2}"
        elif op == "-":
            num1, num2 = random.randint(50, 150), random.randint(10, 49)
            answer = num1 - num2
            q = f"{num1} - {num2}"
        elif op == "*":
            num1, num2 = random.randint(5, 20), random.randint(5, 20)
            answer = num1 * num2
            q = f"{num1} × {num2}"
        elif op == "/":
            num2 = random.randint(2, 12)
            answer = random.randint(2, 12)
            num1 = num2 * answer
            answer = round(num1 / num2, 2)
            q = f"{num1} ÷ {num2}"
        else:  # Exponent
            num1 = random.randint(2, 5)
            num2 = random.randint(2, 3)
            answer = num1 ** num2
            q = f"{num1}^{num2}"

        # Store question and answer
        st.session_state.math_question = q
        st.session_state.math_answer = answer
        st.session_state.math_new = False

    # Display question
    st.write(f"Solve: **{st.session_state.math_question} = ?**")
    user_ans = st.text_input("Your answer:", key=f"math_input_{st.session_state.math_attempts}")

    if st.button("Submit Answer", key=f"math_submit_{st.session_state.math_attempts}"):
        st.session_state.math_attempts += 1
        try:
            if float(user_ans.strip()) == float(st.session_state.math_answer):
                st.success("✅ Correct!")
                st.session_state.math_score += 10  # 10 points for correct
                st.session_state.math_streak += 1
                if st.session_state.math_streak > st.session_state.math_best_streak:
                    st.session_state.math_best_streak = st.session_state.math_streak
            else:
                st.error(f"❌ Incorrect. Correct answer: {st.session_state.math_answer}")
                st.session_state.math_score -= 2  # penalty for wrong
                st.session_state.math_streak = 0
            st.session_state.math_new = True
            st.experimental_rerun()
        except ValueError:
            st.warning("⚠️ Please enter a valid number.")

    # Show performance
    st.markdown("---")
    st.write(f"🏆 Score: **{st.session_state.math_score}**")
    st.write(f"📊 Attempts: **{st.session_state.math_attempts}**")
    if st.session_state.math_attempts > 0:
        accuracy = (st.session_state.math_score / (10 * st.session_state.math_attempts)) * 100
        st.write(f"🎯 Accuracy: **{accuracy:.1f}%**")
    st.write(f"🔥 Current Streak: **{st.session_state.math_streak}**")
    st.write(f"🥇 Best Streak: **{st.session_state.math_best_streak}**")
