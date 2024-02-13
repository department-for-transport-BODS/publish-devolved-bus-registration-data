# Prerequisites
* [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
* [Node (v18.x.x) / NPM (v9.x.x)](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
* [PostgreSQL Client (psql)](https://www.postgresql.org/download/)
* [Docker Desktop](https://www.docker.com/get-started/) **or another container runtime of your choosing**

## Installation

### Step 1: Configure /etc/hosts

In order to emulate the correct flow in development, add to `/etc/hosts`:

```sh
127.0.0.1 www.devolved-registrations-portal.local postgres.local
```

### Step 2: Set up Docker Compose

Environment configuration when using Docker Compose is achieved using a `.env`
file that is passed to the docker containers. A template for the `.env` file is
provided in the repository (`.env.local.template`).

First copy the `.env.local.template` file to `.env` within the _config/_ 
directory:

```sh
# Assuming you're in the epp-app root directory
cp .env.local.template .env
```

### Step 3: Start Supporting Services

There are different options available when it comes to running the services 
locally. For database administration, this is managed using the previously 
configured Docker Compose, and both a PostgreSQL and pgAdmin container can 
be managed easily by running a combination of the following:

```sh
# Start up container services for backend data storage
make start-services

# Stop container services for backend data storage
make stop-services

# Stop and remove all related backend data storage container services
make clean-services
```

As part of the startup of PostgreSQL, the initial project database will be created 
with roles defined within the `./sql/localdev` directory.

### Step 4: Initialise the Database Schema

Whilst the application database itself is created as part of the PostgreSQL
startup, creation of the schema and any further database migrations requires
that a subsequent _make_ command is executed:

```sh
# Run all .sql scripts sequentially against the application database
make run-db-migrations
```

This will fully initialise the database and populate it with the necessary
tables/triggers that allow for storage of data by the application.


### Step 5: Start Up the Application Frontend / Backend

The frontend application is written in React and uses NPM to manage the 
build and run of its components.

The backend api is written in Python and uses AWS SAM for deployment into 
any target environment. For local testing AWS SAM provides an option to run
these services locally (using Docker on the backend, although this process
is hidden from the end user). 

In order to start these services up, it is necessary to run:

```sh
# Start up the frontend
make run-frontend

# Start up the backend
make run-backend
```

It is advisable (and at times necessary) to run each service in separate 
terminals to be able to take full advantage of any debug logging that may
occur as a result of running these applications. It is worth noting that 
changes to the underlying codebase should be reflected in the already
running application(s), without the need for additional rebuilding.