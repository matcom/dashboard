dev:
	USER=`id -u` docker compose up app

app:
	USER=`id -u` docker compose up --force-recreate -d

install:
	python -m pip install -r requirements.txt

update-reqs:
	python -m pip install -U -r requirements.in
	python -m pip freeze > requirements.txt

docker:
	docker build -t apiad/matcom-dashboard:latest .

shell:
	USER=`id -u` docker compose run app bash

update:
	USER=0 docker compose run app make update-reqs
	make docker
	docker push apiad/matcom-dashboard

sync:
	git add data/*.yaml
	git commit -m "Update data" || echo "Nothing to commit"
	git pull --no-edit
	git push
