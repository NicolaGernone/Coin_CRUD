build:
	docker compose build

down:
	docker compose down

up: build makemigrations migrate
	docker compose up -d

migrate:
	docker compose run --rm api python manage.py migrate

show:
	docker compose run --rm api python manage.py showmigrations

makemigrations:
	docker compose run --rm api python manage.py makemigrations api

static:
	docker compose run --rm api python manage.py collectstatic --noinput --clear --no-post-process

user:
	docker compose run --rm api python manage.py createsuperuser

shell:
	docker compose run --rm api python manage.py shell

deps:
	docker compose run --rm api poetry install

bash:
	docker compose run --rm api /bin/sh

test: build migrate
	docker compose run --rm api python manage.py test

coverage: build migrate
	docker compose run --rm api coverage run --source='api' --omit='api/tests/*' manage.py test
	docker compose run --rm api coverage report
	docker compose run --rm api coverage xml