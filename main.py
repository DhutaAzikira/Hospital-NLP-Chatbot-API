from contextlib import asynccontextmanager

from fastapi import FastAPI
from routes import DatabaseRouter, ChatbotRouter


# === App Initialization ===
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    print("Application startup")

    yield

    # Shutdown logic
    print("Application shutdown")

app = FastAPI(lifespan=lifespan)

app.include_router(DatabaseRouter.router)
app.include_router(ChatbotRouter.router)

@app.get("/")
async def root():
    return {"message": "MainEntry"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
