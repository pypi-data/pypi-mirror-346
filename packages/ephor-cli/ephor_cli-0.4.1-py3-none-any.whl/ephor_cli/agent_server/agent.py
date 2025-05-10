import logging
from contextlib import asynccontextmanager
from typing import AsyncIterable, Literal, Optional, Union

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    AIMessageChunk,
    ToolMessageChunk,
)
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel, Field
from ephor_cli.types.conversation import Conversation
from ephor_cli.types.agent import MCPServerConfig

logger = logging.getLogger(__name__)


@asynccontextmanager
async def get_tools(mcpServers: list[MCPServerConfig]):
    if not mcpServers:
        yield []
        return
    config = {
        mcpServer.name: {
            "url": mcpServer.url,
            "transport": mcpServer.transport,
        }
        for mcpServer in mcpServers
    }
    async with MultiServerMCPClient(config) as client:
        logger.info(f"Loaded {len(client.get_tools())} tools")
        yield client.get_tools()


class ResponseFormat(BaseModel):
    """Respond to the user in this format."""

    conversation: Conversation
    status: Literal["input_required", "completed", "error"]
    input_message: Optional[str] = Field(
        default="Message to the user if additional input is required from user to complete the task."
    )
    error_message: Optional[str] = Field(
        default="Message to the user if the task can not be completed even with additional input from user or if you are not supposed to entertain such requests."
    )
    final_response: Optional[str] = Field(
        default="Final response to the user if the task is completed. This should be a complete response and should not refer to any previous messages. User will see only this message as final response to the given task so make sure it is complete and self-contained."
    )


class Agent:
    def __init__(
        self,
        name: str,
        prompt: str = None,
        model: str = "claude-3-5-sonnet-20240620",
        temperature: float = 0.2,
        supported_content_types: list[str] = ["text", "text/plain"],
        initial_state: list[BaseMessage] = None,
        tools: list = None,
    ):
        self.name = name
        self.prompt = prompt
        self.model = ChatAnthropic(model=model, temperature=temperature)
        self.supported_content_types = supported_content_types
        self.tools = tools if tools is not None else []
        self.graph = None
        self.memory = MemorySaver()
        self.initial_state = initial_state

    def _prompt(self, prompt: str):
        return f"""
        {prompt}

        Remember: 
        - Your job is to complete the given task.
        - You can ask user for additional information if needed to complete the task. Respond with input_required status and provide a message to the user.
        - If task can not be completed even with additional input from user or if you are not supposed to entertain such requests, respond with error status and provide an error message to the user.
        - If task is completed, respond with completed status and provide a final response to the user. Do not ask any follow up question to continue the chat.
        """

    async def initialize_graph(self, sessionId: str):
        if self.graph:
            return

        self.graph = create_react_agent(
            self.model,
            prompt=self.prompt,
            tools=self.tools,
            checkpointer=self.memory,
            response_format=ResponseFormat,
        )

        if self.initial_state:
            self.graph.update_state(
                self._get_config(sessionId), {"messages": self.initial_state}
            )

    def _get_config(self, session_id: str):
        return {"configurable": {"thread_id": session_id}}

    async def stream(
        self, message: HumanMessage, session_id: str
    ) -> AsyncIterable[Union[AIMessageChunk, ToolMessageChunk]]:
        await self.initialize_graph(session_id)
        inputs = {"messages": [message]}
        config = self._get_config(session_id)

        logger.info(
            f"Streaming agent with query: {message}, sessionId: {session_id}, current state: {self.graph.get_state(config)}"
        )

        async for chunk, _ in self.graph.astream(
            inputs, config, stream_mode="messages"
        ):
            # print(f"Stream event => {chunk}")
            yield chunk

    def get_agent_response(self, session_id: str):
        current_state = self.graph.get_state(self._get_config(session_id))
        print(f"Current state: {current_state}")
        structured_response = current_state.values.get("structured_response")

        if structured_response and isinstance(structured_response, ResponseFormat):
            if structured_response.status == "input_required":
                return {
                    "is_task_complete": False,
                    "require_user_input": True,
                    "content": structured_response.input_message,
                }
            elif structured_response.status == "error":
                return {
                    "is_task_complete": False,
                    "require_user_input": True,
                    "content": structured_response.error_message,
                }
            elif structured_response.status == "completed":
                return {
                    "is_task_complete": True,
                    "require_user_input": False,
                    "content": structured_response.final_response,
                }

        return {
            "is_task_complete": False,
            "require_user_input": True,
            "content": "We are unable to process your request at the moment. Please try again.",
        }

    def get_current_state(self, session_id: str):
        return self.graph.get_state(self._get_config(session_id))
