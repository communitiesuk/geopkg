import subprocess
import warnings
from pathlib import Path

from typing_extensions import Literal

import geopkg

Action = Literal["raise", "warn", "ignore"]

PATH_PACKAGE = (Path.cwd() / geopkg.__name__).absolute().as_posix()
INI = Path("./mypy.ini").absolute().as_posix()
ACTIONS = frozenset(["raise", "warn", "ignore"])


def test_mypy(action: Action = "warn") -> None:
    """Test using mypy."""
    if action not in ACTIONS:
        raise ValueError(f"Invalid value for the 'action' parameter: {action!r}")

    command = f"mypy {PATH_PACKAGE!r} --config-file {INI!r}"
    out = subprocess.run(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, check=False
    )

    stdout = out.stdout.decode()
    stderr = out.stderr.decode()
    assert not stderr, stderr

    if action == "warn" and out.returncode != 0:
        warnings.warn(stdout)

    if action == "raise":
        try:
            assert out.returncode == 0, stdout
        except AssertionError as ex:
            msg = stdout.rsplit("\n", maxsplit=2)[1]
            raise AssertionError(msg) from ex
