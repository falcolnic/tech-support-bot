from dtos.messages import ChatListItemDTO

from telegram.helpers import escape_markdown


def convert_chats_dtos_to_message(chats: list[ChatListItemDTO]) -> str:
    return '\n'.join(
        (
            'List of all avaible chats:',
            '\n'.join(
                (f"ChatOID: `{escape_markdown(chat.oid, version=2)}` Problem: {escape_markdown(chat.title, version=2)}" for chat in chats)  # type: ignore
            )
        )
    )