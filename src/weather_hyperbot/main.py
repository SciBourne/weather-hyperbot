import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from loguru import logger as log

from configs import BOT_TOKEN
from router import router


async def main():
    bot = Bot(
        token=BOT_TOKEN,

        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )

    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    log.info("Weather Hyperbot started")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


def start():
    asyncio.run(
        main()
    )
