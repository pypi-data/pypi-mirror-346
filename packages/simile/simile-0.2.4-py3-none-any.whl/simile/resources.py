import uuid
from typing import TYPE_CHECKING, List

from .models import (
    QualGenerationRequest,
    QualGenerationResponse,
    MCGenerationRequest,
    MCGenerationResponse,
    SurveySessionCloseResponse
)

if TYPE_CHECKING:
    from .client import Simile

class Agent:
    """Represents an agent and provides methods for interacting with it directly."""
    def __init__(self, agent_id: uuid.UUID, client: 'Simile'):
        self._agent_id = agent_id
        self._client = client

    @property
    def id(self) -> uuid.UUID:
        return self._agent_id

    async def generate_qual_response(self, question: str) -> QualGenerationResponse:
        """Generates a qualitative response from this agent based on a question."""
        return await self._client.generate_qual_response(agent_id=self._agent_id, question=question)

    async def generate_mc_response(self, question: str, options: List[str]) -> MCGenerationResponse:
        """Generates a multiple-choice response from this agent."""
        return await self._client.generate_mc_response(agent_id=self._agent_id, question=question, options=options)


class SurveySession:
    """Represents an active survey session with an agent, allowing for contextual multi-turn generation."""
    def __init__(self, id: uuid.UUID, agent_id: uuid.UUID, status: str, client: 'Simile'):
        self._id = id
        self._agent_id = agent_id
        self._status = status
        self._client = client

    @property
    def id(self) -> uuid.UUID:
        return self._id

    @property
    def agent_id(self) -> uuid.UUID:
        return self._agent_id

    @property
    def status(self) -> str:
        return self._status

    async def generate_qual_response(self, question: str) -> QualGenerationResponse:
        """Generates a qualitative response within this survey session."""
        endpoint = f"sessions/{str(self._id)}/qual"
        payload = QualGenerationRequest(question=question) 
        return await self._client._request(
            "POST",
            endpoint,
            json=payload.model_dump(), 
            response_model=QualGenerationResponse
        )

    async def generate_mc_response(self, question: str, options: List[str]) -> MCGenerationResponse:
        """Generates a multiple-choice response within this survey session."""
        endpoint = f"sessions/{str(self._id)}/mc"
        payload = MCGenerationRequest(question=question, options=options) 
        return await self._client._request(
            "POST",
            endpoint,
            json=payload.model_dump(), 
            response_model=MCGenerationResponse
        )

    async def close(self) -> SurveySessionCloseResponse:
        """Closes this survey session on the server."""
        endpoint = f"sessions/{str(self._id)}/close"
        return await self._client._request(
            "POST",
            endpoint,
            response_model=SurveySessionCloseResponse
        )
