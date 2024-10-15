import aiohttp
from loguru import logger as log

from configs import (
    OWM_API_KEY,

    OWM_BASE_URL,
    OWM_GEO_POINT,
    OWM_WEATHER
)

from models.errors import WeatherError


async def get_coordinates(client: aiohttp.ClientSession, city: str):
    end_point = f"{OWM_BASE_URL}{OWM_GEO_POINT}?q={city},RU&appid={OWM_API_KEY}"

    async with client.get(end_point) as resp:
        match resp.status:
            case 200:
                locations = await resp.json()
                return locations[0]

            case _:
                return None


async def get_weather(city: str):
    session_config = {
        'connector': aiohttp.TCPConnector(
            limit=None
        ),

        'timeout': aiohttp.ClientTimeout(
            total=None,
            sock_connect=5,
            sock_read=5
        )
    }

    try:
        async with aiohttp.ClientSession(**session_config) as client:
            location = await get_coordinates(client, city)

            if location is None:
                return WeatherError.NAME_ERR

            end_point = (
                f"{OWM_BASE_URL}{OWM_WEATHER}"
                f"?lat={location['lat']}&lon={location['lon']}"
                f"&appid={OWM_API_KEY}"
                "&lang=ru"
                "&units=metric"
            )

            async with client.get(end_point) as resp:
                match resp.status:
                    case 200:
                        weather_data = await resp.json()

                        log.debug(f"Data received: {weather_data['id']}")
                        return weather_data

                    case _:
                        log.error(resp.status, await resp.json())
                        return WeatherError.SERVICE_ERR

    except aiohttp.client_exceptions.SocketTimeoutError as err:
        log.error(err)
        return WeatherError.SERVICE_ERR
