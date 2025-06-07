from abc import ABC, abstractmethod
from jinja2 import Environment, FileSystemLoader
import os

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")


class PromptTemplate(ABC):
    def __init__(self, template_file: str):
        env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
        self.template = env.get_template(template_file)

    @abstractmethod
    def build_context(self) -> dict:
        pass

    def build_prompt(self) -> str:
        return self.template.render(self.build_context())
