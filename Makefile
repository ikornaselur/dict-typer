mypy:
	poetry run mypy dict_typer tests

flake8:
	poetry run flake8 dict_typer tests

lint: mypy flake8

test:
	poetry run pytest tests -vxs

test_%:
	poetry run pytest tests -xvs -ktest_$*

shell:
	poetry run ipython
