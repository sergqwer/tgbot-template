import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from infrastructure.database.functions.setup import create_session_pool
from tgbot.config import Config, load_config
from tgbot.handlers.admins.admin import admin_router
from tgbot.handlers.users.echo import echo_router
from tgbot.handlers.users.user import user_router
from tgbot.middlewares import ConfigMiddleware, DatabaseMiddleware
from tgbot.misc.functions import on_startup_notify, on_shutdown_notify

logger = logging.getLogger(__name__)


def register_global_middlewares(dp: Dispatcher, config: Config, session_pool):
    dp.update.outer_middleware(ConfigMiddleware(config))
    dp.update.outer_middleware(DatabaseMiddleware(session_pool))


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s'
    )
    logger.info('Starting bot...')

    config = load_config('.env')
    storage = MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=storage)
    session_pool = await create_session_pool(db=config.db, echo=True, drop_all_tables=True)

    bot.config = config  # Binding the bot config to the bot object
    bot.db = session_pool  # Binding the session pool of the bot to the bot object

    # Registering bot routers
    for router in [
        user_router,  # All users
        admin_router,  # Admins
        echo_router  # All messages
    ]:
        dp.include_router(router)

    # Registering bot middlewares
    register_global_middlewares(dp=dp, config=config, session_pool=session_pool)

    dp.startup.register(on_startup_notify)
    dp.shutdown.register(on_shutdown_notify)

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt or SystemExit:
        logger.error('The bot has been disabled!')
