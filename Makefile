DIRNAME=`basename ${PWD}`

help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

# Start the Docker container services
start-services:
	docker-compose up 

# Stop and remove the Docker container services
stop-services:
	docker-compose down

# initialise-database:

# Clean up the Docker image
clean: stop-services
	docker rm -f postgres pgadmin 2>/dev/null
	docker volume rm ${DIRNAME}_postgres-data 2>/dev/null