
from pydantic import BaseModel, Field


class SendMessage(BaseModel):
    chat_id: str
    text: str
    data: dict = {}


class ChatStatus(BaseModel):
    chat_id: str
