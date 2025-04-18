from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config.database import engine, Base
from app.routers import user, project, record, dsl

app = FastAPI(title="Cody-generator BackEnd")

app.openapi_extra = {"security": [{"BearerAuth": []}]}

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Create database tables
Base.metadata.create_all(bind=engine)

app.include_router(user.router)
app.include_router(project.router)
app.include_router(record.router)
app.include_router(dsl.router)


@app.get("/", summary="Root endpoint", description="Welcome message for the Code Generator API")
def read_root():
    return {"message": "Welcome to Code Generator API"}
