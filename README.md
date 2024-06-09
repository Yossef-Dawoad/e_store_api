# E-commerce REST API (FastAPI)
This is a production-ready, testable, and Dockerized RESTful API built with Python (FastAPI) for an e-commerce application.
Features
 * User Authentication: JWT-based authentication system for secure user access with email notifications.
 * Asynchronous Database Interactions: Utilizes asynchronous interactions with a PostgreSQL database for efficient data handling and scalability.
 * Database Migrations: Supports database migrations to ensure a smooth evolution of the API's data schema.
 * Dockerized Services: Leverages Docker Compose to simplify deployment and manage dependencies for the database, email service, and application itself.
### Getting Started
 * Prerequisites:
   * Python 3.6+
   * pipenv (or virtualenv)
   * Docker
 * Clone the repository:
 ```bash
git clone https://github.com/your-username/e-commerce-api.git
```
 * Install dependencies:
 ```bash
cd e-commerce-api
pip install -r requirements.txt
# OR if you have poetry installed 
poetry install
```

 * Configure environment variables:
   Create a file named .env in the project root directory and define the following environment variables:
   * DATABASE_URL: Your PostgreSQL database connection string
   * EMAIL_USERNAME: Username for your email notification service
   * EMAIL_PASSWORD: Password for your email notification service
 * Run the API:
```bash
Docker-compose -d up build
# OR if You have similar dicker services in your local machine
# with environments keys configured correctly you can run
fastapi run 
```

This will start the API development server. You can access the API documentation at `http://localhost:8000/docs`.
### Usage
Refer to the API documentation for detailed information on endpoints, request parameters, and response formats. The documentation is accessible at `http://localhost:8000/docs` when the API is running.
### Testing
The project includes unit tests for the API functionality. To run the tests:
```bash
poetry test 
```
### Deployment
Docker Compose is used to manage deployment. The docker-compose.yml file defines the services for the database, email service, and the API application.
To build and run the Docker containers:
```bash
docker-compose up -d
```

This will start all the services in detached mode. You can access the API documentation at http://localhost:8000/docs after the containers are up and running.
Contributing
Pull requests are welcome! Please create a pull request with your changes and any relevant documentation updates.
