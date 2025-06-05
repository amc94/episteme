import requests

from pydantic import BaseModel, ValidationError
from typing import Dict, List

from .template import build_prompt

class ConceptResponse(BaseModel):
    concepts: List[str]


class Client:
    def __init__(
        self,
        model_name: str = "llama3",
        header_type: str = "default",
        max_retries: int = 5,
        api_url: str = "http://localhost:11434/api/generate",
    ):
        self.model_name = model_name
        self.max_retries = max_retries
        self.api_url = api_url

        try:
            build_prompt("dummy", header_type)
        except ValueError:
            raise ValueError("Invalid header type")

        self.header_type = header_type

    def get_concepts(self, task: str) -> List[str]:
        if len(task) > 200:
            raise ValueError()
        prompt = self._build_prompt(task)

        for _ in range(self.max_retries):
            raw_response = self._call(prompt)
            parsed = self._parse_response(raw_response)
            print(f"Checking reponse: {parsed}")
            if parsed is not None:
                return parsed

        raise ValueError("Max retries exceeded without valid response")

    def _call(self, prompt: str) -> str:
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }
        try:
            response = requests.post(self.api_url, json=payload, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            return "{}"

    def _parse_response(self, response_json: str) -> List[str] | None:
        try:
            print(f"Checking response_json: f{response_json}")
            parsed = ConceptResponse.model_validate_json(response_json)
            print(f"Checking parsing: {parsed}")
            return parsed.concepts
        except ValidationError:
            return None

    def _build_prompt(self, task: str) -> str:
        return build_prompt(task, self.header_type)