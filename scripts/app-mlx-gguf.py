import argparse
import time

import models

from scripts.prompts import get_system_prompt

try:
    import mlx.core as mx
    import pyperclip
except ImportError:
    import os
    import site

    # Automator environment does not have site-packages installed by pdm. We need to add it manually.
    site.addsitedir(os.getenv("PYTHONPATH") or "")
    import mlx.core as mx
    import pyperclip


def generate(
    model: models.Model,
    tokenizer: models.GGUFTokenizer,
    prompt: str,
    max_tokens: int,
    temp: float,
) -> str | None:
    encoded_prompt = tokenizer.encode(prompt)

    tic = time.time()
    tokens = []
    for token, n in zip(
        models.generate(encoded_prompt, model, temp),
        range(max_tokens), strict=False,
    ):
        if token == tokenizer.eos_token_id:
            break

        if n == 0:
            prompt_time = time.time() - tic
            tic = time.time()

        tokens.append(token.item())
    response = tokenizer.decode(tokens)
    print(response, flush=True)
    gen_time = time.time() - tic
    print("=" * 10)
    if len(tokens) == 0:
        print("No tokens generated for this prompt")
        return None
    prompt_tps = encoded_prompt.size / prompt_time
    gen_tps = (len(tokens) - 1) / gen_time
    print(f"Prompt: {prompt_tps:.3f} tokens-per-sec")
    print(f"Generation: {gen_tps:.3f} tokens-per-sec")

    return response


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Inference script")
    parser.add_argument(
        "--gguf",
        type=str,
        help="The GGUF file to load (and optionally download).",
        default="neuralbeagle14-7b.Q4_0.gguf",
    )
    parser.add_argument(
        "--repo",
        type=str,
        default="mlabonne/NeuralBeagle14-7B-GGUF",
        help="The Hugging Face repo if downloading from the Hub.",
    )

    parser.add_argument(
        "--prompt",
        help="The message to be processed by the model",
    )
    parser.add_argument(
        "--max-tokens",
        "-m",
        type=int,
        default=8192,
        help="Maximum number of tokens to generate",
    )
    parser.add_argument(
        "--temp",
        help="The sampling temperature.",
        type=float,
        default=0.7,
    )
    parser.add_argument("--seed", type=int, default=0, help="The PRNG seed")

    args = parser.parse_args()
    mx.random.seed(args.seed)
    model, tokenizer = models.load(args.gguf, args.repo)

    # TODO (San): Auto detect chat template from gguf model.
    prompt = f"""<s>system\n{get_system_prompt(args.prompt)}</s>"""

    response = generate(model, tokenizer, prompt, args.max_tokens, args.temp)
    if response is not None:
        pyperclip.copy(response)
        print(response)
