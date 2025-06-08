from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class ReflectionLog:
    concept_id: int
    date: datetime = datetime.now()
    notes: Optional[str] = ""
