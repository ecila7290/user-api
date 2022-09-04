.PHONY: init run test migrate

init:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

run:
	uvicorn main:app --reload

test:
	python -m pytest

migrate:
	alembic revision --autogenerate -m '$(msg)'
	alembic upgrade head