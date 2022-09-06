.PHONY: init run test revision migrate

init:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

run:
	uvicorn main:app --reload

test:
	python -m pytest

revision:
	alembic revision --autogenerate -m '$(msg)'

migrate:
	alembic upgrade head