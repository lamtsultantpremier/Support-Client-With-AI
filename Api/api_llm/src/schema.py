from pydantic import BaseModel,Field,ConfigDict

from typing import List
from dataclasses import dataclass
from langchain_core.messages import BaseMessage

class Message(BaseMessage):
    role:str
    content:str
    model_config = ConfigDict(from_attributes = True)


class ChatRequest(BaseModel):
    input:str
    messages:List[Message]
@dataclass
class MessageBase:
    role:str
    content:str