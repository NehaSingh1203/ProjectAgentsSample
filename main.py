# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from openai import OpenAI

# Load OpenAI key from env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)  # Automatically uses OPENAI_API_KEY from environment

app = FastAPI()

# Input schema
class TaskInput(BaseModel):
    user_input: str
    agent_type: str  # "extract" or "validate"

# Agent: Extract requirements
def extract_requirements(user_input: str) -> str:
    prompt = f"""Extract structured engineering requirements from the following text:\n\n{user_input}\n\nFormat:\n- [ID]: [Requirement]"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()

# Agent: Validate requirements
def validate_requirements(user_input: str) -> str:
    prompt = f"""Check the following engineering requirements for completeness, clarity, and testability:\n\n{user_input}\n\nReturn feedback on each."""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()

# API endpoint
@app.post("/run")
async def run_agent(task: TaskInput):
    if task.agent_type == "extract":
        result = extract_requirements(task.user_input)
    elif task.agent_type == "validate":
        result = validate_requirements(task.user_input)
    else:
        result = "Unknown agent type. Use 'extract' or 'validate'."
    
    return {"result": result}
