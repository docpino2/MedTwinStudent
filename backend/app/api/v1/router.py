from fastapi import APIRouter

from app.api.v1 import ai_health, cases, curriculum, reasoning, simulation, students, tutor

api_router = APIRouter()
api_router.include_router(students.router, prefix="/students", tags=["students"])
api_router.include_router(curriculum.router, prefix="/curriculum", tags=["curriculum"])
api_router.include_router(cases.router, prefix="/cases", tags=["clinical cases"])
api_router.include_router(reasoning.router, prefix="/reasoning", tags=["reasoning"])
api_router.include_router(tutor.router, prefix="/tutor", tags=["socratic tutor"])
api_router.include_router(simulation.router, prefix="/simulation", tags=["learning simulation"])
api_router.include_router(ai_health.router, prefix="/ai-health", tags=["competencias IA/Salud Digital"])
