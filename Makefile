ifneq (,$(wildcard ./config/.env))
    include ./config/.env
    export
endif

DIRNAME=`basename ${PWD}`
PG_EXEC=psql "host=$(POSTGRES_HOST) port=$(POSTGRES_PORT) user=$(POSTGRES_USER) password=$(POSTGRES_PASSWORD) gssencmode='disable'

cmd-exists-%:
	@hash $(*) > /dev/null 2>&1 || \
		(echo "ERROR: '$(*)' must be installed and available on your PATH."; exit 1)

help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

start-services: ## Start the Docker container services
	docker-compose --env-file ./config/.env up  ${service}

stop-services: ## Stop the Docker container services
	docker-compose --envfile ./config/.env down

clean-services: ## Stop and remove all related Docker container services
	docker-compose --env-file ./config/.env down
	docker rm -f postgres pgadmin 2>/dev/null
	docker volume rm ${DIRNAME}_postgres-data 2>/dev/null

run-backend: ## Run the backend api locally
	echo '[INFO] Don't forget to run "poetry shell -C ./backend && poetry install -C ./backend --no-root"
	uvicorn src.main:app --reload --port 8000 --app-dir=./backend

run-backend-pytest: ## Run the tests for backend
	echo '[INFO] Don't forget to run "poetry shell -C ./backend && poetry install -C ./backend --no-root"
	cd ./backend; pytest --cov=. --cov-report term-missing

build-backend-sam: ## Build the backend api using sam
	sam build --template-file=./backend/template.yaml

run-backend-sam: ## Run the backend api locally using sam
	sam local start-api --template-file=./backend/template.yaml

build-backend-docker: ## Build the backend api using docker
	docker build -t python-backend ./backend -f ./docker/python-backend/Dockerfile

run-backend-docker: build-backend-docker ## Run the backend api using docker
	docker rm -f python-backend || true
	docker run -t --name python-backend -p8000:8000 python-backend

fix-backend-lint: ## Fix the linting issues
	ruff ./backend --fix
	isort ./backend

run-db-initialise: cmd-exists-psql ## Initialise the database with users/roles and schema
	for file in `find ./sql/localdev -type f | sort | cut -c3-`; do ${PG_EXEC}" -f $$file; done

run-db-migrations: cmd-exists-psql ## Run the database migrations found under ./sql
	for file in `find ./sql -type f -depth 1 | sort | cut -c3-`; do ${PG_EXEC} dbname=$(PROJECT_NAME)" -f $$file; done

run-db-destroy: cmd-exists-psql ## Delete the database
	${PG_EXEC}" -c "DROP DATABASE $(PROJECT_NAME); "