# Reproducible Setup Guide

This guide provides step-by-step instructions to set up, run, test, and deploy the Data Opportunity Portal (FastAPI + Jinja2 + SQLite + OpenAI LLM) using Docker.

---

## 1. Prerequisites
- Docker and Docker Compose installed ([Get Docker](https://docs.docker.com/get-docker/))
- (Optional) Python 3.11+ for local development
- (Optional) Git for version control

---

## 2. Clone the Repository
```sh
git clone https://github.com/himanshujohn/ai-dev-tools-zoomcamp.git
cd "ai-dev-tools-zoomcamp"
cd "Project Attempt 1"
```

---

## 3. Environment Variables & Secrets
- Copy `backend/.env.example` to `backend/.env` and set your `OPENAI_API_KEY`.
- Never commit `.env` files to version control.

Example `backend/.env`:
```
OPENAI_API_KEY=sk-...your-key...
```

---

## 4. Build and Run with Docker Compose
```sh
docker-compose build
docker-compose up -d
```
- Frontend: http://localhost:8000
- Backend API: http://localhost:8001

---

## 5. Local Development (Optional)
- Backend:
  ```sh
  cd backend
  pip install -r requirements.txt
  uvicorn main:app --reload --port 8001
  ```
- Frontend:
  ```sh
  cd frontend
  pip install -r requirements.txt
  uvicorn main:app --reload --port 8000
  ```

---

## 6. Database Initialization
- The backend will auto-create `opportunity.db` on first run.
- To manually initialize:
  ```sh
  cd backend
  python db_init.py
  ```

---

## 7. Testing
- Submit and view opportunities via the frontend UI.
- API endpoints:
  - `POST /opportunity` (backend)
  - `GET /view_opportunity` (backend)
- Use tools like Postman or curl for API testing.

---

## 8. Deployment Best Practices
- Use strong, unique API keys and secrets.
- Never commit `.env` or database files.
- Use Docker volumes for persistent data.
- Regularly update dependencies and base images.
- For production, consider HTTPS, reverse proxy (e.g., Nginx), and non-root containers.

---

## 9. Stopping and Cleaning Up
```sh
docker-compose down
```

---

## 10. Troubleshooting
- Check logs:
  ```sh
  docker-compose logs backend
  docker-compose logs frontend
  ```
- Ensure ports 8000 and 8001 are free.
- Verify `.env` and database file permissions.

---

## 11. File Structure Overview
```
project-root/
├── backend/
│   ├── main.py
│   ├── db_init.py
│   ├── opportunity.db
│   ├── requirements.txt
│   ├── .env
│   └── Dockerfile
├── frontend/
│   ├── main.py
│   ├── templates/
│   │   └── index.html
│   ├── static/
│   │   └── style.css
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml
├── .gitignore
└── reproducable.md
```

---

## 12. Support
For issues, open an issue in the repository or contact the maintainer.
