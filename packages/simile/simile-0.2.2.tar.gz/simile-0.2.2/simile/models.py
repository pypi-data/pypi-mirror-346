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


class InitialDataItemPayload(BaseModel):
    data_type: str
    content: Any


class CreateAgentPayload(BaseModel):
    name: str
    population_id: Optional[uuid.UUID] = None
    agent_data: Optional[List[InitialDataItemPayload]] = None


class CreateDataItemPayload(BaseModel):
    data_type: str
    content: Any


class UpdateDataItemPayload(BaseModel):
    content: Any


class DeletionResponse(BaseModel):
    message: str


# --- Generation Operation Models ---
class QualGenerationRequest(BaseModel):
    question: str

class QualGenerationResponse(BaseModel):
    question: str
    answer: str

class MCGenerationRequest(BaseModel):
    question: str
    options: List[str]

class MCGenerationResponse(BaseModel):
    question: str
    options: List[str]
    chosen_option: str


# --- Survey Session Models ---
class ConversationTurn(BaseModel):
    type: str # "qual" or "mc"
    question: str
    options: Optional[List[str]] = None
    answer: Optional[str] = None
    chosen_option: Optional[str] = None
    timestamp: datetime

class SurveySessionCreateResponse(BaseModel):
    id: uuid.UUID # Session ID
    agent_id: uuid.UUID
    created_at: datetime
    status: str
    
class SurveySessionCloseResponse(BaseModel):
    id: uuid.UUID # Session ID
    status: str 
    updated_at: datetime 
    message: Optional[str] = None