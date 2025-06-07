from .base import PromptTemplate


class TaskPrompt(PromptTemplate):
    def __init__(self, task: str, use_cot: bool = True):
        super().__init__("task_template.jinja")
        self.task = task
        self.use_cot = use_cot

    def build_context(self):
        return {
            "header": "You are a concept-mapping agent.",
            "few_shot_examples": """Task: machine learning\nResponse: {"concepts": ["probability", "linear algebra"]}""",
            "instructions": 'Return only valid JSON: {"concepts": ["..."]}. No explanations or markdown.',
            "cot_scaffold": "Think step by step about what concepts are foundational."
            if self.use_cot
            else "",
            "task": self.task,
        }
