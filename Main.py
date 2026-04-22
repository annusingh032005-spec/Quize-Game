"""
🎯 Python Quiz Game
A feature-rich terminal quiz game with multiple categories, scoring, and timer.
"""

import random
import time
import json

# ─────────────────────────────────────────────
#  QUESTION BANK
# ─────────────────────────────────────────────

QUESTIONS = {
    "Python Basics": [
        {
            "question": "What is the output of: print(type([]))?",
            "options": ["A) <class 'tuple'>", "B) <class 'list'>", "C) <class 'dict'>", "D) <class 'set'>"],
            "answer": "B",
            "explanation": "[] creates an empty list, so type([]) returns <class 'list'>."
        },
        {
            "question": "Which keyword is used to define a function in Python?",
            "options": ["A) function", "B) func", "C) def", "D) define"],
            "answer": "C",
            "explanation": "'def' is the keyword used to define a function in Python."
        },
        {
            "question": "What does len('hello') return?",
            "options": ["A) 4", "B) 5", "C) 6", "D) Error"],
            "answer": "B",
            "explanation": "'hello' has 5 characters, so len() returns 5."
        },
        {
            "question": "Which of these is a valid Python comment?",
            "options": ["A) // comment", "B) /* comment */", "C) # comment", "D) <!-- comment -->"],
            "answer": "C",
            "explanation": "Python uses # for single-line comments."
        },
        {
            "question": "What is the result of 10 // 3 in Python?",
            "options": ["A) 3.33", "B) 3", "C) 4", "D) 1"],
            "answer": "B",
            "explanation": "// is floor division. 10 // 3 = 3 (discards the remainder)."
        },
    ],
    "Data Structures": [
        {
            "question": "Which data structure uses LIFO (Last In, First Out)?",
            "options": ["A) Queue", "B) Stack", "C) List", "D) Dictionary"],
            "answer": "B",
            "explanation": "A Stack follows LIFO — the last element pushed is the first popped."
        },
        {
            "question": "Which Python structure does NOT allow duplicate values?",
            "options": ["A) list", "B) tuple", "C) set", "D) dict values"],
            "answer": "C",
            "explanation": "A set automatically removes duplicate values."
        },
        {
            "question": "How do you access the value 'age' key in dict d = {'name':'Alice','age':30}?",
            "options": ["A) d.age", "B) d['age']", "C) d->age", "D) d.get_key('age')"],
            "answer": "B",
            "explanation": "Dictionary values are accessed using d['key'] syntax."
        },
        {
            "question": "What is the time complexity of accessing an element by index in a Python list?",
            "options": ["A) O(n)", "B) O(log n)", "C) O(1)", "D) O(n²)"],
            "answer": "C",
            "explanation": "List indexing is O(1) — direct memory access."
        },
    ],
    "OOP Concepts": [
        {
            "question": "What does 'self' refer to in a Python class method?",
            "options": ["A) The class itself", "B) The current instance", "C) The parent class", "D) A static variable"],
            "answer": "B",
            "explanation": "'self' refers to the current instance of the class."
        },
        {
            "question": "Which OOP concept allows a class to inherit from multiple classes?",
            "options": ["A) Polymorphism", "B) Encapsulation", "C) Multiple Inheritance", "D) Abstraction"],
            "answer": "C",
            "explanation": "Multiple inheritance allows a class to inherit from more than one parent class."
        },
        {
            "question": "What is the special method called when an object is created?",
            "options": ["A) __start__", "B) __create__", "C) __new__", "D) __init__"],
            "answer": "D",
            "explanation": "__init__ is the constructor method called when a new object is instantiated."
        },
    ],
    "General Knowledge": [
        {
            "question": "Who invented Python?",
            "options": ["A) James Gosling", "B) Guido van Rossum", "C) Linus Torvalds", "D) Bjarne Stroustrup"],
            "answer": "B",
            "explanation": "Guido van Rossum created Python in 1991."
        },
        {
            "question": "What does CPU stand for?",
            "options": ["A) Central Processing Unit", "B) Computer Power Unit", "C) Core Processing Utility", "D) Central Program Utility"],
            "answer": "A",
            "explanation": "CPU stands for Central Processing Unit — the brain of a computer."
        },
        {
            "question": "What does HTML stand for?",
            "options": ["A) Hyper Transfer Markup Language", "B) HyperText Markup Language", "C) High Text Machine Language", "D) Hyper Tool Markup Language"],
            "answer": "B",
            "explanation": "HTML stands for HyperText Markup Language."
        },
    ]
}


# ─────────────────────────────────────────────
#  DISPLAY HELPERS
# ─────────────────────────────────────────────

def clear_line():
    print()

def banner():
    print("=" * 55)
    print("  🎯  PYTHON QUIZ GAME  🎯")
    print("=" * 55)

def show_score_bar(score, total, width=30):
    if total == 0:
        return
    filled = int((score / total) * width)
    bar = "█" * filled + "░" * (width - filled)
    pct = (score / total) * 100
    print(f"  [{bar}] {pct:.0f}%")

def countdown(seconds=3):
    print("  Starting in: ", end="", flush=True)
    for i in range(seconds, 0, -1):
        print(f"{i}...", end=" ", flush=True)
        time.sleep(1)
    print("GO!\n")


# ─────────────────────────────────────────────
#  CORE GAME LOGIC
# ─────────────────────────────────────────────

def ask_question(q_data, q_num, total_q, timed=False, time_limit=15):
    """Display a question and get the player's answer."""
    print(f"\n  Question {q_num}/{total_q}")
    print("  " + "─" * 50)
    print(f"  {q_data['question']}\n")
    for opt in q_data["options"]:
        print(f"    {opt}")
    print()

    start = time.time()

    while True:
        if timed:
            elapsed = time.time() - start
            remaining = time_limit - elapsed
            if remaining <= 0:
                print("  ⏰  Time's up!")
                return None, time_limit
            prompt = f"  Your answer (A/B/C/D) [{remaining:.0f}s]: "
        else:
            prompt = "  Your answer (A/B/C/D): "

        user_input = input(prompt).strip().upper()

        if user_input in ("A", "B", "C", "D"):
            elapsed = time.time() - start
            return user_input, elapsed
        else:
            print("  ⚠️  Please enter A, B, C, or D.")


def run_quiz(questions, timed=False, time_limit=15):
    """Run the quiz and return score details."""
    score = 0
    results = []
    random.shuffle(questions)

    for i, q in enumerate(questions, 1):
        answer, time_taken = ask_question(q, i, len(questions), timed, time_limit)

        if answer is None:
            correct = False
        else:
            correct = (answer == q["answer"])

        if correct:
            score += 1
            # Bonus point for fast answers in timed mode
            bonus = 1 if (timed and time_taken < time_limit / 2) else 0
            score += bonus
            tag = "✅ Correct!" + (" (+1 speed bonus!)" if bonus else "")
        else:
            tag = f"❌ Wrong! Correct answer: {q['answer']}"

        print(f"\n  {tag}")
        print(f"  💡 {q['explanation']}")

        results.append({
            "question": q["question"],
            "your_answer": answer,
            "correct_answer": q["answer"],
            "correct": correct,
            "time_taken": round(time_taken, 2)
        })

        time.sleep(1.2)

    return score, results


# ─────────────────────────────────────────────
#  RESULTS & LEADERBOARD
# ─────────────────────────────────────────────

def show_results(name, score, results, category):
    total = len(results)
    correct = sum(1 for r in results if r["correct"])
    avg_time = sum(r["time_taken"] for r in results) / total if total else 0

    print("\n" + "=" * 55)
    print("  📊  QUIZ RESULTS")
    print("=" * 55)
    print(f"  Player : {name}")
    print(f"  Category: {category}")
    print(f"  Score   : {score} points")
    print(f"  Correct : {correct}/{total}")
    show_score_bar(correct, total)
    print(f"  Avg Time: {avg_time:.1f}s per question")

    # Grade
    pct = (correct / total * 100) if total else 0
    if pct == 100:
        grade = "🏆 Perfect Score!"
    elif pct >= 80:
        grade = "🥇 Excellent!"
    elif pct >= 60:
        grade = "🥈 Good Job!"
    elif pct >= 40:
        grade = "🥉 Keep Practicing!"
    else:
        grade = "📚 Study More!"
    print(f"\n  {grade}")
    print("=" * 55)

    return {"name": name, "score": score, "correct": correct, "total": total, "category": category}


def load_leaderboard(filename="leaderboard.json"):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_leaderboard(board, filename="leaderboard.json"):
    with open(filename, "w") as f:
        json.dump(board, f, indent=2)


def show_leaderboard(board):
    if not board:
        print("\n  No scores yet. Be the first!\n")
        return

    sorted_board = sorted(board, key=lambda x: x["score"], reverse=True)
    print("\n" + "=" * 55)
    print("  🏅  LEADERBOARD  (Top 10)")
    print("=" * 55)
    print(f"  {'Rank':<5} {'Name':<15} {'Score':<8} {'Correct':<10} {'Category'}")
    print("  " + "─" * 50)
    for i, entry in enumerate(sorted_board[:10], 1):
        medal = ["🥇", "🥈", "🥉"][i - 1] if i <= 3 else f"  {i}."
        print(f"  {medal:<5} {entry['name']:<15} {entry['score']:<8} "
              f"{entry['correct']}/{entry['total']:<8} {entry['category']}")
    print("=" * 55)


# ─────────────────────────────────────────────
#  MAIN MENU & GAME LOOP
# ─────────────────────────────────────────────

def choose_option(prompt, options):
    """Generic menu chooser."""
    while True:
        choice = input(prompt).strip()
        if choice in options:
            return choice
        print(f"  ⚠️  Please choose from: {', '.join(options)}")


def main():
    banner()
    print("\n  Welcome to the Python Quiz Game!\n")

    leaderboard = load_leaderboard()

    while True:
        print("\n  MAIN MENU")
        print("  ─────────────────────")
        print("  1. Start Quiz")
        print("  2. View Leaderboard")
        print("  3. Quit")
        choice = choose_option("\n  Enter choice (1/2/3): ", ["1", "2", "3"])

        if choice == "3":
            print("\n  👋 Thanks for playing! Goodbye!\n")
            break

        elif choice == "2":
            show_leaderboard(leaderboard)

        elif choice == "1":
            # Get player name
            name = input("\n  Enter your name: ").strip() or "Player"

            # Choose category
            categories = list(QUESTIONS.keys()) + ["Mixed (All Categories)"]
            print("\n  Choose a category:")
            for i, cat in enumerate(categories, 1):
                print(f"    {i}. {cat}")
            cat_choice = choose_option(
                f"\n  Enter number (1-{len(categories)}): ",
                [str(i) for i in range(1, len(categories) + 1)]
            )
            cat_index = int(cat_choice) - 1

            if cat_index == len(categories) - 1:
                category = "Mixed"
                all_q = [q for qs in QUESTIONS.values() for q in qs]
            else:
                category = categories[cat_index]
                all_q = QUESTIONS[category]

            # Choose number of questions
            max_q = len(all_q)
            print(f"\n  Available questions: {max_q}")
            while True:
                try:
                    n = int(input(f"  How many questions? (1-{max_q}): "))
                    if 1 <= n <= max_q:
                        break
                    print(f"  ⚠️  Enter a number between 1 and {max_q}.")
                except ValueError:
                    print("  ⚠️  Please enter a valid number.")

            # Timed mode?
            timed_input = choose_option("  Enable timed mode? (y/n): ", ["y", "n", "Y", "N"]).lower()
            timed = timed_input == "y"
            time_limit = 15
            if timed:
                print(f"  ⏱️  Each question: {time_limit} seconds. Fast answers earn a bonus point!")

            # Difficulty shuffle
            selected_q = random.sample(all_q, n)

            print(f"\n  Quiz: {category} | Questions: {n} | Timed: {'Yes' if timed else 'No'}")
            countdown(3)

            # Run quiz
            score, results = run_quiz(selected_q, timed=timed, time_limit=time_limit)

            # Show results
            entry = show_results(name, score, results, category)

            # Save to leaderboard
            leaderboard.append(entry)
            save_leaderboard(leaderboard)
            print("\n  ✅ Score saved to leaderboard!")

            # Play again?
            again = choose_option("\n  Play again? (y/n): ", ["y", "n", "Y", "N"]).lower()
            if again != "y":
                print("\n  👋 Thanks for playing!\n")
                break


# ─────────────────────────────────────────────
if __name__ == "__main__":
    main()
