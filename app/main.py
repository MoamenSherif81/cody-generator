import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from google.api_core.exceptions import BadRequest

from app.Jobs.GoogleSheetFlush import start_scheduler, push_to_google_sheets
from app.config.database import engine, Base
from app.routers import user, project, record, dsl, Dataset, message

app = FastAPI(title="Cody-generator BackEnd")


@app.exception_handler(BadRequest)
async def bad_request_handler(request: Request, exc: BadRequest):
    return JSONResponse(
        status_code=400,
        content={"error": exc.message}
    )


app.openapi_extra = {"security": [{"BearerAuth": []}]}

# Mount static files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Create database tables
Base.metadata.create_all(bind=engine)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user.router)
app.include_router(project.router)
app.include_router(record.router)
app.include_router(dsl.router)
app.include_router(Dataset.router)
app.include_router(message.router)


@app.on_event("startup")
async def startup_event():
    print("Background job started!")
    global scheduler
    scheduler = start_scheduler()


@app.on_event("shutdown")
async def shutdown_event():
    push_to_google_sheets()
    scheduler.shutdown()
    print("Background job stopped.")


@app.get("/", summary="Root endpoint", description="Welcome message for the Code Generator API")
def read_root():
    return {"message": "What the Fuck are u doing here it's root !"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)
