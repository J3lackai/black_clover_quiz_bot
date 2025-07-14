from config.config import Config, load_config
import asyncio
from aiogram import Bot, Dispatcher
from handlers import user, quiz, errors, language
from utils import setup_logger
from loguru import logger
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.strategy import FSMStrategy
from middlewares import LexiconMiddleware
import os

os.environ["AIORGRAM_FSM_STRATEGY"] = "USER_IN_CHAT"


async def main() -> None:
    config: Config = load_config()
    setup_logger(config.bot.log)
    logger.info("🚀 Бот запускается...")
    bot = Bot(token=config.bot.token)
    storage = MemoryStorage()
    dp = Dispatcher(
        storage=storage,
        fsm_strategy=FSMStrategy.USER_IN_CHAT,  # Важная настройка для aiogram 3.x
    )
    dp.message.outer_middleware(LexiconMiddleware())
    dp.include_router(user.router)
    dp.include_router(quiz.router)
    dp.include_router(language.router)
    dp.include_router(errors.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
