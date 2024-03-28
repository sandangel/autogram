"""Define LLMs."""

import os

import dspy

# Add export GENAI_API_KEY="api_key" before this script
# You can generate one API key at Google AI studio: https://makersuite.google.com/
gemini = dspy.Google(api_key=os.getenv("GENAI_API_KEY"), max_output_tokens=32000)
# The key max_tokens is expected but was not mapped to max_output_tokens
# gemini.kwargs["max_tokens"] = None

dolphincoder = dspy.OllamaLocal(model="dolphincoder:15b-starcoder2-q4_0", model_type="chat", temperature=0.7)
