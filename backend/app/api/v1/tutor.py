from fastapi import APIRouter

from app.schemas.tutor import TutorTurnRequest, TutorTurnResponse
from app.services.socratic_tutor import SocraticTutorAgent

router = APIRouter()
agent = SocraticTutorAgent()


@router.post("/turn", response_model=TutorTurnResponse)
def create_tutor_turn(request: TutorTurnRequest) -> TutorTurnResponse:
    return agent.generate_turn(request)

