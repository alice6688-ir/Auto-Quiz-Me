import openai
import PyPDF2
import docx

openai.api_key = "YOUR_OPENAI_API_KEY"

def extract_text_from_file(file):
    if file.name.endswith('.pdf'):
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    elif file.name.endswith('.docx'):
        doc = docx.Document(file)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
    elif file.name.endswith('.txt'):
        text = str(file.read(), "utf-8")
    else:
        text = ""
    return text

def generate_quiz_questions(text):
    prompt = f"""
    Based on the following notes, create 5 multiple choice questions. 
    For each question, provide 4 choices labeled A, B, C, D. 
    Also, mark the correct answer.

    Notes:
    {text}

    Return your answer as JSON in this format:
    [
      {{
        "question": "What is X?",
        "choices": ["A", "B", "C", "D"],
        "answer": "B"
      }},
      ...
    ]
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    try:
        output = response["choices"][0]["message"]["content"]
        questions = eval(output)  # Quick and dirty parsing (only because you control prompt)
        return questions
    except Exception as e:
        print("Error parsing AI response:", e)
        return []
