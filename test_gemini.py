
from langchain_google_genai import ChatGoogleGenerativeAI

from src.config import GOOGLE_API_KEY, MODEL_NAME

print("Connecting to Gemini...")

model = ChatGoogleGenerativeAI(
    model=MODEL_NAME,
    google_api_key=GOOGLE_API_KEY,
    temperature=0,
    max_retries=0,
)

response = model.invoke("Reply with only: Hello Bhavani!")

print("Gemini response:")
print(response.content)
