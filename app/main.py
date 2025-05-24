from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config.database import engine, Base
from app.routers import user, project, record, dsl, Dataset

# Load once at startup
# from app.services.shared_ai_state import model, sampler

app = FastAPI(title="Cody-generator BackEnd")

app.openapi_extra = {"security": [{"BearerAuth": []}]}

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Create database tables
Base.metadata.create_all(bind=engine)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user.router)
app.include_router(project.router)
app.include_router(record.router)
app.include_router(dsl.router)
app.include_router(Dataset.router)


@app.get("/", summary="Root endpoint", description="Welcome message for the Code Generator API")
def read_root():
    return {"message": "What the Fuck are u doing here it's root !"}
