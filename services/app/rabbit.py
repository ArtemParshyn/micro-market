from __future__ import annotations

import json
import logging
from collections.abc import Awaitable, Callable
from typing import Any

import aio_pika
from aio_pika import Message
from aio_pika.abc import AbstractChannel, AbstractQueue, AbstractRobustConnection

from services.notification.config import settings

logger = logging.getLogger(__name__)

MessageHandler = Callable[[dict[str, Any]], Awaitable[None]]


class Rabbit:
    def __init__(self) -> None:
        self.connection: AbstractRobustConnection | None = None
        self.channel: AbstractChannel | None = None
        self.queue: AbstractQueue | None = None

    async def connect(self) -> None:
        self.connection = await aio_pika.connect_robust(settings.rabbit_url)
        self.channel = await self.connection.channel()
        self.queue = await self.channel.declare_queue(settings.queue_tg, durable=True)
        logger.info("RabbitMQ connected, queue=%s", settings.queue_tg)

    async def close(self) -> None:
        if self.connection and not self.connection.is_closed:
            await self.connection.close()
            logger.info("RabbitMQ connection closed")

    async def publish(self, payload: dict[str, Any]) -> None:
        if self.channel is None:
            raise RuntimeError("RabbitMQ is not connected")

        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        message = Message(body, delivery_mode=aio_pika.DeliveryMode.PERSISTENT)
        await self.channel.default_exchange.publish(message, routing_key=settings.queue_tg)

    async def consume(self, handler: MessageHandler) -> None:
        if self.queue is None:
            raise RuntimeError("RabbitMQ is not connected")

        async with self.queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    payload = json.loads(message.body.decode("utf-8"))
                    await handler(payload)


rabbit = Rabbit()
