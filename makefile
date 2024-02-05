run-dev: run-dev-frontend  run-dev-backend

run-dev-frontend: ## Run the frontend
	@echo "Running frontend..."
	@cd frontend && make run
	@echo "Done"

run-dev-backend: ## Run the backend
	@echo "Running backend..."
	@cd backend && make run
	@echo "Done"

d-run-backend: ## Run the backend in detached mode
	@echo "Running backend in detached mode..."
	@docker-compose up --build backend
	@echo "Done"
d-stop-backend: ## Stop the backend
	@echo "Stopping backend..."
	@docker-compose down
	@echo "Done"