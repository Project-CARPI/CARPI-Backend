# CARPI Course Planner - API

This is the API service for the CARPI Course Planner application. It is designed to work in tandem with the [frontend](https://github.com/Project-CARPI/site) and [SIS scraper](https://github.com/Project-CARPI/sis-scraper).

## Running the API

### Prerequisites

- **[Docker](https://www.docker.com/products/docker-desktop/)** (Required): Used for the streamlined development environment setup.
- **[Python >= 3.12](https://www.python.org/)** (Optional): Useful for code editor linting or running the API locally without Docker.

### Setup Instructions

**1. Configure Environment Variables**

Create a copy of the `example.env` file in the project root and rename it to `.env`.

The default values provided in the example file will work out of the box, but they can be customized as needed.

**2. Start the Development Environment**

With Docker Engine running, execute the following command in your terminal:

```bash
docker compose run --rm api && docker compose down
```

### About the Database Environment

- **Shared Database:** The development environment pulls a shared MySQL database service definition from an external repository, creating a local database volume.
- **Data Persistence:** The test database volume persists between Docker start and stop cycles, ensuring test data remains available across development sessions and for other services that depend on the database.
- **Resetting the Database:** To completely rebuild the database from scratch, you must manually remove the corresponding Docker volume prior to starting the environment.
