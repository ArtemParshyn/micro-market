"""Точка входа бота: python -m notification"""

import asyncio
import logging
import sys

from aiogram import Bot

from services.notification.config import settings
from services.app.rabbit import rabbit
from services.notification.worker import consume_and_send

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger(__name__)


async def main() -> None:
    if not settings.bot_token:
        logger.error("BOT_TOKEN is missing. Set it in .env or compose environment.")
        sys.exit(1)

    bot = Bot(token=settings.bot_token)
    await rabbit.connect()

    try:
        await consume_and_send(bot)
    finally:
        await rabbit.close()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
