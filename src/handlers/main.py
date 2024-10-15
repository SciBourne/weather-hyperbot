from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from loguru import logger as log

from services.owm import get_weather
from models.errors import WeatherError


router = Router()


@router.message(Command("start"))
async def start(msg: Message):
    log.debug("Incoming message: /start")

    await msg.answer(
        "<b>Нужна инфа о погоде?</b>\n"
        "Ни слова больше, просто скинь мне имя города:"
    )


@router.message(Command("help"))
async def help_handler(msg: Message):
    log.debug("Incoming message: /help")

    await msg.answer(
        ("<b>/start</b> — начало работы\n"
         "<b>/help</b> — помощь\n"
         "<b>имя города</b> — получить прогноз погоды")
    )


@router.message()
async def weather_handler(msg: Message):
    log.debug(f"Incoming message: {msg.text}")
    data = await get_weather(msg.text)

    match data:
        case WeatherError.NAME_ERR:
            await msg.answer("Неизвестный город")

        case WeatherError.SERVICE_ERR:
            await msg.answer("Сервис временно недоступен")

        case _:
            await msg.answer(
                f"Температура: <code>{data['main']['temp']}°C</code>\n"
                f"Влажность: <code>{data['main']['humidity']}%</code>\n\n"
                f"Описание: <code>{data['weather'][0]['description']}</code>"
            )
