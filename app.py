import streamlit as st
from utils import extract_text_from_file, generate_quiz_questions

# Initialize session state
if "questions" not in st.session_state:
    st.session_state["questions"] = []
if "current_question" not in st.session_state:
    st.session_state["current_question"] = 0
if "score" not in st.session_state:
    st.session_state["score"] = 0
if "wrong_answers" not in st.session_state:
    st.session_state["wrong_answers"] = []
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
if 'difficulty' not in st.session_state:
    st.session_state.difficulty = "Medium"

st.set_page_config(page_title="AliceQuizWhiz", page_icon="⚡", initial_sidebar_state="expanded")

def toggle_theme():
    st.session_state.dark_mode = not st.session_state.dark_mode

st.sidebar.button("Toggle Dark/Light Mode", on_click=toggle_theme)

# Theme styling
if st.session_state.dark_mode:
    st.markdown(
        """
        <style>
        body {
            background-color: #121212;
            color: white;
        }
        .sidebar .sidebar-content {
            background-color: #333;
        }
        .stButton > button {
            background-color: #444;
            color: white;
        }
        </style>
        """, unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <style>
        body {
            background-color: white;
            color: black;
        }
        .sidebar .sidebar-content {
            background-color: #f5f5f5;
        }
        .stButton > button {
            background-color: #f0f0f0;
            color: black;
        }
        </style>
        """, unsafe_allow_html=True
    )

st.title("⚡ AliceQuizWhiz")
st.subheader("Turn your notes into quizzes instantly!")

# Difficulty selection
col1, col2 = st.columns([2, 1])
with col1:
    uploaded_file = st.file_uploader("Upload your notes (PDF, TXT, DOCX)", type=["pdf", "txt", "docx"])
    pasted_text = st.text_area("Or paste your notes here:")

with col2:
    st.markdown("### 🎯 Difficulty Level")
    difficulty = st.selectbox(
        "Choose difficulty:",
        ["Easy", "Medium", "Hard"],
        index=1,  # Default to Medium
        help="Easy: Basic recall questions\nMedium: Application and analysis\nHard: Complex reasoning and evaluation"
    )
    st.session_state.difficulty = difficulty

    # Difficulty indicators
    if difficulty == "Easy":
        st.success("🟢 Easy: Simple recall questions")
    elif difficulty == "Medium":
        st.warning("🟡 Medium: Application & analysis")
    else:
        st.error("🔴 Hard: Complex reasoning")

if st.button("Generate Quiz"):
    with st.spinner('Creating your quiz...'):
        # Get text content
        if uploaded_file:
            text = extract_text_from_file(uploaded_file)
        elif pasted_text:
            text = pasted_text
        else:
            st.error("Please upload a file or paste text!")
            st.stop()

        # Generate questions with difficulty level
        questions = generate_quiz_questions(text, difficulty=st.session_state.difficulty)

        # Handle the response
        if questions and len(questions) > 0:
            st.session_state["questions"] = questions
            st.session_state["current_question"] = 0
            st.session_state["score"] = 0
            st.session_state["wrong_answers"] = []
            st.success(f"Generated {len(questions)} {st.session_state.difficulty.lower()} difficulty questions! Start your quiz below.")
        else:
            st.error("Failed to generate quiz questions. Please check your text content.")
            st.stop()

# Display quiz questions
if st.session_state["questions"]:
    questions = st.session_state["questions"]
    q_num = st.session_state["current_question"]

    if q_num < len(questions):
        # Display current question
        q = questions[q_num]

        st.markdown("---")
        difficulty_icon = {"Easy": "🟢", "Medium": "🟡", "Hard": "🔴"}
        st.subheader(f"Question {q_num + 1} of {len(questions)} {difficulty_icon.get(st.session_state.difficulty, '⚫')} {st.session_state.difficulty}")
        st.markdown(f"**{q['question']}**")

        # Display answer choices
        user_answer = st.radio(
            "Choose your answer:",
            q["choices"],
            key=f"question_{q_num}"
        )

        if st.button("Submit Answer", key=f"submit_{q_num}"):
            # Get correct answer
            correct_choice = q["choices"][ord(q["answer"]) - ord("A")]

            if user_answer == correct_choice:
                st.success("Correct! ✅")
                st.session_state["score"] += 1
            else:
                st.error(f"Incorrect. The correct answer is: {correct_choice}")
                st.session_state["wrong_answers"].append({
                    "question": q["question"],
                    "correct": correct_choice,
                    "your_answer": user_answer,
                })

            # Move to next question
            st.session_state["current_question"] += 1
            st.rerun()

    else:
        # Quiz completed
        st.markdown("---")
        difficulty_icon = {"Easy": "🟢", "Medium": "🟡", "Hard": "🔴"}
        st.success(f"🎉 Quiz Complete! You scored {st.session_state['score']} out of {len(questions)} on {difficulty_icon.get(st.session_state.difficulty, '⚫')} {st.session_state.difficulty} difficulty!")
        st.balloons()

        # Show percentage with difficulty-based feedback
        percentage = (st.session_state['score'] / len(questions)) * 100
        st.metric("Your Score", f"{percentage:.1f}%")

        # Difficulty-based feedback
        if st.session_state.difficulty == "Easy":
            if percentage >= 80:
                st.success("🌟 Excellent! Ready to try Medium difficulty?")
            elif percentage >= 60:
                st.info("👍 Good job! Practice a bit more or try Medium difficulty.")
            else:
                st.warning("📚 Keep studying! Review the material and try again.")
        elif st.session_state.difficulty == "Medium":
            if percentage >= 70:
                st.success("🔥 Outstanding! Ready for Hard difficulty?")
            elif percentage >= 50:
                st.info("💪 Well done! You're getting the hang of it.")
            else:
                st.warning("📖 Good effort! Try Easy mode first or review the material.")
        else:  # Hard
            if percentage >= 60:
                st.success("🏆 Incredible! You've mastered this material!")
            elif percentage >= 40:
                st.info("🎯 Impressive! Hard questions are challenging.")
            else:
                st.warning("🤔 These are tough questions! Try Medium difficulty first.")

        # Review wrong answers
        if st.session_state["wrong_answers"]:
            st.subheader("📝 Review Incorrect Answers:")
            for i, item in enumerate(st.session_state["wrong_answers"], 1):
                with st.expander(f"Question {i}"):
                    st.markdown(f"**{item['question']}**")
                    st.write(f"❌ Your answer: {item['your_answer']}")
                    st.write(f"✅ Correct answer: {item['correct']}")

        # Restart option
        if st.button("🔄 Start Over"):
            for key in ["questions", "current_question", "score", "wrong_answers"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

# Debug info (remove in production)
if st.checkbox("Show Debug Info"):
    st.write("Session State:", st.session_state)

