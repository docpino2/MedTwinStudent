from fastapi import APIRouter

from app.schemas.curriculum import CurriculumConcept, CurriculumGraph
from app.services.seed_repository import get_seed_concepts

router = APIRouter()


@router.get("/concepts", response_model=list[CurriculumConcept])
def list_concepts() -> list[CurriculumConcept]:
    return get_seed_concepts()


@router.get("/graph", response_model=CurriculumGraph)
def get_graph() -> CurriculumGraph:
    concepts = get_seed_concepts()
    edges = []
    for concept in concepts:
        for prerequisite in concept.prerequisites:
            edges.append((prerequisite, concept.id, "prerequisite_for"))
    return CurriculumGraph(concepts=concepts, edges=edges)

