from dataclasses import dataclass
import json
from re import A

from exceptions.base import ApplicationException


@dataclass(frozen=True, eq=False)
class BaseWebException(ApplicationException):
    status_code: int
    response_content: str

    @property
    def response_json(self) -> dict:
        return json.loads(self.response_content)

    @property
    def error_text(self) -> str:
        return self.response_json.get('detail', {}).get('error', '')


@dataclass(frozen=True, eq=False)
class ChatListRequestError(BaseWebException):
    @property
    def message(self) -> str:
        return 'Failed to get list of all chats'


@dataclass(frozen=True, eq=False)
class ListenerListRequestError(BaseWebException):
    @property
    def message(self) -> str:
        return 'Failed to get list of chat listeners'


@dataclass(frozen=True, eq=False)
class ListenerAddRequestError(BaseWebException):
    @property
    def message(self) -> str:
        return 'Failed to add listener to chat'


@dataclass(frozen=True, eq=False)
class ChatAlreadyExistsError(ApplicationException):
    telegram_chat_id: str | None = None
    web_chat_id: str | None = None

    @property
    def message(self) -> str:
        return 'Chat with that data already exists'


@dataclass(frozen=True, eq=False)
class ChatInfoNotFoundError(ApplicationException):
    telegram_chat_id: str | None = None
    web_chat_id: str | None = None

    @property
    def message(self) -> str:
        return 'Failed to find created chat'


@dataclass(frozen=True, eq=False)
class ChatNotFoundByTelegramIDError(ApplicationException):
    telegram_chat_id: str 

    @property
    def message(self) -> str:
        return 'Chat for respond not registered in bot'


@dataclass(frozen=True, eq=False)
class ChatInfoRequestError(BaseWebException):
    @property
    def message(self) -> str:
        return 'Failed to get information about chat'


@dataclass(frozen=True, eq=False)
class SendMessageToChatError(ApplicationException):
    @property
    def message(self) -> str:
        return 'Failed to send message to chat'