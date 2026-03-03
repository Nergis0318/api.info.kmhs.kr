FROM ghcr.io/astral-sh/uv:alpine

WORKDIR /app

COPY . .

RUN uv sync --frozen --no-cache

EXPOSE 8000

ENTRYPOINT ["uv", "run", "hypercorn", "main:app", "--bind", "0.0.0.0:8000", "-w", "1"]
