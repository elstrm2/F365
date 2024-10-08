import asyncio
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.utils import executor
from config.settings import REDIS_SETTINGS
from core.bot import bot
from core import logger
from handlers.admin import register_handlers_admin
from handlers.profile import register_handlers_profile
from handlers.search import register_handlers_search
from handlers.start import register_handlers_start
from core.parser import main as parser_main
from middlewares.ban import BanMiddleware
from middlewares.anti_spam import ThrottlingMiddleware
from middlewares.tech_works import TechWorksMiddleware
from tasks.record_load_history import (
    record_load_history,
)

logger.start()

storage = RedisStorage2(**REDIS_SETTINGS)
dp = Dispatcher(bot, storage=storage)

register_handlers_admin(dp)
register_handlers_profile(dp)
register_handlers_search(dp)
register_handlers_start(dp)

dp.middleware.setup(TechWorksMiddleware())
dp.middleware.setup(BanMiddleware())
dp.middleware.setup(ThrottlingMiddleware())


async def on_startup(dp: Dispatcher):
    asyncio.create_task(parser_main.main())
    asyncio.create_task(record_load_history())


if __name__ == "__main__":
    executor.start_polling(
        dp,
        skip_updates=True,
        on_startup=on_startup,
    )
