from telegram import Update
from telegram.ext import ContextTypes

from containers.factories import get_container
from handlers.converters.chats import convert_chats_dtos_to_message
from services.web import BaseChatWebService


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


async def set_chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    container = get_container()
    
    async with container() as request_container:
        service = await request_container.get(BaseChatWebService)
        chats = await service.get_all_chats()
        context.bot.getc
        
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=convert_chats_dtos_to_message(chats=chats),
            parse_mode='MarkdownV2',
        )