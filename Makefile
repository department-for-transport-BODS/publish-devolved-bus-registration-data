DIRNAME=`basename ${PWD}`

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