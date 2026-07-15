from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import interaction
from db import Base, engine
import models  # noqa: F401  -- ensures models are registered with Base before create_all

Base.metadata.create_all(bind=engine)  # creates crm.db + tables on first run

app = FastAPI(title="AI-First CRM - HCP Module")

# Allow the React dev server (localhost:3000) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(interaction.router)


@app.get("/")
def home():
    return {"message": "Backend running"}
