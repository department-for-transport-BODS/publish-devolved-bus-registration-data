# Prerequisites

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

### Step 3: Start Services

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