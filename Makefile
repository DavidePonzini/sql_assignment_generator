########## Makefile start ##########
# Type: PyPi
# Author: Davide Ponzini

VENV=./venv

ifeq ($(OS),Windows_NT)
	VENV_BIN=$(VENV)/Scripts
else
	VENV_BIN=$(VENV)/bin
endif


venv:
	python -m venv --clear $(VENV)
	$(VENV_BIN)/python -m pip install --upgrade -r requirements.txt


########## Makefile end ##########
