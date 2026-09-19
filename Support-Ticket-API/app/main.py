from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app import models
from app.routes.tickets import router as ticket_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Support Ticket API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(ticket_router)


@app.get("/")
def root():
    return {"message": "Support Ticket API is running"}