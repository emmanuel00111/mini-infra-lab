# mini-infra-lab

![CI](https://github.com/<your-username>/mini-infra-lab/actions/workflows/ci.yml/badge.svg)

A small “infrastructure lab” repo to practice DevOps fundamentals with a simple API service.

## Day 1: API + Docker + Compose
### Run locally with Docker Compose
```bash
docker compose up --build
```

## Day 2: Environment Configuration + Request Logging

### Environment configuration
The service now supports environment-based configuration to better mirror real production services.

An example environment file is provided:
```bash
.env.example
```

## Day 4: Metrics (Prometheus)
New endpoint:
- `/metrics` — Prometheus-compatible metrics output

Run:
```bash
docker compose up --build
