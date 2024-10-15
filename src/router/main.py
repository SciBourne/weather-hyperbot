from aiogram import Router
from handlers import main_router


router = Router()
router.include_router(main_router)
