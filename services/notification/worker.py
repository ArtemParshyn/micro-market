from __future__ import annotations

import logging
from typing import Any

from aiogram import Bot

from services.app.rabbit import rabbit

logger = logging.getLogger(__name__)


async def consume_and_send(bot: Bot) -> None:
    async def on_message(payload: dict[str, Any]) -> None:
        chat_id = payload.get("chat_id")
        text = payload.get("text", "")

        if chat_id is None or not text:
            logger.warning("skip invalid payload: %s", payload)
            return

        await bot.send_message(chat_id=int(chat_id), text=text)
        logger.info("sent to telegram chat_id=%s text=%r", chat_id, text)

    logger.info("notification consumer started, waiting for messages")
    await rabbit.consume(on_message)
