import sys

import cloudpickle as pk
import dspy
import polars as pl
from dspy.evaluate import Evaluate
from dspy.teleprompt import MIPRO

from shortcutx.evaluator import metric
from shortcutx.instrument import otel_instrument
from shortcutx.llm import gemini
from shortcutx.program import RephraseTextProgram


def compile() -> None:
    otel_instrument()
    path = sys.argv[1]
    compiled_path = sys.argv[2]
    df = pl.read_csv(
        path,
        truncate_ragged_lines=True,
    )
    dataset: list[dspy.Example] = [
        dspy.Example(
            text=text,
            rephrased_text=rephrased_text,
        ).with_inputs("text")
        for text, rephrased_text in df.rows()
    ]

    trainset = dataset[:40]
    devset = dataset[40:]

    eval_kwargs = dict(num_threads=1, display_progress=True, display_table=0)
    evaluate = Evaluate(devset=devset, metric=metric, **eval_kwargs)

    program = RephraseTextProgram()

    # with dspy.context(lm=gemini):
    #     baseline_eval = evaluate(program, devset=devset, **kwargs)
    #     baseline_train = evaluate(program, devset=trainset, **kwargs)
    #     print(f"Baseline train: {baseline_train}")
    #     print(f"Baseline dev: {baseline_eval}")

    # Set up a basic teleprompter, which will compile our program.
    teleprompter = MIPRO(metric=metric, prompt_model=gemini, task_model=gemini, verbose=True)

    # Compile!
    with dspy.context(lm=gemini):
        compiled_program = teleprompter.compile(
            program,
            trainset=dataset,
            num_trials=20,
            max_bootstrapped_demos=3,
            max_labeled_demos=5,
            eval_kwargs=eval_kwargs,
        )
        # optimized_eval = evaluate(compiled_program, devset=devset, **kwargs)
        # optimized_train = evaluate(compiled_program, devset=trainset, **kwargs)
        # print(f"Optimized train: {optimized_train}")
        # print(f"Optimized dev: {optimized_eval}")

        # Saving
        pk.dump(compiled_program, open(compiled_path, "wb"))
