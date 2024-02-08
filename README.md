# Autogram
<img src="assets/autogram.jpg" style="max-width: 400px;" />
Grammar checker for Apple Silicon devices powered by Automator with Ollama + Gemini or Apple MLX as backend.
Open, free, easy and fast!
Play, copy, fork, experiment, have fun!

The main tool will give answer from both Ollama and Gemini for comparison and choose which is the best for you.

Example rephrased text from the above message:

> The primary tool will provide responses from both Ollama and Gemini for comparison, enabling you to select the optimal option for your needs.

> ------

> The primary tool provides answers from both Ollama and Gemini for comparison, allowing you to determine the most suitable option.

## Setup

- Install [ollama](https://ollama.ai/)
- Install [pdm](https://pdm-project.org/latest/#installation). If you are using nix, just need to run `nix develop --impure .`, or `direnv allow` if you're using direnv + nix
- Install dependencies

```python
pdm install
```

- Gemini: You can generate one Bard API key at Google AI studio: https://makersuite.google.com/
- Ollama: Pull the model from ollama registry

```sh
ollama pull starling-lm:7b-alpha-q4_K_M
```

## Install workflow

Edit the workflow, adding your Gemini API KEY and site-packages path.

<img src="assets/step-1.png" width="500"/>

<img src="assets/step-2.png" width="500"/>

Then just double click to install the workflow.

Go to System Preferences -> Keyboard -> Shortcuts -> Services -> Text -> GrammarChecker, and set the shortcut, in my case I set it to `⌃⌥⌘S`.

## Usage

In any OSX application, select some text, and press the shortcut you set. The selected text will be replaced with the generated text from the model.

Please note that Ollama allow you to keep the model in memory for faster startup time. Currently it's set to 1 hour.

## Apple MLX Backend

Install `MLXGrammarChecker.workflow` the same way as above. Please note that this is the experimental. In theory MLX should be faster but because we need to load the weights into memory every time we call the workflow, it will take more time comparing to Gemini or Ollama.

This worfklow is based on Qwen/Qwen1.5-14B-Chat model.

## Roadmap

- Integrate with nvim
- Popup to pick and choose instead of printing both text from Ollama and Gemini

## Credits
Original idea [LLM-Automator](https://github.com/radames/LLM-automator) [Radamés Ajna](https://github.com/radames)
This is forked from [Autogram](https://github.com/ivanfioravanti/autogram) with some changes:

- Use pdm for Python package management
- Use bash script in Automator so you can modify Python code in the scripts/*.py files instead of modifying them in the Automator workflow
- Add support for Gemini
- Change the prompt which is improved by Gemini
- Experiment with MLX GGUF
