#!venv/bin/pytest

import os

import _pytest


# Passing `--template=html-dots/index.html --report=logs/report-{envname}.html` to pytest in tox.ini breaks pytest in Python 3.6.
# Setting the arguments here also allows me to easily generate a report name with python if needed.
def pytest_configure(config: '_pytest.config.Config') -> None:
	root = os.path.dirname(__file__)
	if not getattr(config.option, 'template', None):
		config.option.template = ['html-dots/index.html']
	if not getattr(config.option, 'report', None):
		config.option.report = [os.path.join('logs', 'report-%s.html' % os.environ.get('TOX_ENV', 'no-tox'))]
	print("config.option.template", config.option.template)
	print("config.option.report", config.option.report)
