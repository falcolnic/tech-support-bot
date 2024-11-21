from telegram import Bot, Update
from telegram.ext import ContextTypes

from containers.factories import get_container
from handlers.converters.chats import convert_chats_dtos_to_message
from services.web import BaseChatWebService


async def get_thread_name(bot: Bot, chat_id: int, message_thread_id: int) -> str:
    # Get first message in thread
    chat = await bot.get_chat(chat_id=chat_id)
    message = await chat.get_message(message_thread_id)
    # Return thread name
    return message.text


async def get_all_chats_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    container = get_container()
    
    async with container() as request_container:
        service = await request_container.get(BaseChatWebService)
        chats = await service.get_all_chats()
        
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=convert_chats_dtos_to_message(chats=chats),
            parse_mode='MarkdownV2',
        )


async def set_chat_listener(update: Update, context: ContextTypes.DEFAULT_TYPE):
    container = get_container()
    
    async with container() as request_container:
        service = await request_container.get(BaseChatWebService)  # type: ignore
        await service.add_listener(
            telegram_chat_id=update.effective_chat.id,
            chat_oid=context.args[0],
        )

        await context.bot.send_message(
            chat_id=update.effective_chat.id,  # type: ignore
            text='You connected to the chat',
            parse_mode='MarkdownV2',
        )


async def quit_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,  # type: ignore
            text='You left the chat',
            parse_mode='MarkdownV2',
        )


async def send_message_to_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # TODO: сделать паттерн под UUID4
        thread_name = await get_thread_name(context.bot, chat_id=update.message.chat_id, message_thread_id=update.message.message_id)
    except IndexError:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,  # type: ignore
            text='Необходимо ответить именно на сообщение пользователя.',
        )
        return
