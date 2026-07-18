import os
import json
import streamlit as st
from dotenv import load_dotenv
from models import SkillAssessment
from prompts import SYSTEM_INSTRUCTION, USER_PROMPT_TEMPLATE

# Load local .env file if it exists
load_dotenv()

def get_api_key():
    # 1. Try Streamlit Cloud secrets safely
    try:
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

    # 2. Try local .env / environment variable
    api_key = os.getenv("GEMINI_API_KEY")

    if api_key:
        return api_key

    return None

def analyze_submission(category: str, work_content: str, explanation_content: str) -> SkillAssessment:
    """
    Sends the work and explanation to the Gemini API using structured JSON output.
    Validates and parses the result into a SkillAssessment object.
    """
    api_key = get_api_key()
    if not api_key:
        raise ValueError("Gemini API key is not configured. Please add GEMINI_API_KEY to your .env file or Streamlit secrets.")

    # Try importing the new google-genai SDK
    try:
        from google import genai
        from google.genai import types
        use_modern_sdk = True
    except ImportError:
        use_modern_sdk = False

    prompt = USER_PROMPT_TEMPLATE.format(
        category=category,
        work_content=work_content,
        explanation_content=explanation_content
    )

    if use_modern_sdk:
        try:
            # Initialize Client with specific API key
            client = genai.Client(api_key=api_key)
            
            response = client.models.generate_content(
                model='gemini-flash-latest',
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    response_mime_type="application/json",
                    response_schema=SkillAssessment,
                    temperature=0.2,
                ),
            )
            
            response_text = response.text
            # Parse the response text and validate via Pydantic
            data = json.loads(response_text)
            return SkillAssessment.model_validate(data)
            
        except Exception as e:
            # If modern SDK fails or experiences model access issues, try fallback to legacy or raise error
            raise RuntimeError(f"Error communicating with Gemini via modern SDK: {e}")
            
    else:
        # Fallback to google-generativeai (legacy SDK) if modern is not installed
        try:
            import google.generativeai as legacy_genai
            from google.generativeai.types import RequestOptions
            
            legacy_genai.configure(api_key=api_key)
            
            # Setup generation configuration for JSON output
            generation_config = {
                "temperature": 0.2,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 8192,
                "response_mime_type": "application/json",
            }
            
            # Formulate full text prompt including system instruction since system_instruction param format varies
            full_prompt = f"{SYSTEM_INSTRUCTION}\n\n{prompt}"
            
            model = legacy_genai.GenerativeModel(
                model_name="gemini-flash-latest",
                generation_config=generation_config
            )
            
            response = model.generate_content(full_prompt)
            response_text = response.text
            
            # Clean up text if LLM wrapped in markdown code blocks
            if response_text.startswith("```json"):
                response_text = response_text.replace("```json", "", 1)
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            data = json.loads(response_text)
            return SkillAssessment.model_validate(data)
            
        except ImportError:
            # If both fail, raise instruction to install dependencies
            raise ImportError(
                "Neither 'google-genai' nor 'google-generativeai' libraries could be imported. "
                "Please run: pip install google-genai"
            )
        except Exception as e:
            raise RuntimeError(f"Error communicating with Gemini via legacy SDK: {e}")
