from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config.database import engine, Base
from app.routers import user, project, record, dsl, Dataset
from app.Jobs.GoogleSheetFlush import start_scheduler

app = FastAPI(title="Cody-generator BackEnd")

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



@app.on_event("startup")
async def startup_event():
    print("^^" * 100)
    print("Background job started!")
    print("^^" * 100)
    # Start the scheduler for background jobs
    global scheduler
    scheduler = start_scheduler()

@app.on_event("shutdown")
async def shutdown_event():
    print("^^" * 100)
    scheduler.shutdown()  # Properly shut down the scheduler when FastAPI shuts down
    print("Background job stopped.")
    print("^^" * 100)

@app.get("/", summary="Root endpoint", description="Welcome message for the Code Generator API")
def read_root():
    return {"message": "What the Fuck are u doing here it's root !"}

