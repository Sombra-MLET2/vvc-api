import logging
from typing import Annotated
from fastapi import FastAPI, Depends
from infra.database.database import Base, engine
from infra.security.security import get_current_active_user
from routes.categories_router import router as categories_router
from routes.processings_router import router as processing_router
from routes.productions_router import router as productions_router
from routes.users_router import router as users_router
from routes.scrping_router import router as scraping_router
from ucs.user.dtos import User

# SQLAlchemy create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users_router)
app.include_router(productions_router)
app.include_router(processing_router)
app.include_router(categories_router)
app.include_router(scraping_router)

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


@app.get("/protected")
async def protected(current_user: Annotated[User, Depends(get_current_active_user)]):
    return {"protected": True}
