from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .config import settings
from .database import db_helper
from .models.base_model import Base
from .routes import frontend_router, url_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield


def check_docs_availability():
    return "/docs" if settings.debug else None


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan,
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
