
# 🚀 Local Cloud – Django REST Backend

A **production‑ready Django REST Framework backend** built with **clean architecture**, **Celery**, **JWT authentication**, **LocalStack (AWS mock)**, and **Docker‑based local infrastructure**.

This project is designed as a **real‑world backend system** suitable for:
- Portfolio / resume projects
- Backend + DevOps learning
- CI‑ready applications

---

## ✨ Features

### 🔐 Authentication
- JWT authentication using **SimpleJWT**
- Login & token refresh APIs

### 👤 Users
- Custom user model
- User CRUD APIs
- Background tasks support

### 📦 Products
- Product CRUD APIs
- Image upload via **Celery async task**
- Quota‑based product creation
- Filters, search, pagination
- Cached product statistics

### ☁️ AWS (LocalStack)
- S3 – product image storage
- SES – email sending
- CloudWatch – centralized logging
- Fully mocked locally using **LocalStack**

### ⚙️ Infrastructure
- PostgreSQL
- Redis
- RabbitMQ
- Celery workers & beat
- Docker & Docker Compose

### 🧪 Testing & Quality
- Pytest (root‑level `tests/` folder)
- Factory Boy
- Integration tests (Celery, SES, CloudWatch)
- Pre‑commit hooks
- GitHub Actions CI pipeline

---

## 🗂️ Project Structure

```
backend/
├── apps/
│   ├── auth/        # JWT authentication
│   ├── users/       # Custom user app
│   ├── products/    # Product domain (models, services, tasks)
│   └── core/        # Shared logic (logging, storage, email, pagination)
├── celery.py        # Celery configuration
├── settings.py      # Django settings
├── urls.py          # Root API routing
└── templates/       # Email templates

tests/               # Root‑level tests (pytest)
docker-compose.yml   # Local infrastructure
Dockerfile            # Multi‑stage Docker build
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-----|-----------|
| Backend | Django 5.x, DRF |
| Auth | JWT (SimpleJWT) |
| Async | Celery |
| Broker | RabbitMQ |
| Cache | Redis |
| DB | PostgreSQL |
| Storage | S3 (LocalStack) |
| Email | SES (LocalStack) |
| Logs | CloudWatch (LocalStack) |
| Infra | Docker, Docker Compose |
| CI | GitHub Actions |
| Tests | Pytest |

---

## ⚙️ Environment Setup

### 1️⃣ Clone repository
```bash
git clone <repo-url>
cd local-cloud
```

### 2️⃣ Create `.env`
```bash
cp .env.example .env
```

Update values as needed.

---

## 🐳 Run Infrastructure (LocalStack, DB, etc.)

```bash
docker compose up -d
```

Services started:
- PostgreSQL
- Redis
- RabbitMQ
- LocalStack (S3, SES, CloudWatch)

---

## 🐍 Local Development (Without Docker)

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## 🐳 Run Application with Docker

```bash
docker build -t local-cloud-backend .
docker run --env-file .env -p 8000:8000 local-cloud-backend
```

---

## 🔁 Celery Workers

```bash
celery -A backend worker -l info
celery -A backend beat -l info
```

---

## 🧪 Running Tests

```bash
pytest
```

Run pre‑commit manually:
```bash
pre-commit run --all-files
```

---

## 🔄 CI Pipeline

GitHub Actions pipeline includes:
1. Pre‑commit checks
2. PostgreSQL, Redis, RabbitMQ, LocalStack
3. Migrations
4. Pytest execution

Pipeline file:
```
.github/workflows/ci.yml
```

---

## 📚 API Documentation

- Swagger UI
  `http://localhost:8000/api/docs/swagger`
- Redoc
  `http://localhost:8000/api/docs/redoc`

---

## 📩 Emails (SES – LocalStack)

Emails are sent asynchronously via Celery using SES mock.

Templates:
```
backend/templates/email/
```

---

## 🧠 Design Principles

- Service‑layer business logic
- Thin views
- Async background processing
- Cache‑first reads
- Signals for side‑effects
- Clean separation of concerns

---

## 🚀 Ideal Use Cases

- Backend portfolio project
- DevOps practice with LocalStack
- Celery + Django reference project
- CI‑ready Django template

---

## 🧑‍💻 Author

**Shiyas**
Backend Developer | Django | DevOps Enthusiast

---

## 📜 License

MIT License
