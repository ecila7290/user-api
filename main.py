import uvicorn
from fastapi import FastAPI

from app.common.database import Base, engine
from app.common.config import settings
from app.users.routers import user

app = FastAPI(title="FastAPI User API", docs_url=f"{settings.API_V1}/docs")

Base.metadata.create_all(bind=engine)

app.include_router(user.router, prefix=f"{settings.API_V1}/users", tags=["Users"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
