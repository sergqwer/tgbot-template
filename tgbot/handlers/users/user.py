from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hcode, hlink

from tgbot.filters import PrivateChatFilter

user_router = Router()
user_router.message.filter(PrivateChatFilter())


@user_router.message(CommandStart())
async def bot_start(message: Message):
    await message.answer(
        f'Welcome {message.from_user.mention_html()}!\n'
        f'Your ID: {hcode(message.from_user.id)}\n'
        f'Use the /a or /admin command to access the admin menu (available for administrators only)\n\n'
        f'This template was created using {hlink("Aiogram 3.x", "https://docs.aiogram.dev/en/dev-3.x/")} '
        f'and {hlink("SQLAlchemy 2.x", "https://docs.sqlalchemy.org/en/20/index.html")}'
    )
