DIRNAME=`basename ${PWD}`

help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

start-services: ## Start the Docker container services
	docker-compose --env-file ./config/.env up 

stop-services: ## Stop and remove the Docker container services
	docker-compose --envfile ./config/.env down

sss: ## Start a Specific Service
	docker-compose --env-file ./config/.env up ${service}
# initialise-database:

# Clean up the Docker image
clean-services: ## Stop and remove the Docker container services
	docker-compose --env-file ./config/.env down
	docker rm -f postgres pgadmin 2>/dev/null
	docker volume rm ${DIRNAME}_postgres-data 2>/dev/null