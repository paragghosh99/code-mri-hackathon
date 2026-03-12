# What just happened when you run the app:
# models is imported
# Task is registered with Base
# create_all() walks the registry
# SQLite file tasks.db is created
# Table tasks is created (if not already present)
# This runs once.
# Future runs see the table and do nothing.

from fastapi import FastAPI, Request
from app.database import engine
from app import models
from .routes import router
import logging
import time
from fastapi.responses import JSONResponse

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger("task_app")

app = FastAPI()

logger.info("🚀 Task App starting up")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    logger.info(f"➡️  Incoming request: {request.method} {request.url.path}")

    response = await call_next(request)

    duration = time.time() - start_time

    logger.info(
        f"⬅️  Completed request: {request.method} {request.url.path} "
        f"Status={response.status_code} Duration={duration:.3f}s"
    )

    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(
        f"🔥 Unhandled exception on {request.method} {request.url.path}",
        exc_info=True
    )

    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"}
    )


# Create tables at startup
models.Base.metadata.create_all(bind=engine)

@app.get("/ping")
def ping():
    return {"status": "ok"}

# @app.get("/crash")
# def crash():
#     logger.info("💥 Crash endpoint called")
#     raise RuntimeError("Intentional crash for logging test")

app.include_router(router)