import logging

from fastapi import FastAPI

from appscheduler.scheduler import start_scheduler, stop_scheduler
from infra.database.database import Base, engine
from routes.categories_router import router as categories_router
from routes.exports_router import router as exports_router
from routes.imports_router import router as imports_router
from routes.processings_router import router as processing_router
from routes.productions_router import router as productions_router
from routes.sales_router import router as sales_router
from routes.scrping_router import router as scraping_router
from routes.users_router import router as users_router

# SQLAlchemy create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users_router)
app.include_router(productions_router)
app.include_router(processing_router)
app.include_router(categories_router)
app.include_router(scraping_router)
app.include_router(sales_router)
app.include_router(exports_router)
app.include_router(imports_router)

# Enabling caching module

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.get("/")
async def root():
    return {
        "FIAP": {
            "success": True,
            "tech_challenge": "Phase 1",
            "team": "Sombra-MLET2"
        }
    }


@app.get("/stop_scheduler")
async def stop_tasks_scheduler():
    stop_scheduler()
    return {"message": "scheduler is stop"}


@app.on_event("startup")
async def startup_event():
    start_scheduler()
    

@app.on_event("shutdown")
def shutdown_event():
    stop_scheduler()
    