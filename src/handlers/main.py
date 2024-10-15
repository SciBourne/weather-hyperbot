from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from loguru import logger


router = Router()


@router.message(Command("start"))
async def start(msg: Message):
    logger.debug("Incoming message: /start")
    await msg.answer("Приветствие")


@router.message(Command("help"))
async def help_handler(msg: Message):
    logger.debug("Incoming message: /help")
    await msg.answer("Описание команд")


@router.message()
async def error_handler(msg: Message):
    logger.debug(f"Incoming message: {msg.text}")
    await msg.answer("API погоды")
