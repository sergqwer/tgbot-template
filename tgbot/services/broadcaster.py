import asyncio
import logging
from typing import Union

from aiogram import Bot, exceptions


async def send_message(bot: Bot, user_id: Union[int, str], text: str, disable_notification: bool = False) -> bool:
    try:
        await bot.send_message(chat_id=user_id, text=text, disable_notification=disable_notification)
    except exceptions.TelegramForbiddenError:
        logging.error(f"Target [ID:{user_id}]: got TelegramForbiddenError")

    except exceptions.TelegramRetryAfter as e:
        logging.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.retry_after} seconds.")
        await asyncio.sleep(e.retry_after)
        return await send_message(bot=bot, user_id=user_id, text=text,
                                  disable_notification=disable_notification)  # Recursive call

    except exceptions.TelegramAPIError:
        logging.exception(f"Target [ID:{user_id}]: failed")
    else:
        logging.info(f"Target [ID:{user_id}]: success")
        return True

    return False


async def broadcast(bot: Bot, users: list[int, str], text: str, delay: float = 0.05,
                    disable_notification: bool = False) -> int:
    """
    Simple broadcaster
    :return: Count of messages
    """
    count = 0
    try:
        for user_id in users:
            if await send_message(bot=bot, user_id=user_id, text=text, disable_notification=disable_notification):
                count += 1
            await asyncio.sleep(delay)  # Default 20 messages per second (Limit: 30 messages per second)
    finally:
        logging.info(f"{count} messages successful sent.")

    return count
