#!../venv/bin/pytest

from latex_runner.config_types import Color

def test_color_repr() -> None:
	assert repr(Color('red')) == "Color('red')"
