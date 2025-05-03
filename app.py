import streamlit as st
from utils import extract_text_from_file, generate_quiz_questions

st.set_page_config(page_title="QuizWhiz", page_icon="⚡", initial_sidebar_state="expanded")

if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False  # Default is light mode


def toggle_theme():
    st.session_state.dark_mode = not st.session_state.dark_mode

st.sidebar.button("Toggle Dark/Light Mode", on_click=toggle_theme)

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


st.title("⚡ QuizWhiz")
st.subheader("Turn your notes into quizzes instantly!")

uploaded_file = st.file_uploader("Upload your notes (PDF, TXT, DOCX)", type=["pdf", "txt", "docx"])
pasted_text = st.text_area("Or paste your notes here:")

if st.button("Generate Quiz"):
    with st.spinner('Creating your quiz...'):
        if uploaded_file:
            text = extract_text_from_file(uploaded_file)
        elif pasted_text:
            text = pasted_text
        else:
            st.error("Please upload a file or paste text!")
            st.stop()

        questions = generate_quiz_questions(text)
        print(questions)
        if questions:
            st.session_state["questions"] = questions
            st.session_state["current_question"] = 0
            st.session_state["score"] = 0
        else:
            st.error("Failed to generate quiz questions.")

# -----------------------------
# QUIZ DISPLAY WITH ANIMATION
# -----------------------------

if "questions" in st.session_state:
    questions = st.session_state["questions"]
    q_num = st.session_state.get("current_question", 0)

    if q_num < len(questions):
        q = questions[q_num]
        st.subheader(f"Question {q_num + 1} of {len(questions)}")

        # Create a unique key for the radio button
        user_answer = st.radio(
            q["question"],
            q["choices"],
            key=f"question_{q_num}"
        )

        if st.button("Submit Answer", key=f"submit_{q_num}"):
            correct_answer = q["answer"]

            # Score update
            if user_answer == correct_answer:
                st.session_state["score"] += 1
                st.success("Correct! ✅")
            else:
                st.error(f"Wrong! Correct answer: {correct_answer}")

            st.session_state["current_question"] += 1
            st.rerun()  # Re-run app to load next question

    else:
        st.success(f"Quiz Complete! 🎉 You scored {st.session_state['score']} out of {len(questions)}")
        st.balloons()
