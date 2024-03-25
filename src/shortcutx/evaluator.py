import sys

import dspy
import polars as pl
from dspy.evaluate import Evaluate
from pydantic import BaseModel, Field

from shortcutx.instrument import otel_instrument
from shortcutx.llm import dolphincoder, gemini
from shortcutx.program import RephraseTextProgram


class ScoreRephrasedText(dspy.Signature):
    class Input(BaseModel):
        original_text: str = Field(description="The original text from which to rephrase")
        example_rephrased_text: str = Field(description="The example rephrased text")
        assessment_rephrased_text: str = Field(description="The assessment rephrased text")

    class Output(BaseModel):
        wording_score: float = Field(
            ge=0,
            le=100,
            description="On a scale of 0 to 100, how effectively does the rephrased text improve the wording of the original compared to the example rephrased text? Consider factors like clarity, precision, and overall readability.",
        )
        meaning_score: float = Field(
            ge=0,
            le=100,
            description="On a scale of 0 to 100, rate how faithfully the assessment rephrased text captures the original text's meaning and intention compared to the example rephrased text.",
        )

    input: Input = dspy.InputField()
    output: Output = dspy.OutputField()


def metric(example: dspy.Example, pred: dspy.Prediction, trace=None) -> float:
    judge = dspy.TypedChainOfThought(ScoreRephrasedText)
    with dspy.context(lm=gemini):
        assessment = judge(
            input=ScoreRephrasedText.Input(
                original_text=example.text,
                example_rephrased_text=example.rephrased_text,
                assessment_rephrased_text=pred.rephrased_text,
            )
        )
    if trace is None:
        # Float metric is used for evaluation and optimization
        return (assessment.output.wording_score + assessment.output.meaning_score) / 200.0
    else:
        # Boolean metric is used for bootstrapping
        return (assessment.output.wording_score + assessment.output.meaning_score) / 200.0 >= 0.5


def evaluate() -> None:
    print("Set up OpenTelemetry.")
    otel_instrument()

    print("Load test data.")
    path = sys.argv[1]
    df = pl.read_csv(path)
    devset: list[dspy.Example] = [
        dspy.Example(text=text, rephrased_text=rephrased_text).with_inputs("text") for text, rephrased_text in df.rows()
    ]
    print(devset[0])

    print("Set up evaluator.")
    evaluator = Evaluate(devset=devset, num_threads=2, display_progress=True, display_table=0)

    print("Run evaluation without optimization!")
    with dspy.context(lm=gemini):
        evaluator(RephraseTextProgram(), metric=metric)
