from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import uuid


class Population(BaseModel):
    population_id: uuid.UUID
    name: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class DataItem(BaseModel):
    id: uuid.UUID
    agent_id: uuid.UUID
    data_type: str
    content: Any
    created_at: datetime
    updated_at: datetime


class Agent(BaseModel):
    agent_id: uuid.UUID
    name: str
    population_id: Optional[uuid.UUID] = None
    created_at: datetime
    updated_at: datetime
    data_items: List[DataItem] = Field(default_factory=list)

class CreatePopulationPayload(BaseModel):
    name: str
    description: Optional[str] = None


class CreateAgentPayload(BaseModel):
    name: str
    population_id: Optional[uuid.UUID] = None
    agent_data: Optional[List[Dict[str, Any]]] = None # For initial data items


class CreateDataItemPayload(BaseModel):
    data_type: str
    content: Any


class UpdateDataItemPayload(BaseModel):
    content: Any


class DeletionResponse(BaseModel):
    message: str


# --- LLM Generation Models ---

class QualGenerationRequest(BaseModel):
    question: str

class QualGenerationResponse(BaseModel):
    agent_id: uuid.UUID
    question: str
    answer: str

class MCGenerationRequest(BaseModel):
    question: str
    options: List[str]

class MCGenerationResponse(BaseModel):
    agent_id: uuid.UUID
    question: str
    options: List[str]
    chosen_option: str
