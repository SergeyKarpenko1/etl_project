.PHONY: run test format lint check

PYTHON ?= python
CODE_PATHS := src tests main.py

run:
	PYTHONPATH=src $(PYTHON) main.py

test:
	$(PYTHON) -m pytest tests/ -v

format:
	$(PYTHON) -m black $(CODE_PATHS) # автоформатирование кода

lint:
	$(PYTHON) -m black --check --diff $(CODE_PATHS) # проверка формата 

check: lint test # тесты перед коммитом
