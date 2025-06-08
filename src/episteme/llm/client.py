import json
import logging
import requests

from episteme.prompt import PromptBuilder
from pydantic import BaseModel, ValidationError
from typing import Dict, List

logger = logging.getLogger(__name__)


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
        self.prompt = PromptBuilder()
        self.header_type = header_type

    def get_concepts(self, task: str) -> List[str]:
        prompt = self._build_prompt(task)

        for _ in range(self.max_retries):
            raw_response = self._call(prompt)
            parsed = self._parse_response(raw_response)
            print(f"Checking reponse: {parsed}")
            if parsed is not None:
                return parsed

        raise ValueError("Max retries exceeded without valid response")

    def _call(self, prompt: str) -> str:
        logger.debug(f"Sending prompt: {prompt}")
        payload = {"model": self.model_name, "prompt": prompt, "stream": False}
        try:
            response = requests.post(self.api_url, json=payload, timeout=10)
            logger.debug(f"Response code: {response.status_code}")
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.exception(f"LLM Call failed with: {e}")
            return "{}"

    def _parse_response(self, response_json: str) -> List[str] | None:
        try:
            logger.debug(f"Checking response_json: f{response_json}")
            outer = json.loads(response_json)
            inner = outer["response"]
            parsed = ConceptResponse.model_validate_json(inner)
            logger.debug(f"Checking parsing: {parsed}")
            return parsed.concepts
        except (ValidationError, KeyError, json.JSONDecodeError) as e:
            logger.exception(f"Parse error: {e}")
            return None

    def _build_prompt(self, task: str) -> str:
        return self.prompt.build_prompt("task", task)
