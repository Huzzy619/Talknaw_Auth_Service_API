import uvicorn

from app.core.config import settings


def main() -> None:
    """Entrypoint of the application."""
    if settings.debug: #? development
        uvicorn.run(
            "app.core.application:get_app",
            host=settings.host,
            port=settings.port,
            reload=True,
            factory=True,
        )
    
    else: #? production
        uvicorn.run(
            "app.core.application:get_app",
            workers=settings.workers_count,
            port=settings.port,
        )


if __name__ == "__main__":
    main()
