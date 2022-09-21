dev:
	docker-compose up

app:
	docker-compose up --force-recreate -d

install:
	python -m pip install -r requirements.txt

update-reqs:
	python3 -m pip install -U -r requirements.in
	python3 -m pip freeze > requirements.txt

docker:
	docker build -t apiad/matcom-dashboard:latest .

shell:
	docker-compose run app bash

sync:
	git add data/*.yaml
	git commit -m "Update data" || echo "Nothing to commit"
	git pull --no-edit
	git push
	make app
