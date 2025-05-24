from fastapi import APIRouter

from app.schemas.Situation.GenerateSituation import GenerateSituation
from app.schemas.Situation.GetSituation import GetSituation

router = APIRouter(prefix="/dataset", tags=["dataset"])


@router.post(
    "/generate",  # use POST for creation
    summary="Generate a new situation",
    response_model=GetSituation,
    description=GenerateSituation.get_GenerateSituation_description()
)
async def generate_new_situation(generate_situation: GenerateSituation):
    # todo: add the service logic
    situation = GetSituation()
    return situation
