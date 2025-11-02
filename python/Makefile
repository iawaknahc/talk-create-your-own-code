venv:
	python3 -m venv venv

.PHONY: setup
setup:
	pip install '.[dev]'

.PHONY: lint-repl
lint-repl:
	PYTHONPATH="$$PWD/pylint_checkers" pylint repl.py

.PHONY: worker
worker:
	celery -A tasks worker

.PHONY: lint-tasks
lint-tasks:
	PYTHONPATH="$$PWD/pylint_checkers" pylint tasks.py
