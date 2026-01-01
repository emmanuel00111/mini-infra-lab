import logging
import time
import uuid
from datetime import datetime
from fastapi import FastAPI, Request
from settings import settings
from starlette.responses import Response
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST


# Basic logger setup
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(settings.app_name)

app = FastAPI(title=settings.app_name)
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "path", "status"],
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency (seconds)",
    ["method", "path"],
)

IN_PROGRESS = Gauge(
    "http_requests_in_progress",
    "Number of HTTP requests in progress",
)


@app.middleware("http")
async def request_logger(request: Request, call_next):
    request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
    start = time.perf_counter()

    method = request.method
    path = request.url.path

    IN_PROGRESS.inc()
    try:
        response: Response = await call_next(request)
    finally:
        IN_PROGRESS.dec()

    duration_ms = (time.perf_counter() - start) * 1000
    duration_s = duration_ms / 1000.0

    # Log request
    logger.info(
        "request",
        extra={
            "request_id": request_id,
            "method": method,
            "path": path,
            "status_code": response.status_code,
            "duration_ms": round(duration_ms, 2),
        },
    )

    # Metrics
    REQUEST_COUNT.labels(method=method, path=path, status=str(response.status_code)).inc()
    REQUEST_LATENCY.labels(method=method, path=path).observe(duration_s)

    response.headers["x-request-id"] = request_id
    return response



@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": settings.app_name,
        "env": settings.app_env,
        "time": datetime.utcnow().isoformat() + "Z",
    }

@app.get("/")
def root():
    return {"message": f"{settings.app_name} is running", "env": settings.app_env}

@app.get("/config")
def config():
    # safe to expose only non-sensitive config
    return {
        "app_name": settings.app_name,
        "app_env": settings.app_env,
        "log_level": settings.log_level,
        "include_timing": settings.include_timing,
    }

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
