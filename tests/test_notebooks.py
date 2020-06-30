"""Execute the Jupyter notebooks used as examples to ensure no errors are present."""

import os
import subprocess
import tempfile
import pytest


NOTEBOOKS = list(map(lambda filename: os.path.join(os.path.dirname(__file__), filename), [
    "../examples/rooms.ipynb"
]))


@pytest.mark.parametrize("notebook", NOTEBOOKS)
def test_notebook(notebook):

    with tempfile.NamedTemporaryFile(suffix=".ipynb") as fout:
        args = ["jupyter", "nbconvert", notebook,
                "--output", fout.name,
                "--to", "notebook",
                "--execute", "--ExecutePreprocessor.timeout=60"]
        subprocess.check_call(args)
