from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

import api
from models.tables import Base
from settings import exception_handler, settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await settings.db.init_db(Base)
    yield
    await settings.db.close()


if not settings.debug:
    app = FastAPI(openapi_url=None, redoc_url=None, docs_url=None, lifespan=lifespan)
else:
    app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def general_exception_handler(*args):
    return await exception_handler(*args)


app.include_router(api.api_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
