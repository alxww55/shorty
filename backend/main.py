from collections.abc import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from loguru import logger
from pydantic import ValidationError

from backend.messaging import broker

from .config import settings
from .routes import frontend_router, url_router

logger.add(
    sink=settings.logging_config.log_file_path,
    rotation=settings.logging_config.rotation,
    format=settings.logging_config.format,
    level="INFO",
)

templates = Jinja2Templates(directory="./frontend/templates")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    if not broker.is_worker_process:
        await broker.startup()
        logger.info("Broker startup successfully")
    yield
    if not broker.is_worker_process:
        logger.info("Broker shutdown successfully")
        await broker.shutdown()


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    docs_url="/docs" if settings.debug else None,
)

app.include_router(url_router)
app.include_router(frontend_router)
app.mount("/static", StaticFiles(directory="./frontend/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(ValidationError)
async def pydantic_validation_exception_handler(
    request: Request, exc: ValidationError
):
    errors = [err["msg"].split(",")[1::] for err in exc.errors()]
    logger.error(
        "Received following error(s) from API: {errors}, 422", errors=errors
    )
    return JSONResponse(
        status_code=422,
        content={"detail": errors},
    )


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    logger.error("Requested ressource was not found, 404")
    return templates.TemplateResponse(
        "404.html", {"request": request}, status_code=exc.status_code
    )
