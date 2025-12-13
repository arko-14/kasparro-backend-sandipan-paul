import os
import logging
from dotenv import load_dotenv

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    # Critical: Raise error if Env var is missing
    if not GROQ_API_KEY:
        raise ValueError("CRITICAL: GROQ_API_KEY is missing from environment variables.")
        
    # Model is configurable, no hardcoded fallback in logic
    MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")
