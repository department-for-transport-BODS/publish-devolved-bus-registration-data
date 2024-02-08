help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

run: ## Run the backend api locally
	uvicorn src.main:app --reload --port 8000

pytest: ## Run the tests
	pytest  --cov=. --cov-report term-missing #--cov-report=html

slocal: ## Run the backend api locally using sam
	sam local start-api #--docker-network host

fix-lint: ## Fix the linting issues
	ruff . --fix
	isort .

sbuild: ## Build the backend api using sam
	sam build