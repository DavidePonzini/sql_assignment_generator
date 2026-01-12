########## Makefile start ##########
# Type: PyPi
# Author: Davide Ponzini

NAME=sql_assignment_generator
VENV=./venv
REQUIREMENTS=requirements.txt

ifeq ($(OS),Windows_NT)
	VENV_BIN=$(VENV)/Scripts
else
	VENV_BIN=$(VENV)/bin
endif

.PHONY: install build uninstall documentation upload download clean

$(VENV):
	python -m venv --clear $(VENV)
	touch -a $(REQUIREMENTS)
	$(VENV_BIN)/python -m pip install --upgrade -r $(REQUIREMENTS)

$(VENV)_upgrade: $(VENV)
	$(VENV_BIN)/python -m pip install --upgrade -r $(REQUIREMENTS)

.env:
	cp .env.template .env
	echo "Please edit the .env file to add your environment variables."

install: uninstall build
	$(VENV_BIN)/python -m pip install ./dist/*.whl

build: $(VENV) .env
	rm -rf dist/
	$(VENV_BIN)/python -m build

uninstall: $(VENV)
	$(VENV_BIN)/python -m pip uninstall -y $(NAME)

documentation:
	make html SPHINXBUILD="../$(VENV_BIN)/sphinx-build" -C docs/

upload: build documentation
	$(VENV_BIN)/python -m pip install --upgrade twine
	$(VENV_BIN)/python -m twine upload --verbose dist/*

download: uninstall
	$(VENV_BIN)/python -m pip install $(NAME)

clean:
	find . -type d -name '__pycache__' -print0 | xargs -0 rm -r || true
	rm -rf dist docs/_build .pytest_cache .coverage tests/htmlcov


########## Makefile end ##########
