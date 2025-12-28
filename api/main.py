import logging
import time
import uuid
from datetime import datetime
from fastapi import FastAPI, Request, Response
from settings import settings

# Basic logger setup
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(settings.app_name)

app = FastAPI(title=settings.app_name)

@app.middleware("http")
async def request_logger(request: Request, call_next):
    request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
    start = time.perf_counter()

    # Run request
    response: Response = await call_next(request)

    duration_ms = (time.perf_counter() - start) * 1000
    logger.info(
        "request",
        extra={
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": round(duration_ms, 2),
        },
    )

    # Return request id to client too
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
