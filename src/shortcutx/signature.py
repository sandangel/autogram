"""Signature."""

import dspy


class RephraseText(dspy.Signature):
    """Rephrase text with enhanced clarity, wordings, correct spelling, grammar, and sounds professional."""

    text: str = dspy.InputField(description="The text to rephrase")
    rephrased_text: str = dspy.OutputField(description="The rephrased text")
