
FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN pip install uv && uv sync --frozen --no-dev

COPY ./dashboard /app/dashboard

EXPOSE 8501

CMD ["uv", "run", "streamlit", "run", "dashboard/app.py", "--server.address=0.0.0.0"]
