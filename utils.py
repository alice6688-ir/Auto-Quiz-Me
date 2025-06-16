import openai
import json
import tiktoken
import PyPDF2
import docx
from openai import OpenAI

client = OpenAI(
    api_key=""
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


def generate_quiz_questions(text, difficulty="Medium"):
    if not text.strip():
        print("No text provided.")
        return []

    # Difficulty-specific instructions
    difficulty_instructions = {
        "Easy": """
        Generate EASY questions that test basic recall and understanding:
        - Focus on simple facts, definitions, and direct information from the text
        - Use straightforward "what is", "who did", "when did" questions
        - Make answer choices clearly different from each other
        - Avoid complex reasoning or analysis
        - Test memory and basic comprehension
        """,

        "Medium": """
        Generate MEDIUM difficulty questions that require application and analysis:
        - Ask questions that require understanding concepts and relationships
        - Include "why", "how", and "what would happen if" questions
        - Test ability to compare, contrast, and explain concepts
        - Make answer choices somewhat similar but with clear distinctions
        - Require connecting ideas from different parts of the text
        """,

        "Hard": """
        Generate HARD questions that demand critical thinking and synthesis:
        - Create complex scenario-based questions requiring deep analysis
        - Ask questions that require evaluating, synthesizing, and making inferences
        - Include questions about implications, consequences, and applications
        - Make answer choices very similar with subtle but important differences
        - Test ability to connect concepts across multiple topics
        - Require higher-order thinking skills
        """
    }

    difficulty_instruction = difficulty_instructions.get(difficulty, difficulty_instructions["Medium"])

    prompt = f"""
    You are a quiz generator creating {difficulty.upper()} difficulty questions.
    
    {difficulty_instruction}
    
    Based on the following notes, generate 10 multiple choice questions appropriate for {difficulty} difficulty level.
    For each question, provide 4 choices labeled A, B, C, D. 
    
    IMPORTANT: The "answer" field must contain ONLY a single letter (A, B, C, or D), not the full text of the answer.

    Notes:
    {text}

    Respond ONLY with valid JSON in this EXACT format:
    
    [
      {{
        "question": "What is photosynthesis?",
        "choices": ["The process of making food from sunlight", "The process of breathing", "The process of reproduction", "The process of growth"],
        "answer": "A"
      }},
      {{
        "question": "Where does photosynthesis occur?",
        "choices": ["In the roots", "In the chloroplasts", "In the stem", "In the flowers"],
        "answer": "B"
      }}
    ]
    
    Remember: answer field must be A, B, C, or D only!
    """

    messages = [
        {"role": "system", "content": f"You are a helpful quiz question generator specializing in {difficulty.lower()} difficulty questions."},
        {"role": "user", "content": prompt}
    ]

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            max_tokens=1500,  # Increased for more complex questions
            temperature=0.7,
        )

        output = response.choices[0].message.content.strip()

        if "```json" in output:
            output = output.split("```json")[-1].split("```")[0].strip()
        elif "```" in output:
            output = output.split("```")[-1].strip()

        # Debug raw output
        print(f"AI Response for {difficulty} difficulty: \n")

        # Try parsing the output
        questions = json.loads(output)

        # Calculate token usage
        input_tokens = sum([count_tokens(m['content']) for m in messages])
        output_tokens = count_tokens(output)
        total_tokens = input_tokens + output_tokens

        print(f"Used {input_tokens} input tokens, {output_tokens} output tokens, {total_tokens} total tokens.")

        cost_per_1k_tokens = 0.002  # GPT-3.5-turbo cost per 1000 tokens
        estimated_cost = (total_tokens / 1000) * cost_per_1k_tokens
        print(f"Estimated cost for this request: ${estimated_cost:.6f}")

        return questions

    except json.JSONDecodeError as e:
        print("Failed to parse JSON.", e)
        return []
    except Exception as e:
        print("Other error:", e)
        return []
