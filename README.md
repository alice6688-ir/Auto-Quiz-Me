# Project Brief: Auto-Quiz-Me

Overview:
Auto-Quiz Me is an AI-powered tool for teachers or students that instantly turns their notes, textbooks, or lecture slides into practice quizzes.
The goal is to make active studying effortless, improve recall, and save students/teachers massive time preparing for exams.


Problem:
1. Passive reading → poor retention
2. Creating practice questions manually is tedious and time-consuming
3. Potential gap in the market


Solution:
Upload or paste your notes → AI reads and understands → Instantly generates practice quizzes.


Key features:
1. Upload file (PDF, DOCX, TXT) or paste text
2. AI generates multiple-choice, fill-in-the-blank, and short-answer questions
3. Difficulty levels (Easy / Medium / Hard)
4. Option to save quizzes and retake them later


MVP Scope:

  Must Have:
    1. File upload + text paste interface
    2. AI generates at least 10 questions per document
    Quiz UI:
      1. Question view
      2. Answer selection
      3. Feedback (potentially essay-based questions too)
  Stretch Goals:
      1. Difficulty level selector
      2. Review wrong answers at the end
      3. "Quiz Me Again" option for quick reattempts
      4. Progress tracking (Improved x% over last session and other statistics)


User Flow (Basic):
1. Landing Page: short intro + "Upload Your Notes" button
2. Upload/Paste Notes: simple, clean upload screen
3. Quiz Generation: loading animation ("Creating your quiz...")
4. Quiz Page:
      1. Questions one by one
      2. Pick answer → instant feedback
5. Quiz End Screen:
      1. Score summary
      2. Progress tracking (if applicable)
      3. Option to retake or try a harder quiz


Tech Stack Suggestion:
Frontend: React.js (smooth, fast UI)

Backend: Node.js + Express or Firebase Functions (easy to scale)

AI API:
OpenAI GPT-4 (best quality questions)
OR use open-source models like LLaMA if you want cheaper/self-hosted later

Database (optional): Firebase / Supabase to save user quizzes


Success Metrics:
1. Students complete at least 80% of the quizzes they generate
2. Students feel the quizzes help them study better or teachers feel it saved them time and was efficient (measured via survey/feedback)
3. Time from upload to first question = under 15 seconds
