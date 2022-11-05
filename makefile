dev:
	docker compose up

app:
	docker compose up --force-recreate -d

install:
	python -m pip install -r requirements.txt

update-reqs:
	python -m pip install -U -r requirements.in
	python -m pip freeze > requirements.txt

docker:
	docker build -t apiad/matcom-dashboard:latest .

shell:
	docker compose run app bash

update:
	docker compose run app bash make update-reqs
	make docker
	docker push

sync:
	git add data/*.yaml
	git commit -m "Update data" || echo "Nothing to commit"
	git pull --no-edit
	git push
