from google import genai
import os
Gemini_KEY = os.getenv("GEMINI_API_KEY", os.getenv("test", ""))
client = None
if Gemini_KEY:
    client = genai.Client(api_key=Gemini_KEY)
def ask_ai(prompt):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text
