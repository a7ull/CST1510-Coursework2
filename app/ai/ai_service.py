from google import genai
client = genai.Client(api_key="api_key")
def ask_ai(prompt):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text
