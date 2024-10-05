from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")
DATA_PATH= os.getenv("DATA_PATH")

def get_openai_api_key():
    return OPENAI_API_KEY



