from openai import OpenAI
import os

# Railway already provides ENV variables
api_key = os.environ.get("OPENAI_API_KEY")

if api_key is None:
    print("DEBUG ENV:", dict(os.environ))
    raise ValueError("OPENAI_API_KEY not found in environment!")

client = OpenAI(api_key=api_key)