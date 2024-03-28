# Get response from both Ollama and Gemini to compare the results and evaluate.
# TODO (San): Add evaluation and benchmark in the CI

import asyncio
import os
import sys

import cloudpickle as pk
import dspy
import pyperclip

from shortcutx.instrument import otel_instrument
from shortcutx.llm import dolphincoder, gemini
from shortcutx.program import RephraseTextProgram

input_string = sys.argv[1]


async def run_ollama() -> str:
    """Run Ollama."""
    try:
        with dspy.context(lm=dolphincoder):
            rephrase_text = RephraseTextProgram()
            response = rephrase_text(text=input_string)
            return response.rephrased_text.strip()
    except Exception as e:
        print(e)
        return ""


async def run_gemini_no_optimize() -> str:
    """Run Ollama."""
    try:
        with dspy.context(lm=gemini):
            rephrase_text = RephraseTextProgram()
            response = rephrase_text(text=input_string)
            return response.rephrased_text.strip()
    except Exception as e:
        print(e)
        return ""


async def run_gemini() -> str:
    """Run Gemini."""
    try:
        with dspy.context(lm=gemini):
            rephrase_text = pk.load(open(os.path.dirname(__file__) + "/compiled.pkl", "rb"))
            response = rephrase_text(text=input_string)

            return response.rephrased_text.strip()
    except Exception as e:
        print(e)
        return ""


async def main() -> None:
    """Main function."""
    otel_instrument()
    responses = await asyncio.gather(
        run_gemini(),
        run_gemini_no_optimize(),
        # TODO (San): Add Ollama back
        # run_ollama(),
    )

    response = "{}\n------\n{}".format(*responses) if len(responses) > 1 else responses[0]

    pyperclip.copy(response)
    print(response)


def cli() -> None:
    """Run the CLI."""
    asyncio.run(main())
