import tomllib
from pathlib import Path


def test_pyproject_toml_parses() -> None:
    pyproject_path = Path(__file__).resolve().parents[1] / "pyproject.toml"
    tomllib.loads(pyproject_path.read_text(encoding="utf-8"))

