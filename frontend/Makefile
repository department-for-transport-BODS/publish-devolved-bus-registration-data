help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

build: ## Build the frontend
	@echo "Building frontend..."
	@cd frontend && npm run build
	@echo "Done"


run: ## Run the frontend
	@echo "Running frontend..."
	@npm run start
	@echo "Done"