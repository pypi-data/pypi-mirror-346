import click

from exponent.commands.shell_commands import Chat, LiveView, Theme, get_term_colors
from exponent.commands.types import exponent_cli_group
from exponent.core.config import Settings
from exponent.commands.settings import use_settings
from exponent.core.graphql.client import GraphQLClient
from exponent.core.graphql.subscriptions import CHAT_EVENTS_STREAM_SUBSCRIPTION
import asyncio
from exponent.core.types.generated.strategy_info import StrategyName
from websockets.exceptions import ConnectionClosed
import os


@exponent_cli_group(hidden=True)
def listen_cli() -> None:
    pass


@listen_cli.command()
@click.option("--chat-id", help="ID of the chat to listen to", required=True)
@use_settings
def listen(settings: Settings, chat_id: str) -> None:
    api_key = settings.api_key
    if not api_key:
        raise click.UsageError("API key is not set")

    base_api_url = settings.get_base_api_url()
    base_ws_url = settings.get_base_ws_url()

    gql_client = GraphQLClient(api_key, base_api_url, base_ws_url)

    working_directory = os.getcwd()
    (fg, bg, palette) = get_term_colors()
    theme = Theme(fg, bg, palette)

    chat = Chat(
        chat_id,
        None,
        settings.base_url,
        working_directory,
        gql_client,
        "CLAUDE_3_7_SONNET_20250219",
        StrategyName.NATURAL_EDIT_CLAUDE_3_7_XML,
        False,
        10,
        LiveView(theme, render_user_messages=True),
        checkpoints=[],
        thinking=False,
    )

    asyncio.run(_listen(gql_client, chat_id, chat))


async def _listen(gql_client: GraphQLClient, chat_id: str, chat: Chat) -> None:
    while True:
        try:
            async for response in gql_client.subscribe(
                CHAT_EVENTS_STREAM_SUBSCRIPTION, {"chatUuid": chat_id}
            ):
                event = response["authenticatedChatEventStream"]
                kind = event["__typename"]
                chat.view.render_event(kind, event)
        except ConnectionClosed:
            print("Websocket disconnected")
            await asyncio.sleep(1)
