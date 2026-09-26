from pydantic import BaseModel, Field


class SendMessage(BaseModel):
    chat_id: int = Field(..., description="Telegram chat id")
    text: str = Field(..., min_length=1)
