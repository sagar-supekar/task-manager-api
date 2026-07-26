# Task Manager API

A REST API built with Flask and JWT authentication.

## Tech Stack
- Flask
- MySQL
- SQLAlchemy
- JWT Authentication
- HTML/CSS/JavaScript

## Features
- User registration and login
- JWT token authentication
- Create, read, update, delete tasks
- Mark tasks as complete

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /auth/register | Register new user |
| POST | /auth/login | Login and get token |
| GET | /tasks | Get all tasks |
| POST | /tasks | Create task |
| PUT | /tasks/<id> | Update task |
| DELETE | /tasks/<id> | Delete task |
| PATCH | /tasks/<id>/done | Mark as done |

## How to Run
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Create MySQL database: `CREATE DATABASE taskdb;`
4. Run: `python app.py`