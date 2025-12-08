FROM python:3.11-slim
WORKDIR /app
COPY backend/pyproject.toml .        
RUN pip install --upgrade pip && pip install uv
RUN uv sync
COPY backend/ .                       
ENV PYTHONUNBUFFERED=1
ENV DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/postgres
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]