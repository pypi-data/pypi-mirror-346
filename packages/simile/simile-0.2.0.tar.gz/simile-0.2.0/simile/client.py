import httpx
from httpx import AsyncClient
from typing import List, Dict, Any, Optional, Union, Type
import uuid
from pydantic import BaseModel

from .models import (
    Population, Agent, DataItem,
    CreatePopulationPayload, CreateAgentPayload, CreateDataItemPayload, UpdateDataItemPayload,
    DeletionResponse, QualGenerationRequest, QualGenerationResponse, MCGenerationRequest, MCGenerationResponse
)
from .exceptions import (
    SimileAPIError, SimileAuthenticationError, SimileNotFoundError, SimileBadRequestError
)

DEFAULT_BASE_URL = "https://simile-api-3a83be7adae0.herokuapp.com/api/v1"
TIMEOUT_CONFIG = httpx.Timeout(5.0, read=30.0, write=30.0, pool=30.0)

class Simile:
    def __init__(self, api_key: str, base_url: str = DEFAULT_BASE_URL):
        if not api_key:
            raise ValueError("API key is required.")
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self._client = AsyncClient(
            headers={"X-API-Key": self.api_key},
            timeout=TIMEOUT_CONFIG
        )

    async def _request(self, method: str, endpoint: str, **kwargs) -> Union[httpx.Response, BaseModel]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response_model_cls: Optional[Type[BaseModel]] = kwargs.pop("response_model", None)
        
        try:
            response = await self._client.request(method, url, **kwargs)
            response.raise_for_status()

            if response_model_cls:
                return response_model_cls(**response.json())
            else:
                return response
        except httpx.HTTPStatusError as e:
            status_code = e.response.status_code
            try:
                error_data = e.response.json()
                detail = error_data.get("detail", e.response.text)
            except Exception:
                detail = e.response.text

            if status_code == 401:
                raise SimileAuthenticationError(detail=detail)
            elif status_code == 404:
                raise SimileNotFoundError(detail=detail)
            elif status_code == 400:
                raise SimileBadRequestError(detail=detail)
            else:
                raise SimileAPIError(f"API request failed: {e}", status_code=status_code, detail=detail)
        except httpx.RequestError as e:
            raise SimileAPIError(f"Request error: {e}")

    # --- Population Endpoints ---
    async def create_population(self, payload: CreatePopulationPayload) -> Population:
        response_data = await self._request("POST", "populations/create", json=payload.model_dump(mode='json', exclude_none=True), response_model=Population)
        return response_data

    async def get_population(self, population_id: Union[str, uuid.UUID]) -> Population:
        response_data = await self._request("GET", f"populations/get/{str(population_id)}", response_model=Population)
        return response_data

    async def delete_population(self, population_id: Union[str, uuid.UUID]) -> DeletionResponse:
        response_data = await self._request("DELETE", f"populations/delete/{str(population_id)}", response_model=DeletionResponse)
        return response_data

    # --- Agent Endpoints ---
    async def create_agent(self, payload: CreateAgentPayload) -> Agent:
        response_data = await self._request("POST", "agents/create", json=payload.model_dump(mode='json', exclude_none=True), response_model=Agent)
        return response_data

    async def get_agent(self, agent_id: Union[str, uuid.UUID]) -> Agent:
        response_data = await self._request("GET", f"agents/get/{str(agent_id)}", response_model=Agent)
        return response_data

    async def delete_agent(self, agent_id: Union[str, uuid.UUID]) -> DeletionResponse:
        response_data = await self._request("DELETE", f"agents/delete/{str(agent_id)}", response_model=DeletionResponse)
        return response_data

    # --- Data Item Endpoints ---
    async def create_data_item(self, agent_id: Union[str, uuid.UUID], payload: CreateDataItemPayload) -> DataItem:
        response_data = await self._request("POST", f"data_item/create/{str(agent_id)}", json=payload.model_dump(mode='json'), response_model=DataItem)
        return response_data

    async def get_data_item(self, data_item_id: Union[str, uuid.UUID]) -> DataItem:
        response_data = await self._request("GET", f"data_item/get/{str(data_item_id)}", response_model=DataItem)
        return response_data

    async def list_data_items(self, agent_id: Union[str, uuid.UUID], data_type: Optional[str] = None) -> List[DataItem]:
        params = {}
        if data_type:
            params["data_type"] = data_type
        raw_response = await self._request("GET", f"data_item/list/{str(agent_id)}", params=params) 
        return [DataItem(**item) for item in raw_response.json()] 

    async def update_data_item(self, data_item_id: Union[str, uuid.UUID], payload: UpdateDataItemPayload) -> DataItem:
        response_data = await self._request("POST", f"data_item/update/{data_item_id}", json=payload.model_dump(), response_model=DataItem)
        return response_data

    async def delete_data_item(self, data_item_id: Union[str, uuid.UUID]) -> DeletionResponse:
        response_data = await self._request("DELETE", f"data_item/delete/{str(data_item_id)}", response_model=DeletionResponse)
        return response_data

    # --- LLM Generation Methods ---
    async def generate_qual_response(self, agent_id: uuid.UUID, request_payload: QualGenerationRequest) -> QualGenerationResponse:
        endpoint = f"/generation/qual/{str(agent_id)}"
        response_data = await self._request(
            "POST", 
            endpoint, 
            json=request_payload.model_dump(), 
            response_model=QualGenerationResponse
        )
        return response_data

    async def generate_mc_response(self, agent_id: uuid.UUID, request_payload: MCGenerationRequest) -> MCGenerationResponse:
        endpoint = f"generation/mc/{agent_id}" 
        response_data = await self._request("POST", endpoint, json=request_payload.model_dump(), response_model=MCGenerationResponse)
        return response_data

    async def aclose(self):
        await self._client.aclose() 

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.aclose()
