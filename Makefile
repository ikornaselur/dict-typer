mypy:
	@poetry run mypy dict_typer tests/*

flake8:
	@poetry run flake8 dict_typer tests/*

lint: mypy flake8

test: unit_test snapshot_test e2e_test

unit_test:
	@poetry run pytest tests/unit -xvvs

snapshot_test:
	@poetry run pytest tests/snapshot -vvs

update_snapshots:
	@poetry run pytest tests/snapshot --snapshot-update

e2e_test:
	@poetry run pytest tests/e2e -xvvs

test_%:
	@poetry run pytest tests -xvvs -ktest_$*

shell:
	@poetry run ipython

install_git_hooks:
	@ln -s `pwd`/.hooks/pre-push .git/hooks/pre-push
