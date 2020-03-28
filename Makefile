mypy:
	poetry run mypy dict_typer tests/unit tests/e2e

flake8:
	poetry run flake8 dict_typer tests/unit tests/e2e

lint: mypy flake8

test: unit_test integration_test e2e_test

unit_test:
	poetry run pytest tests/unit -xvvs

integration_test:
	poetry run pytest tests/integration -xvvs

e2e_test:
	poetry run pytest tests/e2e -xvvs

test_%:
	poetry run pytest tests -xvvs -ktest_$*

shell:
	poetry run ipython
