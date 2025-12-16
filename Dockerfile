FROM python:3.13-alpine
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY . /smallproxy

WORKDIR /smallproxy
RUN uv sync
EXPOSE 8000
CMD ["uv", "run", "uvicorn", "--host", "0.0.0.0", "app.main:app"]
