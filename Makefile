ifneq (,$(wildcard ./config/.env))
    include ./config/.env
    export
endif

ENV?=local
FUNC?=DataCatalogueLambda
DIRNAME=`basename ${PWD}`
PG_EXEC=psql "host=localhost port=$(POSTGRES_PORT) user=$(POSTGRES_USER) password=$(POSTGRES_PASSWORD) gssencmode='disable'

cmd-exists-%:
	@hash $(*) > /dev/null 2>&1 || \
		(echo "ERROR: '$(*)' must be installed and available on your PATH."; exit 1)

help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/[:].*[##]/:/'

start-services: ## Start the Docker container services
	docker-compose --env-file ./config/.env up

stop-services: ## Stop the Docker container services
	docker-compose --envfile ./config/.env down

clean-services: ## Stop and remove all related Docker container services
	docker-compose --env-file ./config/.env down
	docker rm -f postgres pgadmin 2>/dev/null
	docker volume rm ${DIRNAME}_postgres-data 2>/dev/null

build-frontend: ## Build the frontend locally
	@echo "Building frontend for $(ENV)..."
	@cd ./frontend; rm -rf ./build || true; REACT_APP_ENV=$(ENV) npm install && npm run build

run-frontend: ## Run the frontend locally
	@echo "Running frontend for $(ENV)..."
	@cd ./frontend; REACT_APP_ENV=$(ENV) npm run start

deploy-frontend: ## Deploy the frontend to target environment
	@echo "Deploying the frontend to the $(ENV) environment in AWS..."
	@cd ./frontend; aws s3 sync ./build s3://$(ENV)-$(PROJECT_NAME)-deployment-frontend

build-backend: ## Build the backend api using sam
	@cd ./backend; sam build

build-backend-sync: ## Build the backend api using sam and keep contents synced for test
	@cd ./backend; nodemon --watch './src/**/*.py' --signal SIGTERM --exec 'sam' build -e "py"

deploy-backend: ## Deploy the backend api to target environment using sam
	@cd ./backend; sam deploy --config-env=$(ENV) --confirm-changeset --resolve-s3

run-backend-api: ## Run the backend api for CsvHandler and OtcClient locally using sam
	@cd ./backend; sam local start-api --port 8000

run-backend-function: ## Runs a standalone backend function locally using sam (default: DataCatalogueLambda)
	@cd ./backend; sam local invoke $(FUNC)

run-backend-pytest: ## Run the tests for backend
	@cd ./backend; pytest --continue-on-collection-errors --cov=./src --cov-report term-missing

fix-backend-lint: ## Fix the linting issues
	ruff format ./backend 
	ruff ./backend --fix
	isort ./backend

run-db-initialise: cmd-exists-psql ## Initialise the database with users/roles and schema
	@echo "Initialising the database..."
	@for file in `find ./sql/local -type f | sort | cut -c3-`; do ${PG_EXEC}" -f $$file; done

run-db-migrations: cmd-exists-psql ## Run the database migrations found under ./sql
	@echo "Running available database migrations..."
	@for file in `find ./sql -type f -depth 1 | sort | cut -c3-`; do ${PG_EXEC} dbname=$(PROJECT_NAME)_db" -f $$file; done

run-db-destroy: cmd-exists-psql ## Delete the database
	@echo "Destroying the database..."
	@${PG_EXEC}" -c "DROP DATABASE $(PROJECT_NAME)_db WITH (FORCE); "

# run-application-full: start-services run-db-migrations run-backend run-frontend