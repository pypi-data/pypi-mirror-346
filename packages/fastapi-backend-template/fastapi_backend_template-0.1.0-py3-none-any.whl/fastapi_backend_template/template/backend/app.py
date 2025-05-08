import uvicorn

from src.config.manager import settings

if __name__ == "__main__":
    """
    Main entry point to start the API server from project root directory
    
    Example:
        $ cd backend
        $ python app.py
    """
    uvicorn.run(
        app="src.main:backend_app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.DEBUG,
        workers=settings.SERVER_WORKERS,
        log_level=settings.LOGGING_LEVEL,
    ) 