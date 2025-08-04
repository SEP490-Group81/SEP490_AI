import os
import logging
import uvicorn
from typing import List

from google.adk.cli.fast_api import get_fast_api_app
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware

# --- Cấu hình logging đơn giản ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

def parse_origins(origins_env: str | None) -> List[str]:
    if not origins_env:
        return []
    return [o.strip() for o in origins_env.split(",") if o.strip()]

def main():
    agent_dir = os.environ.get("AGENT_PATH", "./your_agent")
    session_db_uri = os.environ.get("SESSION_DB_URL", "sqlite:///./sessions.db")

    # CORS origins có thể tùy chỉnh qua env, mặc định cho localhost:3000 và 127.0.0.1:3000
    allow_origins = parse_origins(os.environ.get("CORS_ALLOW_ORIGINS"))
    if not allow_origins:
        allow_origins = ["http://localhost:3000", "http://127.0.0.1:3000"]

    port = int(os.environ.get("PORT", "8080"))

    logger.info("Starting ADK API server")
    logger.info("Agent directory: %s", agent_dir)
    logger.info("Session DB URI: %s", session_db_uri)
    logger.info("Allowed CORS origins: %s", allow_origins)

    # Tạo FastAPI app từ ADK với session persist và CORS cơ bản
    app = get_fast_api_app(
        agents_dir=agent_dir,
        session_service_uri=session_db_uri,
        allow_origins=allow_origins,
        web=False,
    )

    # Bổ sung middleware CORS để bật credentials hoặc tuỳ chỉnh chi tiết hơn
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


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
    
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
