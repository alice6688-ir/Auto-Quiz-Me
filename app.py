import streamlit as st
from utils import generate_quiz_questions, extract_text_from_file

st.set_page_config(page_title="QuizWhiz", page_icon="⚡")

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

        st.session_state["questions"] = questions
        st.session_state["current_question"] = 0
        st.session_state["score"] = 0

if "questions" in st.session_state:
    questions = st.session_state["questions"]
    q_num = st.session_state["current_question"]

    if q_num < len(questions):
        q = questions[q_num]
        st.subheader(f"Question {q_num + 1}")
        user_answer = st.radio(q["question"], q["choices"])

        if st.button("Submit Answer"):
            if user_answer == q["answer"]:
                st.success("Correct! ✅")
                st.session_state["score"] += 1
            else:
                st.error(f"Wrong! Correct answer: {q['answer']}")

            st.session_state["current_question"] += 1
            st.experimental_rerun()

    else:
        st.success(f"Quiz Complete! 🎉 You scored {st.session_state['score']} out of {len(questions)}")
        st.balloons()
