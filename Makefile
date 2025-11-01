.PHONY: setup
setup:
	pip install '.[dev]'

.PHONY: lint-repl
lint-repl:
	PYTHONPATH="$$PWD/pylint_checkers" pylint repl.py
