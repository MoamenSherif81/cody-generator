from fastapi import APIRouter, Depends, status

from app.Jobs.GoogleSheetFlush import push_to_google_sheets
from app.schemas.Situation.AcceptSituation import AcceptSituation
from app.schemas.Situation.GenerateSituation import GenerateSituation
from app.schemas.Situation.GetSituation import GetSituation
from app.services.dataset import Generate_Situation, Save_Situation

router = APIRouter(prefix="/dataset", tags=["dataset"])


@router.get(
    "/generate",
    summary="Generate a new situation",
    response_model=GetSituation,
    description=GenerateSituation.get_GenerateSituation_description()
)
async def generate_new_situation(generate_situation: GenerateSituation = Depends()):
    # todo: add the service logic

    situation = await Generate_Situation(generate_situation)
    return situation


@router.post(
    "/accept",
    summary="Send the data of the accepted situation",
    status_code=status.HTTP_201_CREATED,
    description=AcceptSituation.get_AcceptSituation_description()
)
async def accept_situation(acceptSituation: AcceptSituation):
    await Save_Situation(acceptSituation)
    return {"detail": "Accepted situation created successfully"}


@router.post(
    "/flush",
    summary="Push data to google sheets",
    status_code=status.HTTP_200_OK,
)
async def flush_situation():
    push_to_google_sheets()
    return {"detail": "situations Pushed successfully"}
