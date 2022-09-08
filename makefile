app:
	docker-compose up

dev:
	streamlit run dashboard/dashboard.py

env:
	python3 -m venv .venv

install:
	python -m pip install -r requirements.txt

update-reqs:
	python3 -m pip install -U -r requirements.in
	python3 -m pip freeze > requirements.txt

docker:
	docker build -t matcom/dashboard:latest .

shell:
	docker-compose run app bash
