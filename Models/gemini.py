import os
from dotenv import load_dotenv

load_dotenv()

from google import genai
from google.genai import types
import time


gemini_api_key = os.getenv("gemini_api_key")
if gemini_api_key is None:
    raise ValueError("gemini_api_key environment variable not set.")

gemini_version = os.getenv("gemini_version")
if gemini_version is None:
    raise ValueError("gemini_version environment variable not set.")


client = genai.Client(api_key=gemini_api_key)


def generate(prompt):

    response = client.models.generate_content(
        model=gemini_version,
        config=types.GenerateContentConfig(
            system_instruction=prompt["system"],
            temperature=0.0   # deterministic output
        ),
        contents=prompt["content"]
    )

    time.sleep(2)

    try:
        with open("log.txt", "a") as log:
            log.write("\n================= NEW CALL =================\n")
            log.write(f"INPUT SYSTEM   : {prompt['system']}\n")
            log.write(f"INPUT CONTENT  : {prompt['content']}\n")
            log.write(f"OUTPUT RAW     : {str(response)}\n")
            log.write(f"OUTPUT TEXT    : {response.text}\n")
            log.write("============================================\n")
    except Exception as e:
        print("Logging failed:", e)


    return response.text


