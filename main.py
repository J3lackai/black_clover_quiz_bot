from config import Config, load_config
import asyncio
from aiogram import Bot, Dispatcher
from handlers import user, quiz, errors
from utils import setup_logger
from loguru import logger
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis
from aiogram.fsm.strategy import FSMStrategy
from middlewares import LexiconMiddleware


async def main() -> None:
    config: Config = load_config()
    setup_logger(config.bot.log)
    logger.info("🚀 Бот запускается...")
    bot = Bot(token=config.bot.token)
    redis = Redis(host="localhost")

    storage = RedisStorage(redis=redis)
    dp = Dispatcher(
        storage=storage,
        fsm_strategy=FSMStrategy.USER_IN_CHAT,
    )
    dp["redis"] = redis
    dp.message.outer_middleware(LexiconMiddleware(redis=redis))
    dp.include_router(user.router)
    dp.include_router(quiz.router)
    dp.include_router(errors.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
