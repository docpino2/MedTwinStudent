from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.api.v1.auth import router as auth_router
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    if settings.init_db_on_startup:
        from app.db_init import main as initialize_database

        initialize_database()
    from app.db_init import ensure_postgraduate_profile

    ensure_postgraduate_profile()
    from app.core.database import engine
    from app.services.auth_service import initialize_auth

    initialize_auth(engine)
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description="Digital twin MVP for medical student learning simulation.",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_origin_regex=settings.backend_cors_origin_regex,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix="/api/v1")
    app.include_router(auth_router, prefix="/api/v1/auth", tags=["acceso"])

    @app.exception_handler(RequestValidationError)
    async def validation_error(request, exc: RequestValidationError):
        # Validation responses must not reflect passwords or other submitted evidence.
        return JSONResponse(status_code=422, content={"detail": "Revisa los campos enviados.", "fields": [list(error["loc"]) for error in exc.errors()]})

    @app.get("/health", tags=["health"])
    def health_check() -> dict[str, str]:
        return {"status": "ok", "service": settings.app_name}

    return app


app = create_app()
