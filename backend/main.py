
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import ValidationError

from .config import settings
from .routes import frontend_router, url_router


def check_docs_availability():
    return "/docs" if settings.debug else None


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    docs_url=check_docs_availability(),
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
    return JSONResponse(
        status_code=422,
        content={"detail": errors},
    )
