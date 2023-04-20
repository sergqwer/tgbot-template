from aiogram import Router, F
from aiogram.types import Message

from tgbot.filters import PrivateChatFilter

echo_router = Router()
echo_router.message.filter(PrivateChatFilter())


@echo_router.message(F.text)
async def bot_echo(message: Message):
    await message.answer(message.text)
