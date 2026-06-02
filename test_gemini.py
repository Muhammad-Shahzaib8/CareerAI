from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

print("Key loaded:", api_key[:6] if api_key else None)

client = genai.Client(
    api_key=api_key
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Say hello"
)

print(response.text)