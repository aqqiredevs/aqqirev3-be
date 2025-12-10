from fastapi import FastAPI
from app.connection.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from app.connection.database import Base, engine
from contextlib import asynccontextmanager
from app.routes import router

@asynccontextmanager
async def lifespan(_):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
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