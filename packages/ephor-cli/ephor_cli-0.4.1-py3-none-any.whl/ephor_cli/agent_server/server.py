from starlette.applications import Starlette
from starlette.responses import JSONResponse
from sse_starlette.sse import EventSourceResponse
from starlette.requests import Request
from google_a2a.common.types import (
    A2ARequest,
    JSONRPCResponse,
    InvalidRequestError,
    JSONParseError,
    GetTaskRequest,
    CancelTaskRequest,
    SendTaskRequest,
    SetTaskPushNotificationRequest,
    GetTaskPushNotificationRequest,
    InternalError,
    AgentCard,
    TaskResubscriptionRequest,
    SendTaskStreamingRequest,
    AgentSkill as A2AAgentSkill,
    AgentCapabilities as A2AAgentCapabilities,
)
from pydantic import ValidationError
import json
from typing import AsyncIterable, Any
import requests
import os
import logging
from ephor_cli.agent_server.task_manager import AgentTaskManager
from ephor_cli.types.agent import AgentConfig
from ephor_cli.constant import AGENT_SERVER_URL


logger = logging.getLogger(__name__)


class A2AProxyServer:
    def __init__(
        self,
        host="0.0.0.0",
        port=5000,
        api_url="http://localhost:3000/api",
    ):
        self.host = host
        self.port = port
        self.api_url = api_url
        self.app = Starlette()
        self.app.add_route("/", self._health_check, methods=["GET"])
        self.app.add_route("/health", self._health_check, methods=["GET"])
        self.app.add_route("/{agent_id}", self._process_request, methods=["POST"])
        self.app.add_route(
            "/{agent_id}/.well-known/agent.json", self._get_agent_card, methods=["GET"]
        )

    def _health_check(self, request: Request) -> JSONResponse:
        """Health check endpoint for ECS"""
        return JSONResponse({"status": "healthy"}, status_code=200)

    def _load_agent_from_api(self, agent_id: str) -> AgentConfig | None:
        """Load an agent from the API by ID."""
        if not os.environ.get("EPHOR_API_KEY"):
            raise ValueError("EPHOR_API_KEY environment variable not set")

        try:
            headers = {"x-api-key": os.environ.get("EPHOR_API_KEY")}
            url = f"{self.api_url}/agents/{agent_id}"
            logger.info(f"Loading agent from {url}")
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            agent_data = response.json()
            agent_config = AgentConfig(**agent_data)
            return agent_config
        except Exception as e:
            logger.error(f"Failed to load agent '{agent_id}' from API: {e}")
            return None

    def _create_task_manager(self, agent_id: str) -> AgentTaskManager:
        """Create a task manager for an agent."""
        agent_config = self._load_agent_from_api(agent_id)
        return AgentTaskManager(agent_config)

    def _create_agent_card_from_config(
        self, config: AgentConfig, agent_id: str
    ) -> AgentCard:
        """Create an AgentCard from an AgentConfig."""
        # Create skills
        skills = []
        for skill_config in config.skills:
            skill = A2AAgentSkill(
                id=skill_config.id,
                name=skill_config.name,
                description=skill_config.description,
                tags=skill_config.tags,
                examples=skill_config.examples,
                inputModes=skill_config.inputModes,
                outputModes=skill_config.outputModes,
            )
            skills.append(skill)

        # Create capabilities
        capabilities = A2AAgentCapabilities(streaming=config.capabilities.streaming)

        # Create agent card
        agent_card = AgentCard(
            name=config.name,
            description=config.description,
            url=f"{AGENT_SERVER_URL}/{agent_id}",
            version=config.version,
            defaultInputModes=["text"],
            defaultOutputModes=["text"],
            capabilities=capabilities,
            skills=skills,
        )

        return agent_card

    def start(self):
        import uvicorn

        uvicorn.run(self.app, host=self.host, port=self.port)

    def _get_agent_card(self, request: Request) -> JSONResponse:
        agent_id = request.path_params.get("agent_id")
        agent_config = self._load_agent_from_api(agent_id)
        if not agent_config:
            raise ValueError(f"Agent {agent_id} not found")
        agent_card = self._create_agent_card_from_config(agent_config, agent_id)
        return JSONResponse(agent_card.model_dump(exclude_none=True))

    async def _process_request(self, request: Request):
        agent_id = request.path_params.get("agent_id")
        logger.info(f"Processing request for agent {agent_id}")

        task_manager = self._create_task_manager(agent_id)

        try:
            body = await request.json()
            json_rpc_request = A2ARequest.validate_python(body)

            if isinstance(json_rpc_request, GetTaskRequest):
                result = await task_manager.on_get_task(json_rpc_request)
            elif isinstance(json_rpc_request, SendTaskRequest):
                result = await task_manager.on_send_task(json_rpc_request)
            elif isinstance(json_rpc_request, SendTaskStreamingRequest):
                result = await task_manager.on_send_task_subscribe(json_rpc_request)
            elif isinstance(json_rpc_request, CancelTaskRequest):
                result = await task_manager.on_cancel_task(json_rpc_request)
            elif isinstance(json_rpc_request, SetTaskPushNotificationRequest):
                result = await task_manager.on_set_task_push_notification(
                    json_rpc_request
                )
            elif isinstance(json_rpc_request, GetTaskPushNotificationRequest):
                result = await task_manager.on_get_task_push_notification(
                    json_rpc_request
                )
            elif isinstance(json_rpc_request, TaskResubscriptionRequest):
                result = await task_manager.on_resubscribe_to_task(json_rpc_request)
            else:
                logger.warning(f"Unexpected request type: {type(json_rpc_request)}")
                raise ValueError(f"Unexpected request type: {type(request)}")

            return self._create_response(result)

        except Exception as e:
            return self._handle_exception(e)

    def _handle_exception(self, e: Exception) -> JSONResponse:
        if isinstance(e, json.decoder.JSONDecodeError):
            json_rpc_error = JSONParseError()
        elif isinstance(e, ValidationError):
            json_rpc_error = InvalidRequestError(data=json.loads(e.json()))
        else:
            logger.error(f"Unhandled exception: {e}")
            json_rpc_error = InternalError()

        response = JSONRPCResponse(id=None, error=json_rpc_error)
        return JSONResponse(response.model_dump(exclude_none=True), status_code=400)

    def _create_response(self, result: Any) -> JSONResponse | EventSourceResponse:
        if isinstance(result, AsyncIterable):

            async def event_generator(result) -> AsyncIterable[dict[str, str]]:
                async for item in result:
                    yield {"data": item.model_dump_json(exclude_none=True)}

            return EventSourceResponse(event_generator(result))
        elif isinstance(result, JSONRPCResponse):
            return JSONResponse(result.model_dump(exclude_none=True))
        else:
            logger.error(f"Unexpected result type: {type(result)}")
            raise ValueError(f"Unexpected result type: {type(result)}")
