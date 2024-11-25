from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ProjectSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    GREETING_TEXT: str = Field(
        alias='GREETING_TEXT', 
        default=(
            'Welcome to the support bot.\n'
            'Please select a chat to work with the client.' 
            '\nGet list of all chats /chats, select chat /set_chats <oid_chat>'
        ),
    )
    WEB_API_BASE_URL: str = Field(default='http://main-app:8000')
    KAFKA_BROKER_URL: str = Field(default='kafka:29092')
    NEW_MESSAGE_TOPIC: str = Field(default='new-messages')
    NEW_CHAT_TOPIC: str = Field(default='new-chats-topic')
    KAFKA_GROUP_ID: str = Field(default='tg-bot')
    DATABASE_NAME: str = Field(default='test.db')
    TELEGRAM_GROUP_ID: str = Field()
    TG_BOT_TOKEN: str = Field()

@lru_cache(1)
def get_settings() -> ProjectSettings:
    return ProjectSettings()