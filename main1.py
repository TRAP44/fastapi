from fastapi import FastAPI
from db.connect import init_db
from contextlib import asynccontextmanager
from routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    #print("App is starting up")
    await init_db()
    yield
    #print("App is shutting down")

app = FastAPI(lifespan=lifespan)

app.include_router(router)