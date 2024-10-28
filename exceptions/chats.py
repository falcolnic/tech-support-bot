from dataclasses import dataclass

from exceptions.base import ApplicationException


@dataclass(frozen=True, eq=False)
class ChatListRequestError(ApplicationException):
    status_code: int
    response_content: str

    @property
    def message(self):
        return 'Failed to retrieve the list of all chats'