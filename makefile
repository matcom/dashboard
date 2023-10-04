dev:
	USER=`id -u` docker-compose up app

app:
	USER=`id -u` docker-compose up --force-recreate -d

install:
	python -m pip install -r requirements.txt

update-reqs:
	docker run -v `pwd`:/src apiad/matcom-dashboard bash -c "python -m pip install -U -r /src/requirements.in && python -m pip freeze > /src/requirements.txt"

docker:
	DOCKER_BUILDKIT=1 docker build -t apiad/matcom-dashboard:latest .

shell:
	USER=`id -u` docker compose run app bash

root:
	USER=0 docker compose run app bash

update:
	make update-reqs
	make docker
	docker push apiad/matcom-dashboard
