from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///./data/logs.db"
    )

settings = Settings()
