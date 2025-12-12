from google import genai
client = genai.Client(api_key="AIzaSyDPfPQ3zmGk5ut-1BQ2gh1ALNK_6vt1l5c")
def ask_ai(prompt):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text
