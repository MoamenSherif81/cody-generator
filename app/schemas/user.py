from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    username: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: str | None = None
    username: str | None = None
    password: str | None = None


class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    username: str
    password: str
