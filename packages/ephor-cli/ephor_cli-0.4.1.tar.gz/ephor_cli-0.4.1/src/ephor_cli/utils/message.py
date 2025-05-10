from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from google_a2a.common.types import Message


def a2a_message_to_langchain_message(message: Message) -> BaseMessage:
    if message.role == "user":
        return a2a_user_message_to_langchain_message(message)
    else:
        raise ValueError(f"Unknown message role: {message.role}")


def a2a_user_message_to_langchain_message(message: Message) -> HumanMessage:
    return HumanMessage(
        content=[{"type": "text", "text": part.text} for part in message.parts]
    )
