"""
🧠 QUIZ GAME
Test your knowledge with a multiple-choice quiz!
"""

import streamlit as st

st.set_page_config(page_title="🧠 Quiz Game", page_icon="🧠")
st.title("🧠 Quiz Game")
st.write("Answer the questions and see your score!")

questions = [
    {
        "question": "What does CPU stand for?",
        "options": ["Central Processing Unit", "Computer Personal Unit", "Central Power Unit", "Control Processing Utility"],
        "answer": "Central Processing Unit"
    },
    {
        "question": "Which language is used for web apps?",
        "options": ["Python", "JavaScript", "C++", "Java"],
        "answer": "JavaScript"
    },
    {
        "question": "What is the value of 2^5?",
        "options": ["10", "32", "25", "16"],
        "answer": "32"
    },
    {
        "question": "Who developed the theory of relativity?",
        "options": ["Isaac Newton", "Albert Einstein", "Marie Curie", "Nikola Tesla"],
        "answer": "Albert Einstein"
    },
]

score = 0
user_answers = []

for idx, q in enumerate(questions):
    st.subheader(f"Q{idx+1}: {q['question']}")
    user_answer = st.radio("Choose your answer:", q["options"], key=f"q{idx}")
    user_answers.append(user_answer)

if st.button("Submit Answers"):
    score = sum([user_answers[i] == questions[i]["answer"] for i in range(len(questions))])
    st.success(f"Your score: {score} / {len(questions)}")
    for i, q in enumerate(questions):
        if user_answers[i] == q["answer"]:
            st.write(f"Q{i+1}: Correct!")
        else:
            st.write(f"Q{i+1}: Incorrect. Correct answer: {q['answer']}")

st.markdown("---")
st.write("💡 **Learning Outcome:** Practice quiz logic, user input, and scoring in Python.")
