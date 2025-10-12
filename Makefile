.PHONY: setup
setup:
	pip install '.[dev]'

.PHONY: pylint
pylint:
	PYTHONPATH="$$PWD/pylint_checkers" pylint test.py
