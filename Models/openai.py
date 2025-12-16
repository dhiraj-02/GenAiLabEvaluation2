import os
from openai import OpenAI
import time

# Load OpenAI API key
openai_api_key = os.getenv("openai_api_key")
if openai_api_key is None:
    raise ValueError("openap_api_key environment variable not set.")

openai_version = os.getenv("openai_version")
if openai_version is None:
    raise ValueError("openai_version environment variable not set.")

# Initialize client
client = OpenAI(api_key=openai_api_key)

def generate(prompt):
    response = client.chat.completions.create(
        model=-openai_version,
        messages=[
            {"role": "system", "content": prompt["system"]},
            {"role": "user", "content": prompt["content"]}
        ],
        temperature=0.0  # deterministic output
    )
    
    time.sleep(2)
    
    try:
        with open("log.txt", "a") as log:
            log.write("\n\n====================================== NEW CALL ======================================\n")
            log.write("INPUT:\n")
            log.write(str(prompt["system"]) + "\n")
            log.write(str(prompt["content"]) + "\n")
            log.write("OUTPUT:\n")
            log.write("DEBUG RESPONSE OBJECT:\n" + str(response) + "\n\n")
            log.write(str(response.text) + "\n")
    except Exception as e:
        print("Logging failed:", e)
    
    return response.choices[0].message.content
