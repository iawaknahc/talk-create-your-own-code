venv:
	python3 -m venv venv

.PHONY: setup
setup:
	pip install '.[dev]'

.PHONY: lint-repl
lint-repl:
	PYTHONPATH="$$PWD/pylint_checkers" pylint repl.py

.PHONY: celery-worker
celery-worker:
	celery -A tasks worker

.PHONY: celery-call
celery-call:
	celery -A tasks call tasks.main_task

.PHONY: lint-tasks
lint-tasks:
	PYTHONPATH="$$PWD/pylint_checkers" pylint tasks.py
