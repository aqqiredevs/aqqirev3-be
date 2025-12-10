from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.routes import router
from app.connection import init_models

@asynccontextmanager
async def lifespan(_):
    await init_models()
    print("[*] Tables ensured on startup")
    yield

app = FastAPI(lifespan=lifespan)

@app.middleware("http")
async def log_headers(request, call_next):
    print("AUTH HEADER RECEIVED:", request.headers.get("authorization"))
    response = await call_next(request)
    return response

allow_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)