import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    # Llama 3.3 70B is powerful and fast on Groq
    MODEL_NAME = "llama-3.3-70b-versatile" 
    
    if not GROQ_API_KEY:
        print("Warning: No GROQ_API_KEY found in env")