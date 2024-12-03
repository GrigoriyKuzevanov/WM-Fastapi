import uvicorn
from fastapi import FastAPI

from api import api_router
from core.config import settings
from core.lifespan import lifespan

app = FastAPI(
    lifespan=lifespan,
)
app.include_router(
    api_router,
    prefix=settings.api.prefix,
)


if __name__ == "__main__":
    uvicorn.run(
        app=settings.run.app,
        host=settings.run.host,
        port=settings.run.port,
        reload=settings.run.reload,
    )
