MANAGE := poetry run python3 manage.py
RUN := poetry run

install:
	@poetry install

make-migration:
	@$(MANAGE) makemigrations

migrate: make-migration
	@$(MANAGE) migrate

build: install migrate

lint:
	$(RUN) flake8 ./library_app/

check:
	poetry check

test-html-coverage:
	$(RUN) coverage run --source='.' manage.py test library_app
	$(RUN) coverage html

develop: lint check test-html-coverage

test:
	$(MANAGE) test

test-coverage:
	$(RUN) coverage run --source='.' manage.py test --noinput library_app
	$(RUN) coverage lcov

start:
	$(MANAGE) runserver

deploy:
	$(RUN) gunicorn library_app.wsgi

shell:
	@$(MANAGE) shell

celery:
	python3 -m celery -A library_app worker -l info

docker:
	docker compose up

clean:
	rm .coverage
	rm -rf *lcov
