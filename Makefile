all: format lint test
format: black ruff
lint: pyright mypy

black:
	poetry run black --preview .

ruff:
	poetry run ruff check . --fix

mypy:
	poetry run mypy .

pyright:
	poetry run pyright

test:
	poetry run pytest tests
	poetry run python tests/segwit_addr.py
