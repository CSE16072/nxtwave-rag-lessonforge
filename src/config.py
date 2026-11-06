
import os
from dotenv import load_dotenv

# Load values from the .env file
load_dotenv()

# Read the Gemini API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Model we will use for lesson generation
MODEL_NAME = "gemini-3.5-flash"


def check_config():
    if not GOOGLE_API_KEY or GOOGLE_API_KEY == "your_gemini_api_key_here":
        raise ValueError(
            "Google API key is missing. Please check your .env file."
        )

    print("Configuration loaded successfully!")
    print(f"Model selected: {MODEL_NAME}")


if __name__ == "__main__":
    check_config()
