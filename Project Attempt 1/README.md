# Data Opportunity Portal

## Objective
Build a lightweight, AI-powered lead qualification platform to help data solutions providers quickly assess new opportunities and generate actionable recommendations using LLMs.

## Primary Outcomes
- Faster lead review
- Better-informed decision-making
- Clear next steps for Sales & PMs
- Standardized understanding of opportunity requirements
- Professional, easy-to-use dashboard experience

## Target Audience
- **Business Users:**
  - Submit new data opportunities
  - View insights for their own submissions
  - Use AI-driven recommendations to approach clients confidently

---

## Features
- **Opportunity Submission:** Users submit new opportunities with all relevant details.
- **Background AI Processing:** LLM generates insights asynchronously.
- **AI-Generated Insights:** Structured, actionable insights for each opportunity.
- **Dashboard:** View opportunities, statuses, and analytics.
- **Authentication:** Basic login for business users.

---

## Project Structure
```
project-root/
├── backend/           # Backend API (FastAPI, SQLite, OpenAI LLM)
│   ├── main.py
│   ├── db_init.py
│   ├── Dockerfile
│   └── ...
├── frontend/          # Frontend (FastAPI + Jinja2)
│   ├── main.py
│   ├── templates/
│   ├── static/
│   └── Dockerfile
├── docker-compose.yml # Multi-container orchestration
├── requirements.txt   # Top-level requirements
└── README.md          # This file
```

---

## Quick Start

### 1. Prerequisites
- [Docker & Docker Compose](https://docs.docker.com/get-docker/)
- (Optional) Python 3.11+ for local development

### 2. Clone the Repository
```sh
git clone https://github.com/himanshujohn/ai-dev-tools-zoomcamp.git
cd "ai-dev-tools-zoomcamp"
cd "Project Attempt 1"
```

### 3. Environment Variables
- Copy `backend/.env.example` to `backend/.env` and set your `OPENAI_API_KEY`.

Example `backend/.env`:
```
OPENAI_API_KEY=sk-...your-key...
```

### 4. Build and Run with Docker Compose
```sh
docker-compose build
docker-compose up -d
```
- Frontend: [http://localhost:8000](http://localhost:8000)
- Backend API: [http://localhost:8001](http://localhost:8001)

### 5. Local Development (Optional)
- **Backend:**
  ```sh
  cd backend
  pip install -r requirements.txt
  uvicorn main:app --reload --port 8001
  ```
- **Frontend:**
  ```sh
  cd frontend
  pip install -r requirements.txt
  uvicorn main:app --reload --port 8000
  ```

### 6. Database Initialization
- The backend auto-creates `opportunity.db` on first run.
- To manually initialize:
  ```sh
  cd backend
  python db_init.py
  ```

### 7. Testing
- Submit and view opportunities via the [frontend UI](frontend/).
- API endpoints:
  - `POST /opportunity` ([backend/main.py](backend/main.py))
  - `GET /view_opportunity` ([backend/main.py](backend/main.py))
- Use Postman or curl for API testing.

### 8. Stopping and Cleaning Up
```sh
docker-compose down
```

---

## Best Practices
- Never commit `.env` or database files.
- Use Docker volumes for persistent data.
- Regularly update dependencies and base images.
- For production: use HTTPS, reverse proxy (e.g., Nginx), and non-root containers.

---

## Troubleshooting
- Check logs:
  ```sh
  docker-compose logs backend
  docker-compose logs frontend
  ```
- Ensure ports 8000 and 8001 are free.
- Verify `.env` and database file permissions.

---

## Support
For issues, open an issue in the repository or contact the maintainer.
