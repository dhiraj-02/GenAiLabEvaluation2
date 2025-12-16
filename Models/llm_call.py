import os
from dotenv import load_dotenv

load_dotenv()

import Models.gemini as gemini
import Models.openai as openai

model_chosen = os.getenv("chosen_model")
if model_chosen is None:
    raise ValueError("No model chosen")

def generate(prompt):

    if model_chosen == "gemini":
        return gemini.generate(prompt)
    elif model_chosen == "openai":
        return openai.generate(prompt)
    else:
        raise ValueError("Model chosen is not supported")
