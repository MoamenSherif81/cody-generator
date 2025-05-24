from fastapi import APIRouter, Depends, status

from app.schemas.Situation.AcceptSituation import AcceptSituation
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


@router.post(
    "/accept",
    summary="Send the data of the accepted situation",
    status_code=status.HTTP_201_CREATED,
    description=AcceptSituation.get_AcceptSituation_description()
)
async def accept_situation(acceptSituation: AcceptSituation):
    # todo: add service logic
    return {"detail": "Accepted situation created successfully"}
