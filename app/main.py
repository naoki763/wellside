from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine
from app.models.model import Base
from app.routes.users import user_router

app = FastAPI()

Base.metadata.create_all(bind=engine)


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router=user_router, tags=["users"], prefix="/v1")


@app.get("/")
async def root():
    return {"message": "Hello World"}
