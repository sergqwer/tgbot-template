from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.markdown import hcode

from tgbot.filters import PrivateChatFilter, AdminFilter

admin_router = Router()
admin_router.message.filter(Command(commands=['a', 'admin']), PrivateChatFilter())


@admin_router.message(AdminFilter())
async def welcome_admin_message(message: Message):
    await message.answer(f'Welcome {message.from_user.mention_html()}!\n'
                         f'You are an administrator.\n'
                         f'Your ID: {hcode(message.from_user.id)}')


@admin_router.message(~AdminFilter())
async def not_an_admin_message(message: Message):
    await message.answer(f'You are not an administrator!')
