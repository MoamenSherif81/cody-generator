from fastapi import APIRouter, Depends
from Backend.app.services.dsl_service import compile_dsl
from Backend.app.dependencies.auth import get_current_user
from Backend.app.models.user import User

router = APIRouter(prefix="/dsl", tags=["dsl"])

@router.post("/")
def compile_dsl_endpoint(dsl: str, platform: str, current_user: User = Depends(get_current_user)):
    result = compile_dsl(dsl, platform)
    return result