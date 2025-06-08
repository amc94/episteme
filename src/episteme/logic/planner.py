from episteme.llm import Client
from episteme.models import Concept
from typing import List

class Planner:
    def __init__(self, client=None):
        self.client = client or Client()

    def add_task(self, task: str) -> List[Concept]:
        concepts = self.client.get_concepts(task)
        return [Concept(concept) for concept in concepts]
