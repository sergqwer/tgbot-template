from typing import Union

from aiogram.enums import ChatType
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery


class PrivateChatFilter(BaseFilter):
    is_private: bool = True

    async def __call__(self, obj: Union[Message, CallbackQuery]) -> bool:
        if isinstance(obj, CallbackQuery):
            obj = obj.message

        return (obj.chat.type == ChatType.PRIVATE) == self.is_private
