# Get response from both Ollama and Gemini to compare the results and evaluate.
# TODO (San): Add evaluation and benchmark in the CI

import sys
import os
import asyncio

from prompts import get_system_prompt

try:
    import pyperclip

    import ollama
    import google.generativeai as genai
except ImportError:
    import site

    # Automator environment does not have site-packages installed by pdm. We need to add it manually.
    site.addsitedir(os.getenv("PYTHONPATH") or "")

    import pyperclip
    import ollama
    import google.generativeai as genai

# Add export GENAI_API_KEY="api_key" before this script
# You can generate one API key at Google AI studio: https://makersuite.google.com/
genai.configure(api_key=os.getenv("GENAI_API_KEY"))

model = genai.GenerativeModel("gemini-pro")


MODEL = "starling-lm:7b-alpha-q4_K_M"

input_string = sys.argv[1]
system_message = get_system_prompt(input_string)


async def run_ollama() -> str:
    try:
        response = ollama.generate(model=MODEL, prompt=system_message, keep_alive="1h")
        return response["response"].strip()
    except Exception as e:
        print(e)
        return ""


async def run_gemini() -> str:
    try:
        response = model.generate_content(system_message)
        return response.text.strip()
    except Exception as e:
        print(e)
        return ""


async def main():
    responses = await asyncio.gather(run_gemini(), run_ollama())

    response = "{}\n------\n{}".format(*responses)
    pyperclip.copy(response)
    print(response)


asyncio.run(main())
