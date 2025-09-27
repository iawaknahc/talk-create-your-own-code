.PHONY: setup
setup:
	pip install '.[dev]'

.PHONY: pylint
pylint:
	PYTHONPATH="$$PWD/pylint_checkers" pylint --load-plugins=urllib_parse --disable=all --enable=urllib-parse-rfc3986 test.py
