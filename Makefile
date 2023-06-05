env = env PATH="${bin}:$$PATH"

venv: .venv/touchfile ## Create virtual environment
.venv/touchfile:
	test -d .venv || python3 -m venv .venv
	. .venv/bin/activate && pip install -U pip
	. .venv/bin/activate && pip install -U pip-tools
	. .venv/bin/activate && ${env} pip-compile --extra dev
	. .venv/bin/activate && ${env} pip-sync
	. .venv/bin/activate && ${env} pip install -e .
	touch .venv/touchfile

clean_venv: ## Remove virtual environment
	@echo "Cleaning venv"
	@rm -rf .venv

run:
	. .venv/bin/activate && ${env} python -m app.main

pip-sync: ## synchronizes the .venv with the state of requirements.txt
	. .venv/bin/activate && ${env} pip-compile --extra dev
	. .venv/bin/activate && ${env} pip-sync
	. .venv/bin/activate && ${env} pip install -e .

setup: venv app.conf
app.conf:
	cp app.conf.example app.conf

lint:
	. .venv/bin/activate && ${env} pylint app
	. .venv/bin/activate && ${env} black --check app

audit:
	. .venv/bin/activate && ${env} bandit app

fix:
	. .venv/bin/activate && $(env) black app tests

test: venv setup
	. .venv/bin/activate && ${env} pytest tests

type-check:
	. .venv/bin/activate && ${env} MYPYPATH=stubs/ mypy --show-error-codes app

coverage:
	. .venv/bin/activate && ${env} coverage run -m pytest tests && coverage report && coverage html

check-all: lint type-check test audit
