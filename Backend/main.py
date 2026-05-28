# Run using:
# python -m uvicorn main:app --reload


import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY environment variable not set")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NotesRequest(BaseModel):
    topic: str
    level: str
    semester: str
    notes_type: str

@app.get("/")
def home():
    return {
        "message": "AI Notes Generator Backend Running"
    }

def build_prompt(data):
    base = f"""
You are an expert educational AI assistant.

Generate high-quality study material.

Topic: {data.topic}
Education Level: {data.level}
Class/Semester: {data.semester}

Requirements:
- Use clean markdown
- Use proper headings and subheadings
- Use bullet points where useful
- Include examples
- Include important points
- Make notes useful for exams and revision
"""

    # ───────────────── SHORT NOTES

    if data.notes_type == "Short (Quick Revision)":

        return base + """

Generate SHORT revision notes.

Include:
- Key definitions
- Important formulas
- Important concepts
- Quick summary
- Revision-friendly points

Keep the notes concise and easy to revise quickly.
"""

    # ───────────────── DETAILED NOTES

    elif data.notes_type == "Detailed (In-Depth)":

        return base + """

Generate DETAILED IN-DEPTH notes.

Include:
- Complete explanation of concepts
- Important subtopics
- Real-world examples
- Step-by-step explanations
- Tables where useful
- Advantages and disadvantages if relevant
- Important terminology
- Summary at the end

The notes should help a student deeply understand the topic.
"""

    # ───────────────── EXAM ORIENTED

    elif data.notes_type == "Exam-Oriented (Key Points + MCQs)":

        return base + """

Generate EXAM-ORIENTED study notes.

Include:
- Important theory
- Key exam points
- Frequently asked concepts
- Important definitions
- Memory tricks if useful

Also include:
- 5 MCQs with answers
- 5 short-answer questions with answers
- 3 long-answer questions

Highlight topics most likely to appear in exams.
"""

    # ───────────────── PRACTICE PROBLEMS

    elif data.notes_type == "Practice Problems & Solutions":

        return base + """

Generate PRACTICE PROBLEMS with SOLUTIONS.

Include:
- Easy problems
- Medium problems
- Hard problems

For each problem:
- Show the question
- Provide step-by-step solution
- Explain the reasoning clearly

If the topic is theoretical:
- Create conceptual questions
- Scenario-based questions
- Application-based questions

If the topic is numerical:
- Include calculations and formulas

The goal is active learning and practice.
"""

    # ───────────────── MIND MAP

    elif data.notes_type == "Mind Map":

        return base + """

Generate ONLY a TEXT-BASED VISUAL MIND MAP.

IMPORTANT RULES:
- DO NOT write paragraphs
- DO NOT write detailed notes
- DO NOT explain concepts normally
- DO NOT use markdown headings
- ONLY generate a tree-style structure
- Use Unicode tree characters

STRICT FORMAT:

TOPIC
├── Main Branch
│   ├── Sub Branch
│   ├── Sub Branch
│   └── Sub Branch
│
├── Main Branch
│   ├── Sub Branch
│   └── Sub Branch
│
└── Main Branch
    ├── Sub Branch
    └── Sub Branch

Keep the output concise, visual, and easy to memorize.
"""

    # ───────────────── DEFAULT

    return base



@app.post("/generate-notes")
def generate_notes(data: NotesRequest):
    prompt = build_prompt(data)
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "system",
                "content": "You are an expert teacher and professor."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    notes = response.choices[0].message.content

    return {
        "notes": notes
    }
    
