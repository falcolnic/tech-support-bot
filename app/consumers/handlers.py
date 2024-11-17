from faststream import Context
from faststream.kafka.broker import KafkaBroker
from telegram import Bot

from consumers.schemas import NewChatMessageSchema
from containers.factories import get_container
from services.web import BaseChatWebService
from settings import get_settings


settings = get_settings()
router = KafkaBroker()

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
