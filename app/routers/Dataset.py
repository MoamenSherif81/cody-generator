from fastapi import APIRouter, Depends
from app.schemas.Situation.GenerateSituation import GenerateSituation
from app.schemas.Situation.GetSituation import GetSituation

router = APIRouter(prefix="/dataset", tags=["dataset"])

@router.get(
    "/generate",
    summary="Generate a new situation",
    response_model=GetSituation,
    description=GenerateSituation.get_GenerateSituation_description()
)
async def generate_new_situation(generate_situation: GenerateSituation = Depends()):
    # todo: add the service logic
    situation = GetSituation()
    return situation

