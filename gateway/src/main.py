from contextlib import asynccontextmanager

import uvicorn
from api import routers
from config import settings
from database import sessionmanager
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    """
    yield
    if sessionmanager._engine is not None:
        # Close the DB connection
        await sessionmanager.close()


app = FastAPI(lifespan=lifespan, title=settings.project_name, docs_url="/docs")


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Routers
app.include_router(routers.user_router)
app.include_router(routers.auth_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.me_host, reload=True, port=settings.me_port)
