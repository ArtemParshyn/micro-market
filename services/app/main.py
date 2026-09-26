import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from services.notification.config import settings
from services.app.rabbit import rabbit
from services.app.schemas import SendMessage

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await rabbit.connect()
    yield
    await rabbit.close()


app = FastAPI(title="FastAPI → Telegram", lifespan=lifespan)


@app.get("/health")
async def health():
    return {"status": "ok", "queue": settings.queue_tg}

@app.post("/send")
async def send(msg: SendMessage):
    await rabbit.publish(msg.model_dump())
    logger.info("queued chat_id=%s text=%r", msg.chat_id, msg.text)
    return {"status": "queued", "payload": msg.model_dump()}
