https://capstone-project-user-production.up.railway.app/import logging
from functools import lru_cache
from typing import List

from pydantic import ConfigDict
from pydantic_settings import BaseSettings
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from fastapi import Request
import traceback
from google.adk.cli.fast_api import get_fast_api_app


class Settings(BaseSettings):
    AGENT_PATH: str = "./hospital_booking_agent"
    SESSION_DB_URL: str = "sqlite:///./sessions.db"
    CORS_ALLOW_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000,http://localhost:8080,http://127.0.0.1:8080,https://capstone-project-user-production.up.railway.app:3000"
    PORT: int = 8080
    ENV: str = "development"
    ENABLE_DOCS: bool = True

    # Bỏ qua các biến môi trường không được định nghĩa trong model
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings()


def parse_origins(value: str) -> List[str]:
    return [o.strip() for o in value.split(",") if o.strip()]


def create_app(settings: Settings) -> FastAPI:
    cors_list = parse_origins(settings.CORS_ALLOW_ORIGINS)
    if settings.ENV == "production" and "*" in cors_list:
        raise RuntimeError("Không cho phép '*' trong CORS khi credentials=True")

    # Tạo app từ ADK
    app = get_fast_api_app(
        agents_dir=settings.AGENT_PATH,
        session_service_uri=settings.SESSION_DB_URL,
        allow_origins=cors_list,
        web=False,
    )

    @app.exception_handler(Exception)
    async def all_exception_handler(request: Request, exc: Exception):
        # Lấy message và full stack trace (tuỳ chọn)
        tb = traceback.format_exc()
        return JSONResponse(
            status_code=500,
            content={
                "detail": str(exc),
                "trace": tb.splitlines()
            },
        )

    # Cấu hình CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Chỉ hiển thị docs khi không phải production hoặc ENABLE_DOCS=True
    if settings.ENV != "production" or settings.ENABLE_DOCS:
        @app.get("/openapi.json", include_in_schema=False)
        def openapi_schema():
            return get_openapi(
                title="ADK Agent API",
                version="1.0.0",
                routes=app.routes
            )

        @app.get("/docs", include_in_schema=False)
        def swagger_ui():
            return get_swagger_ui_html(
                openapi_url="/openapi.json",
                title="ADK Agent Swagger UI"
            )

        @app.get("/redoc", include_in_schema=False)
        def redoc_ui():
            return get_redoc_html(
                openapi_url="/openapi.json",
                title="ADK Agent ReDoc"
            )

    # Health check endpoint
    @app.get("/health", include_in_schema=False)
    def health():
        return {"status": "ok", "env": settings.ENV}

    return app


def main():
    # Thiết lập logging cơ bản
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s"
    )
    logger = logging.getLogger("adk_api")

    # Load cấu hình
    settings = get_settings()
    logger.info("Starting ADK API — env=%s, CORS=%s", settings.ENV, settings.CORS_ALLOW_ORIGINS)

    # Tạo FastAPI app
    app = create_app(settings)

    uvicorn.run(app, host="localhost", port=settings.PORT)

if __name__ == "__main__":
    main()