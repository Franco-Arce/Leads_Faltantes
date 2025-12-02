import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.routers import api

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("api.log"),
        logging.StreamHandler()
    ]
)

settings = get_settings()

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting up Zoom Data API...")
    # Pre-load data on startup
    from app.services.data_loader import data_loader
    data_loader.load_data()
    yield
    logging.info("Shutting down Zoom Data API...")

app = FastAPI(
    title=settings.APP_NAME,
    description="API para exponer datos de asistencia de Zoom",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
