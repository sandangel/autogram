import dspy

from shortcutx.signature import RephraseText


class RephraseTextProgram(dspy.Module):
    def __init__(self) -> None:
        super().__init__()
        self.rephrase_text = dspy.ChainOfThought(RephraseText)

    def forward(self, text: str):
        return self.rephrase_text(text=text)
