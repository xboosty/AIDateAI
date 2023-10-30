# my-fastapi-rest-api

This is a REST API built with FastAPI and Postgres. It follows a modular architecture with separate layers for controllers, models, DTOs, services, exceptions, persistence, and configuration. The API includes endpoints for one-to-one, one-to-many, and many-to-many relationships between users, items, and orders.

## Installation

1. Clone the repository.
2. Install the dependencies listed in `requirements.txt`.
3. Create a Postgres database and update the connection details in `config.py`.
4. Run the `app.py` file to start the API.

## Usage

The API includes the following endpoints:

- `/users`: CRUD operations for users.
- `/items`: CRUD operations for items.
- `/orders`: CRUD operations for orders.
- `/user_items`: CRUD operations for user-item relationships.

The API documentation can be accessed at `/docs` or `/redoc`.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.