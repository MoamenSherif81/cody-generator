from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from Backend.app.routers import user, project, record, dsl
from Backend.app.config.database import engine, Base

app = FastAPI(
    title="Code Generator API",
    description="A backend API for a code generator that converts GUI screenshots to DSL and compiles DSL to platform-specific code. Features user management, project management, record handling, and DSL compilation with AI integration.",
    version="1.0.0",
    contact={
        "name": "Your Name",
        "email": "your.email@example.com",
        "url": "https://yourwebsite.com"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    },
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {"name": "Users", "description": "Operations related to user management and authentication"},
        {"name": "Projects", "description": "Operations for managing projects"},
        {"name": "Records", "description": "Operations for managing records (screenshots/DSL)"},
        {"name": "DSL", "description": "Operations for compiling DSL to platform-specific code"}
    ]
)

# Define security scheme for JWT Bearer token
app.openapi_extra = {
    "components": {
        "securitySchemes": {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": "Enter 'Bearer <JWT>' where <JWT> is the token obtained from POST /users/token"
            }
        }
    },
    "security": [{"BearerAuth": []}]
}

# Mount static files directory
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(user.router)
app.include_router(project.router)
app.include_router(record.router)
app.include_router(dsl.router)

@app.get("/", summary="Root endpoint", description="Welcome message for the Code Generator API")
def read_root():
    return {"message": "Welcome to Code Generator API"}