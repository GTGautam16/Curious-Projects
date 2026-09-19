# 🎫 Support Ticket API

A production-style **full-stack customer support ticket system** built with **FastAPI, React, PostgreSQL, and Docker**.

## ✨ Features

* 🎟️ Create, view, update & delete tickets
* 🔐 Input validation with Pydantic
* 🗄️ PostgreSQL database with SQLAlchemy
* ⚡ REST API with FastAPI
* 🖥️ React dashboard
* 🧪 API testing with Pytest
* 🐳 Fully Dockerized with Docker Compose
* 🔄 Frontend ↔ Backend API integration

## 🛠️ Tech Stack

| Layer            | Technology             |
| ---------------- | ---------------------- |
| Backend          | Python, FastAPI        |
| Frontend         | React, Vite            |
| Database         | PostgreSQL             |
| ORM              | SQLAlchemy             |
| Validation       | Pydantic               |
| Testing          | Pytest                 |
| Containerization | Docker, Docker Compose |

## 📁 Structure

```text
Support-Ticket-API/
├── app/                 # FastAPI backend
├── frontend/            # React dashboard
├── tests/               # Pytest tests
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## 🚀 Run with Docker

```bash
docker compose up --build
```

Open:

* 🌐 **Dashboard:** `http://localhost:5173`
* 🔌 **API:** `http://localhost:8000`
* 📚 **Swagger:** `http://localhost:8000/docs`

Stop:

```bash
docker compose down
```

## 🧪 Tests

```bash
pytest
```

Current test status:

```text
3 passed
```

## 🎯 Purpose

Built as a mini production-style project to practice:

**REST APIs → Databases → React → Testing → Docker → Full-Stack Integration**
