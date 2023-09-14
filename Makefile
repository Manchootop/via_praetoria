.PHONY: install
install:
	poetry install

.PHONY: migrate
migrate:
	poetry run python -m core.manage migrate

.PHONY: migrations
migrations:
	poetry run python -m core.manage makemigrations

.PHONY: run-server
run-server:
	poetry run python -m core.manage runserver

.PHONY: run-server-debug
run-server-debug:
	poetry run python -m core.manage runserver --noreload

.PHONY: superuser
superuser:
	poetry run python -m core.manage createsuperuser


.PHONY: update
update: install migrate ;

.PHONY: shell
shell:
	poetry run python -m core.manage shell

p-venv:
	poetry shell

enter-venv:
	.\venv\Scripts\Activate
