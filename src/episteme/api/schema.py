from pydantic import BaseModel, Field
from typing import Literal, Union, Annotated

class NodeBase(BaseModel):
    id: int
    name: str
    status: Literal["in-progress", "complete", "not started"] = "not started"
    note: str | None = None
    added_by: Literal["user", "llm"] = "user" #to track data provinance

class Goal(NodeBase):
    type: Annotated[Literal["goal"], Field(const=True, default="goal")]

class Task(NodeBase):
    type: Annotated[Literal["task"], Field(const=True, default="task")]

class Concept(NodeBase):
    type: Annotated[Literal["concept"],Field(const=True, default="concept")]


Node = Union[Goal, Task, Concept]

class EdgeCreate(BaseModel):
    source_id: int
    target_id: int
    relation: Literal["requires", "decomposes_to", "teaches"]
