"""Render the frozen results with smaller panel titles; preserve the original figure."""
from pathlib import Path
import shutil
import tempfile

import matplotlib

from plot import plot


ROOT = Path(__file__).resolve().parent

if __name__ == "__main__":
    matplotlib.rcParams["axes.titlesize"] = 8
    with tempfile.TemporaryDirectory() as directory:
        temporary = Path(directory)
        for name in ("summary.json", "predictions.csv"):
            shutil.copyfile(ROOT/"results-v1"/name, temporary/name)
        plot(temporary)
        figure = temporary/"comparison.png"
        assert figure.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
        shutil.copyfile(figure, ROOT/"comparison.png")
