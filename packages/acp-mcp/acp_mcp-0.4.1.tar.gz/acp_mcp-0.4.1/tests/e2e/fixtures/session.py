import asyncio
from collections.abc import AsyncIterator
from threading import Thread

import pytest
from acp_sdk.models import (
    Message,
)
from acp_sdk.server import Context
from acp_sdk.server import Server as ACPServer
from mcp import ClientSession
from mcp.shared.memory import create_connected_server_and_client_session
from pydantic import AnyHttpUrl

from acp_mcp.adapter import create_adapter
from e2e.config import Config


@pytest.fixture
async def session() -> AsyncIterator[ClientSession]:
    acp_server = ACPServer()

    @acp_server.agent()
    async def echo(input: list[Message], context: Context) -> AsyncIterator[Message]:
        "Echoes everything"
        for message in input:
            yield message

    @acp_server.agent()
    async def slow_echo(input: list[Message], context: Context) -> AsyncIterator[Message]:
        "Echoes everything but slowly"
        for message in input:
            await asyncio.sleep(1)
            yield message

    thread = Thread(target=acp_server.run, kwargs={"port": Config.PORT}, daemon=True)
    thread.start()

    await asyncio.sleep(1)

    server = create_adapter(AnyHttpUrl(f"http://localhost:{Config.PORT}"))
    async with create_connected_server_and_client_session(server=server) as session:
        yield session

    acp_server.should_exit = True
    thread.join(timeout=2)
