"""
FastAPI + RabbitMQ - Telegram.

Направление одно: API кладёт сообщение в очередь tg_send,
бот его забирает и отправляет пользователю.

POST /send — положить сообщение в очередь.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel

from dependencies.config import QUEUE_TG
from dependencies.rabbit import rabbit


@asynccontextmanager
async def lifespan(app: FastAPI):
    await rabbit.connect()
    yield
    await rabbit.close()


app = FastAPI(title="FastAPI → TG via RabbitMQ", lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "OK", "queue": QUEUE_TG}


class SendMessage(BaseModel):
    chat_id: int
    text: str


@app.post("/send")
async def send(msg: SendMessage):
    """Положить сообщение в очередь — бот отправит его в Telegram."""
    await rabbit.publish(msg.model_dump())
    return {"status": "queued", "payload": msg.model_dump()}
