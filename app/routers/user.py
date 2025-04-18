from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse, LoginRequest
from app.dependencies.auth import get_current_user, get_password_hash, authenticate_user, create_access_token
from app.config.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/token",
    summary="Login to get JWT token",
    description="Authenticate with username and password to receive a JWT token. In Swagger UI, copy the 'access_token' and enter it as 'Bearer <token>' in the Authorize dialog (under BearerAuth).",
    response_description="A JSON object containing the JWT token and token type."
)
async def login_for_access_token(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post(
    "/",
    response_model=UserResponse,
    summary="Create a new user",
    description="Register a new user with name, username, and password. No authentication required.",
    response_description="The created user object."
)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    db_user = User(name=user.name, username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user",
    description="Retrieve details of the currently authenticated user. Requires a valid JWT token in the Authorization header (Bearer <token>), entered via the Swagger UI Authorize dialog (BearerAuth).",
    response_description="The current user object."
)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user

@router.put(
    "/me",
    response_model=UserResponse,
    summary="Update current user details",
    description="Update your name, username, or password. Requires a valid JWT token in the Authorization header (Bearer <token>), entered via the Swagger UI Authorize dialog (BearerAuth).",
    response_description="The updated user object."
)
def update_current_user(
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_user = db.query(User).filter(User.id == current_user.id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if user.username:
        existing_user = db.query(User).filter(User.username == user.username, User.id != current_user.id).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")
        db_user.username = user.username

    if user.name:
        db_user.name = user.name
    if user.password:
        db_user.hashed_password = get_password_hash(user.password)

    db.commit()
    db.refresh(db_user)
    return db_user
