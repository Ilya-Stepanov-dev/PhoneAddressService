FROM python:3.12-slim

WORKDIR /app

# Кладём uv в образ
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Копируем файлы для зависимостей
COPY pyproject.toml uv.lock /app

# Создаём venv и ставим зависимости
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Копируем остальной код
COPY . /app

EXPOSE 8000

# uvicorn из .venv
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
