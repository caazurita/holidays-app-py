from google import genai
import os
import json
import re
from dotenv import load_dotenv

from app.schemas.summary_schema import Summary
load_dotenv()

class AgentService:
    def __init__(self):
        API_KEY = os.getenv("GOOGLE_API_KEY")
        self.client = genai.Client(api_key=API_KEY)
        

    def extract_json(text: str):
        cleaned = text.replace("```json", "").replace("```", "").strip()
        try:
         return json.loads(cleaned)
        except json.JSONDecodeError:
            match = re.search(r"\[.*\]", cleaned, re.DOTALL)
            if match:
                return json.loads(match.group(0))
            else:
                return None
    
    async def run(self, names: list[str]):
        try:
            prompt = f""" 
                You will receive a list of holidays.
                For each holiday:
                - Summarize it in 2 sentences.
                - Classify it as: national, cultural, or religious.

                Return the result as a JSON array with this format:
                [
                    {{
                        "name": "holiday name",
                        "summary": "short summary",
                        "category": "national | cultural | religious"
                    }}
                ]

                Holidays: {", ".join(names)}
            """
            response = self.client.models.generate_content(
                model="gemini-3-flash-preview", contents=prompt
            )
            map =  AgentService.extract_json(response.text)
            return [Summary(**item) for item in map]
        except Exception as e:
            print('error running agent:', e)
            return e
