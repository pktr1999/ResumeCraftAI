import os
from dotenv import load_dotenv
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage


load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="models/gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0
)

def extract_resume_info(resume_text):
    prompt = f"""
You are given resume text.
Convert the content into JSON that exactly follows the structure below:

{{
  "first_name": "",
  "last_name": "",
  "job_title": "",
  "contact": {{
    "location": "",
    "linkedin": ""
  }},
  "career_summary": "",
  "expertise": [],
  "technical_skills": [],
  "professional_experience": [
    {{
      "title": "",
      "company": "",
      "location": "",
      "start_date": "",
      "end_date": "",
      "description": "",
      "achievements": []
    }}
  ],
  "education": [
    {{
      "degree": "",
      "field": "",
      "institution": "",
      "start_year": "",
      "end_year": ""
    }}
  ],
  "certifications": []
}}

Rules:
1. Extract names, job title, contact details, summary, skills, work history, education, and certifications exactly as they appear in the resume.
2. "expertise" = key skill domains from the summary or skill sections.
3. "technical_skills" = specific tools, technologies, and software mentioned.
4. For "professional_experience", each job must be a separate object.
5. "certifications" = list of certificates exactly as stated in the resume.
6. "education" = list of degrees with field, institution, and years.
7. Leave missing values as an empty string "".
8. Job title should have one tile most relevent one.
9. Return only valid JSON — no explanations.


Resume:
{resume_text}
"""
    
#     prompt = f"""
# You are given resume text.
# Convert the content into JSON exactly matching the schema below.

# Schema:
# {{
#   "full_name": "",
#   "job_title": "",
#   "contact": {{
#     "phone": "",
#     "email": "",
#     "location": "",
#     "linkedin": ""
#   }},
#   "summary": "",  # 3–5 line professional summary combining career achievements, expertise, and industry experience
#   "expertise": [],  # key skill domains (e.g., Project Management, Data Analysis)
#   "technical_skills": [],  # specific tools/technologies
#   "professional_experience": [
#     {{
#       "company_and_title": "",  # e.g., "Software Engineer – ABC Corp"
#       "duration": "",  # e.g., "Jan 2020 – Present"
#       "highlights": []  # 2–5 bullet points summarizing responsibilities and key achievements
#     }}
#   ],
#   "education": [
#     {{
#       "degree_and_field": "",  # e.g., "B.Tech in Computer Science"
#       "institution": "",
#       "years": ""  # e.g., "2015 – 2019"
#     }}
#   ],
#   "certifications": []
# }}

# Rules:
# 1. "summary" must be concise (max 4 sentences) and directly resume-ready.
# 2. "professional_experience" entries should be condensed for readability in a resume — use bullet highlights, not full paragraphs.
# 3. Keep wording exactly as in the resume where possible; rephrase only to improve brevity/clarity.
# 4. "expertise" and "technical_skills" should be separate lists (general skills vs. specific tools).
# 5. Leave missing values as an empty string "".
# 6. Return only valid JSON — no extra text or explanations.

# Resume:
# {resume_text}
# """
    
    response = llm.invoke([HumanMessage(content=prompt)])
    raw = response.content.strip()

    # Remove markdown formatting if present
    if raw.startswith("```json"):
        raw = raw.replace("```json", "").replace("```", "").strip()
    
    print("Returning json data from llm")

    return raw