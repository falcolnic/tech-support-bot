from faststream import Context
from faststream.kafka.broker import KafkaBroker
from telegram import Bot

from consumers.schemas import NewChatMessageSchema, NewChatSchema
from containers.factories import get_container
from services.web import BaseChatWebService
from settings import get_settings


settings = get_settings()
router = KafkaBroker()


@router.subscriber(settings.NEW_CHAT_TOPIC, group_id=settings.KAFKA_GROUP_ID)
async def new_chat_handler(data: NewChatSchema):
    # TODO: создать маппинг telegram_thread_id и chat_oid
    # записывать этот маппинг в модели, сохранять при создании топика в телеге
    
    container = get_container()

    async with container() as request_container:
        bot = await request_container.get(Bot)
        chat = await bot.get_chat(chat_id=settings.TELEGRAM_GROUP_ID)
        chat_title = f'{data.chat_title} | {data.chat_oid}'
        await chat.create_forum_topic(name=chat_title)


@router.subscriber(settings.NEW_MESSAGE_TOPIC, group_id=settings.KAFKA_GROUP_ID)
async def new_message_subscription_handler(
    message: NewChatMessageSchema,
    key: bytes = Context('message.raw_message.key'),
):
    container = get_container()
    async with container() as requst_container:
        service = await requst_container.get(BaseChatWebService)
        listeners = await service.get_chat_listeners(chat_oid=key.decode())
        chat_info = await service.get_chat_info(chat_oid=key.decode())

        bot = await requst_container.get(Bot)

        for listener in listeners:
            await bot.send_message(
                chat_id=listener.oid,
                text=(
                    f'Message from chat (<code>{chat_info.oid}</code>) <b>{chat_info.title}</b>'
                    f'<blockquote>{message.message_text}</blockquote>'
                ),
                parse_mode='HTML',
            )
