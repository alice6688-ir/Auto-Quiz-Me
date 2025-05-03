import openai
import json
import tiktoken
import PyPDF2
import docx
from openai import OpenAI
client = OpenAI(
    api_key="YOUR_OPENAI_KEY"
)

MODEL = "gpt-3.5-turbo"
encoding = tiktoken.encoding_for_model(MODEL)


def count_tokens(text):
    return len(encoding.encode(text))


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
    if not text.strip():
        print("No text extracted from file.")
        return[]

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

    messages = [
        {"role": "system", "content": "You are a helpful quiz question generator."},
        {"role": "user", "content": prompt}
        ]

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            max_tokens=100,
            temperature=0.7,
        )

        output = response.choices[0].message.content.strip()

        # Calculate token usage
        input_tokens = sum([count_tokens(m['content']) for m in messages])
        output_tokens = count_tokens(output)
        total_tokens = input_tokens + output_tokens

        print(f"Used {input_tokens} input tokens, {output_tokens} output tokens, {total_tokens} total tokens.")

        cost_per_1k_tokens = 0.002  # GPT-3.5-turbo cost per 1000 tokens
        estimated_cost = (total_tokens / 1000) * cost_per_1k_tokens
        print(f"Estimated cost for this request: ${estimated_cost:.6f}")

        questions = json.loads(output)  # Quick and dirty parsing (only because you control prompt)
        return questions

    except Exception as e:
        print(f"Error parsing AI response: {e}")
        return []
