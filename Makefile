.PHONY: init run test

init:
	python -m pip install --upgrade pip
	pip install -r requirements.txt
	pip install flake8

run:
	uvicorn main:app --reload

test:
	python -m pytest