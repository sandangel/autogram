import sys

from prompts import get_system_prompt

try:
    import pyperclip
    from mlx_lm import generate, load
except ImportError:
    import os
    import site

    # Automator environment does not have site-packages installed by pdm. We need to add it manually.
    site.addsitedir(os.getenv("PYTHONPATH") or "")

    import pyperclip
    from mlx_lm import generate, load

model, tokenizer = load("Qwen/Qwen1.5-14B-Chat")

user_input = sys.argv[1]

system_prompt = get_system_prompt(user_input)

messages = [
    {"role": "system", "content": system_prompt},
]

# Will add generation prompt to the prompt.
# E.g: <|system|>, <|im_start|>assistant, <|im_end|> ... depending on the LLM and its chat template
prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

response = generate(model, tokenizer, prompt=prompt, temp=0.7)

# Plain response will contain eos token. We need to remove it.
# TODO (San): Investigate how to remove this automatically in the generate function.
response = response.replace(tokenizer.eos_token, "")

# It seems like an issue with company provided Mac or Automator, we need to both printing to stdout and copy to clipboard to make the response
# replace selected text
pyperclip.copy(response)
print(response)
