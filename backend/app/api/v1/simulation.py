from fastapi import APIRouter

from app.schemas.simulation import LearningSimulationResponse, SimulationRequest
from app.services.learning_simulation_engine import LearningSimulationEngine

router = APIRouter()
engine = LearningSimulationEngine()


@router.post("/simulate", response_model=LearningSimulationResponse)
def simulate_learning(request: SimulationRequest) -> LearningSimulationResponse:
    return engine.simulate(request)

