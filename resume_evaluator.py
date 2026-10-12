import os
import json

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    try:
        import streamlit as st
        GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    except Exception:
        GOOGLE_API_KEY = None

if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY not found. Configure it in your "
        "local .env file or Streamlit Cloud Secrets."
    )

# Initialize Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0
)


def evaluate_resume(
    resume_context: str,
    job_description: str,
    resume_filename: str
) -> dict:
    """
    Evaluate a resume against a job description using
    evidence retrieved from the resume.
    """

    prompt = f"""
You are an AI-assisted resume screening system.

Your task is to compare the provided resume evidence
against the job description.

IMPORTANT RULES:
1. Use only the supplied resume evidence and job description.
2. Do not invent qualifications, skills, achievements,
   employment history, or education.
3. Distinguish between skills explicitly demonstrated
   and skills that are merely mentioned.
4. If evidence is unavailable, state "Not evidenced".
5. Do not use age, gender, race, religion, disability,
   marital status, nationality, or other protected
   characteristics when evaluating the candidate.
6. Evaluate only job-related qualifications.
7. The score is indicative decision support, not an
   objective measure of candidate quality.
8. Do not make an automatic hiring or rejection decision.
9. Return valid JSON only, without Markdown code fences.

JOB DESCRIPTION:
{job_description}

RESUME FILENAME:
{resume_filename}

RETRIEVED RESUME EVIDENCE:
{resume_context}

Return a JSON object with this exact structure:

{{
    "resume_filename": "{resume_filename}",
    "match_score": 0,
    "matching_skills": [],
    "missing_or_unverified_skills": [],
    "relevant_experience": [],
    "strengths": [],
    "gaps": [],
    "evidence": [],
    "recommendation": "Potential match",
    "recommendation_reason": "",
    "human_review_required": true
}}

Scoring guidance:
- Assess how well the available evidence meets
  the job-related requirements.
- Consider relevant skills, demonstrated experience,
  and evidence of applying required methods.
- Do not award points for unsupported assumptions.
- Use a score between 0 and 100.
- Explain important evidence and gaps clearly.
- Use only these recommendation categories:
  "Strong match", "Potential match", "Limited match".

Return the JSON object now.
"""

    response = llm.invoke(prompt)
    response_text = response.content

    # Handle responses returned as content-block lists
    if isinstance(response_text, list):
        text_parts = []

        for block in response_text:
            if isinstance(block, dict) and "text" in block:
                text_parts.append(block["text"])
            elif isinstance(block, str):
                text_parts.append(block)

        response_text = "\n".join(text_parts)

    response_text = response_text.strip()

    # Remove Markdown fences if the model adds them
    if response_text.startswith("```"):
        response_text = response_text.split("\n", 1)[1]
        response_text = response_text.rsplit("```", 1)[0]

    result = json.loads(response_text)

    # Basic validation
    score = result.get("match_score")

    if not isinstance(score, (int, float)) or not 0 <= score <= 100:
        raise ValueError("The model returned an invalid match score.")

    result["resume_filename"] = resume_filename
    result["human_review_required"] = True

    return result