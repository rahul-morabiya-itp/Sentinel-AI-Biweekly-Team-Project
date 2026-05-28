from pydantic import BaseModel


class ChatRequest(BaseModel):

    source: str

    prompt: str
