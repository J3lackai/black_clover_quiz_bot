from config.config import Config, load_config
import asyncio
from aiogram import Bot, Dispatcher
from handlers import user, quiz, errors
from loguru import logger


async def main() -> None:
    config: Config = load_config()
    bot = Bot(token=config.bot.token)
    dp = Dispatcher()
    dp.include_router(user.router)
    dp.include_router(quiz.router)
    dp.include_router(errors.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
