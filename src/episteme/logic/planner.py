from episteme.llm import Client
from typing import List


class Planner:
    def __init__(self, client=None):
        self.client = client or Client()

    def add_task(self, task: str) -> List[str]:
        return self.client.get_concepts(task)
