import pytest
from discogs_client import Client

from mcp_server_discogs.server import get_user_info_discogs, search_discogs


@pytest.mark.asyncio
async def test_search_discogs_base(mocker):
    dc: Client = Client(user_agent="mcp-server-discogs/0.1.0", user_token="abc")
    query_dict: dict[str, str] = {"query": "nirvana", "title": "nevermind", "year": "1991"}
    mocker.patch("discogs_client.Client.search")
    await search_discogs(client=dc, query_dict=query_dict)
    Client.search.assert_called_once_with(**query_dict)


@pytest.mark.asyncio
async def test_get_user_info_discogs_base(mocker):
    dc: Client = Client(user_agent="mcp-server-discogs/0.1.0", user_token="abc")
    mocker.patch("discogs_client.Client.identity")
    await get_user_info_discogs(client=dc)
    Client.identity.assert_called_once_with()
