# Fabrica Desarrolladores — Tasks API

[![Heroku](https://img.shields.io/badge/Deploy-Heroku-430098?logo=heroku)](https://fabrica-desarrolladores-3f0f43e8d854.herokuapp.com/)

Demo en Heroku: https://fabrica-desarrolladores-3f0f43e8d854.herokuapp.com/openapi/scalar

A small REST API for user registration, authentication (JWT) and task management (CRUD). Built with Flask, Flask-OpenAPI3, SQLAlchemy and Pydantic schemas for request/response validation and OpenAPI documentation.

This repository contains a minimal, well-structured example of a service that follows a clean separation between controllers, use-cases (commands/queries), models and error handling.

Table of contents
- Features
- Tech stack
- Quickstart (Windows / cmd.exe)
- Environment variables
- API endpoints (examples)
- OpenAPI / docs
- Project layout
- Development notes


Features
- Register and login users (password hashed + JWT access token)
- Create, list, read, update and delete tasks per user
- Pydantic models provide request/response schema for OpenAPI
- Commands/queries implement business rules and raise domain errors
- Centralized error handlers that map domain errors to JSON responses


Tech stack
- Python 3.10+
- Flask
- Flask-OpenAPI3 (OpenAPI 3 generation + docs)
- Flask-JWT-Extended (JWT auth)
- Flask-SQLAlchemy (ORM)
- Flask-Bcrypt (password hashing)
- Pydantic (request/response schemas)


Quickstart (Windows / cmd.exe)

1) Install dependencies (this project uses a Pipfile)

```cmd
pip install pipenv
pipenv install --dev
```

2) Set required environment variables (examples for cmd.exe)

```cmd
set SECRET_KEY=change-me
set JWT_SECRET_KEY=change-me-too
:: Either set DATABASE_URL (postgres) or let the app use the default sqlite file
:: set DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
:: or set SQLITE_PATH=sqlite:///instance/app.db
```

3) Run the app

```cmd
python src/app.py
```

By default the app will listen on 127.0.0.1:5000. The project includes a simple `@app.before_request` that creates database tables automatically (no migrations). The default DB is `sqlite:///app.db` (or the path specified in `SQLITE_PATH` / `DATABASE_URL`).


Environment variables
- SECRET_KEY — Flask secret key (default: "change-me")
- JWT_SECRET_KEY — Secret used to sign JWT tokens (default: "change-me-too")
- DATABASE_URL — Optional SQLAlchemy URL (e.g. postgresql://...)
- SQLITE_PATH — Optional convenience value for sqlite (e.g. sqlite:///instance/app.db). If not provided the default `sqlite:///app.db` is used.


API endpoints

All endpoints are prefixed with `/v1`. The auth endpoints are under `/v1/auth` and task endpoints use Spanish paths under `/v1/tareas`.

1) Register
- POST /v1/auth/register
- Body: { "username": "jdoe", "password": "s3cret", "email": "jdoe@example.com" }
- Response: { "code": 0, "message": "User registered successfully", "data": { "id": 1, "username": "jdoe" } }

2) Login
- POST /v1/auth/login
- Body: { "username": "jdoe", "password": "s3cret" }
- Response: { "code": 0, "message": "Login successful", "data": { "access_token": "<jwt>" } }

Example (curl / cmd):
```cmd
curl -X POST http://127.0.0.1:5000/v1/auth/login -H "Content-Type: application/json" -d "{\"username\":\"jdoe\",\"password\":\"s3cret\"}"
```

3) Tasks (require Authorization: Bearer <token>)
- GET /v1/tareas — List tasks for the authenticated user
- GET /v1/tareas/{tid} — Get a single task
- POST /v1/tareas — Create a task
  - Body: { "title": "Buy milk", "description": "2 liters", "completed": false }
- PUT /v1/tareas/{tid} — Update fields (partial allowed)
  - Body: { "title": "Buy milk (2%)" }
- DELETE /v1/tareas/{tid} — Delete a task

Include the JWT token in the Authorization header:

```cmd
curl -H "Authorization: Bearer <token>" http://127.0.0.1:5000/v1/tareas
```

Example create task (curl / cmd):
```cmd
curl -X POST http://127.0.0.1:5000/v1/tareas -H "Content-Type: application/json" -H "Authorization: Bearer <token>" -d "{\"title\":\"Buy milk\",\"description\":\"2 liters\"}"
```

Response schemas
- Successful responses follow the Pydantic models in `src/schemas/tasks.py` and `src/schemas/auth.py` (the top-level object has `code`, `message`, and `data`).
- Error responses are JSON objects with message details (handled by `src/errors/handlers.py`).


OpenAPI / API docs

The project uses Flask-OpenAPI3 which generates OpenAPI JSON and an interactive UI. When the server is running you can access the OpenAPI docs (example):

- GET /openapi.json — OpenAPI spec
- GET /openapi — Interactive docs UI (depends on the library configuration)

The API is documented with Pydantic request and response models. Endpoints that require authentication declare the `bearerAuth` OpenAPI security scheme so the docs indicate an Authorization header is required.


Project layout (important files)
- src/app.py — App factory / OpenAPI configuration
- src/blueprints/v1/auth.py — Authentication endpoints (register/login)
- src/blueprints/v1/tasks.py — Tasks endpoints
- src/commands — Business logic usecases (create/update/delete tasks, register users)
- src/queries — Read-only queries (get/list tasks, authenticate user)
- src/models — SQLAlchemy models (User, Task)
- src/schemas — Pydantic request/response models used for OpenAPI
- src/errors — Custom domain errors and error handlers


Development notes and next steps
- The app creates DB tables on request (no migration framework). For production, use Alembic and a proper DB server.
- Commands and queries raise domain exceptions (ValidationError, NotFoundError). Controllers rely on central error handlers to render proper HTTP responses.
- OpenAPI security is configured (bearerAuth); adjust per-route or globally in `src/app.py` and `src/blueprints/v1/tasks.py`.
- Add automated tests (unit + integration) to cover use-cases and controllers.


Contributing
- Feel free to open issues or PRs. Keep the project small and focused on clear separation between web layer and business rules.

License
- No license included. Add a LICENSE file if you intend to publish this repository.


Contact
- If you want improvements (tests, migrations, CI, docker-compose, deployment help), tell me what you'd like and I can implement them.
