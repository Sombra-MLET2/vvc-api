import logging
from typing import Annotated

from fastapi import FastAPI, Depends

from infra.security.security import get_current_active_user
from routes.users_router import router
from infra.database.database import Base, engine
from ucs.user.dtos import User

# SQLAlchemy create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)

# Enabling caching module
import infra.cache.caching

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.get("/")
async def root():
    return {
        "FIAP": {
            "succes": True,
            "tech_challenge": "Phase 1",
            "team": "Sombra-MLET2"
        }
    }

@app.get("/protected")
async def protected(current_user: Annotated[User, Depends(get_current_active_user)]):
    return { "protected": True }