# Prerequisites

## Installation

### Step 1: Configure /etc/hosts

In order to emulate the correct flow in development, add to `/etc/hosts`:

```sh
127.0.0.1 www.devolved-registrations-portal.local postgres
```

### Step 2: Set up Docker Compose for backend

Environment configuration when using Docker Compose is achieved using a `.env`
file that is passed to the docker containers. A template for the `.env` file is
provided in the repository (`.env.local.template`).

First copy the `.env.local.template` file to `.env`.

```sh
# assuming you're in the epp-app root directory
cp .env.local.template .env
```