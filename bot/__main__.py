"""Точка входа бота: python -m bot"""

import asyncio
import logging
import sys

from aiogram import Bot

from app.config import BOT_TOKEN
from app.rabbit import rabbit
from bot.worker import consume_and_send

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger(__name__)


async def main() -> None:
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN is missing. Set it in .env or compose environment.")
        sys.exit(1)

    bot = Bot(token=BOT_TOKEN)
    await rabbit.connect()

    try:
        await consume_and_send(bot)
    finally:
        await rabbit.close()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
