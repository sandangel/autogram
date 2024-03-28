"""Generate examples of rephrasing text!"""

import sys
from pathlib import Path
from typing import Any, List, Literal

import dspy
import polars as pl
from datasets import Dataset
from dspy.experimental import SyntheticDataGenerator

from shortcutx.instrument import otel_instrument
from shortcutx.llm import gemini
from shortcutx.signature import RephraseText

dspy.settings.configure(lm=gemini)

otel_instrument()


def export(
    data: List[dspy.Example],
    path: str,
    mode: Literal["csv, json", "arrow", "hf"] | None = None,
    **kwargs: Any,
) -> None:
    """Export examples to disk.

    Args:
        data (list[dspy.Example]): Examples to export
        path (pathlib.Path): Path to export to
        mode (str | None, optional): Mode to export to.
        **kwargs (Any, optional): Additional keyword arguments to pass to the export function. Defaults to None.
    """
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    extension = mode or path.split(".")[-1]

    dataset = Dataset.from_list(
        [example.toDict() for example in data],
    )

    if extension == "csv":
        dataset.to_csv(path_or_buf=path, **kwargs)

    elif extension == "json":
        dataset.to_json(path_or_buf=path, **kwargs)

    elif extension == "arrow" or extension == "hf":
        dataset.save_to_disk(path)


def generate():
    """Generate examples for optimizing rephrasing text."""
    path = sys.argv[1]
    sample_size = int(sys.argv[2])
    generator = SyntheticDataGenerator(schema_class=RephraseText)
    examples = generator.generate(sample_size=sample_size)
    export(examples, path)


def generate_test():
    """Generate test data for rephrasing text."""
    path = sys.argv[1]
    sample_size = int(sys.argv[2])
    examples = [
        dspy.Example(text=text, rephrased_text=rephrased_text)
        for text, rephrased_text in pl.read_csv("data/rephrase_text/dataset.csv").rows()
    ]
    num_existing = len(examples)
    generator = SyntheticDataGenerator(schema_class=RephraseText, examples=examples)
    examples = generator.generate(sample_size=sample_size)
    export(examples[num_existing:], path)
