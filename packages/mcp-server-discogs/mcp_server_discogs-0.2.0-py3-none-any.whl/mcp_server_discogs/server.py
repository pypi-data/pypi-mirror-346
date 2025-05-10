"""
Discogs MCP Server implementation.

This module implements a Model Context Protocol (MCP) server that provides
tools and resources for interacting with the Discogs API. It allows searching
the Discogs database and retrieving user information.
"""

import json
import os
from collections.abc import Sequence
from typing import Any

from discogs_client import Client
from discogs_client.models import MixedPaginatedList, User
from mcp.server import InitializationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import EmbeddedResource, ImageContent, Resource, TextContent, Tool
from pydantic import AnyUrl


async def serve() -> None:
    """
    Initialize and run the Discogs MCP server.

    This function sets up the MCP server with tools for searching Discogs and
    resources for retrieving user information. It requires a Discogs API token
    to be set in environment variables.

    Raises:
        ValueError: If the Discogs API token is not set in environment variables.

    Returns:
        None
    """
    token: str = os.getenv("DISCOGS_API_TOKEN", "")
    mcp: Server = Server(name="mcp-server-discogs")
    if token:
        dc: Client = Client(user_agent="mcp-server-discogs/0.1.0", user_token=token)
    else:
        raise ValueError("Access token not set.")

    @mcp.list_tools()
    async def handle_list_tools() -> list[Tool]:
        """
        List the available tools provided by this MCP server.

        This callback function is registered with the MCP server to handle
        tool listing requests. It defines and returns the available tools
        that can be used by clients.

        Returns:
            list[Tool]: A list containing the available tools, currently only
                the 'search' tool.
        """
        return [
            Tool(
                name="search",
                description="Searches discogs for a given search string and returns results. "
                "It is recommended to scope your search as much as possible as there will be many results. "
                "The search tool only looks at the first page anyway (for now)",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "The search string to be used in the search"},
                        "type": {
                            "type": "string",
                            "description": "The type of the query can be 'release', 'master', 'artist' or 'label'",
                        },
                        "title": {
                            "type": "string",
                            "descripion": 'Search by combined "Artist Name - Release Title" title field. '
                            "Example: nirvana - nevermind",
                        },
                        "release_title": {"type": "string", "description": "Search release titles. Example: nevermind"},
                        "credit": {"type": "string", "description": "Search release credits. Example: kurt"},
                        "artist": {"type": "string", "description": "Search artist names. Example: nirvana"},
                        "anv": {"type": "string", "description": "Search artist ANV. Example: nirvana"},
                        "label": {"type": "string", "description": "Search label names. Example: dgc"},
                        "genre": {"type": "string", "description": "Search genres. Example: rock"},
                        "style": {"type": "string", "description": "Search styles. Example: grunge"},
                        "country": {"type": "string", "description": "Search release country. Example: canada"},
                        "year": {"type": "string", "description": "Search release year. Example: 1991"},
                        "format": {"type": "string", "description": "Search formats. Example: album"},
                        "catno": {"type": "string", "description": "Search catalog number. Example: DGCD-24425"},
                        "barcode": {"type": "string", "description": "Search barcodes. Example: 7 2064-24425-2 4"},
                        "track": {
                            "type": "string",
                            "description": "Search track titles. Example: smells like teen spirit",
                        },
                        "submitter": {"type": "string", "description": "Search submitter username. Example: milKt"},
                        "contributor": {
                            "type": "string",
                            "description": "Search contributor usernames.  Example: jerome99",
                        },
                    },
                    "required": ["query"],
                },
            ),
            Tool(
                name="get-release-info",
                description="Gets all information about a specific release based on the release id",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "release-id": {"type": "string", "description": "The release id you want information about"}
                    },
                },
            ),
        ]

    @mcp.call_tool()
    async def handle_tool_call(name: str, arguments: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        """
        Handle tool call requests from clients.

        This callback function is registered with the MCP server to handle
        tool call requests. It routes the request to the appropriate tool
        implementation based on the tool name.

        Args:
            name: The name of the tool to call.
            arguments: A dictionary containing the arguments for the tool call.

        Returns:
            Sequence[TextContent | ImageContent | EmbeddedResource]: The result of the
                tool call, wrapped in an appropriate content type (currently only TextContent).

        Raises:
            ValueError: If the tool name is unknown or if there's an error processing the query.
        """
        content: str = ""
        try:
            match name:
                case "search":
                    search_res = await search_discogs(query_dict=arguments, client=dc)
                    content = json.dumps(search_res, indent=4)
                case "get-release-info":
                    release_info = dc.release(arguments["release-id"])
                    release_info.refresh()  # need to refresh because client behaves weirdly
                    content = json.dumps(release_info.data, indent=4)
                case _:
                    raise ValueError(f"Unknown tool: {name!s}")
            return [TextContent(type="text", text=content)]
        except ValueError as err:
            raise ValueError(f"Error processing query {err!s}") from err

    @mcp.list_resources()
    async def handle_list_resources() -> list[Resource]:
        """
        List the available resources provided by this MCP server.

        This callback function is registered with the MCP server to handle
        resource listing requests. It defines and returns the available resources
        that can be accessed by clients.

        Returns:
            list[Resource]: A list containing the available resources, currently only
                the 'discogs-user-info' resource.
        """
        return [
            Resource(
                uri=AnyUrl("data://discogs/userinfo"),
                name="discogs-user-info",
                description="Returns all relevant information of the discogs user currently authenticated",
                mimeType="application/json",
            )
        ]

    @mcp.read_resource()
    async def handle_read_resource(uri: str) -> str:
        """
        Handle resource read requests from clients.

        This callback function is registered with the MCP server to handle
        resource read requests. It retrieves the requested resource based on the URI.

        Args:
            uri: The URI of the resource to read.

        Returns:
            str: The JSON-serialized content of the requested resource.

        Raises:
            ValueError: If the resource URI is unknown or if there's an error processing the query.
        """
        try:
            match str(uri):
                case "data://discogs/userinfo":
                    content_raw = await get_user_info_discogs(client=dc)
                    return json.dumps(content_raw, indent=4)
                case _:
                    raise ValueError(f"Unknown resource: {uri!s}")
        except ValueError as err:
            raise ValueError(f"Error processing query {err!s}") from err

    options: InitializationOptions = mcp.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await mcp.run(read_stream, write_stream, options)


async def get_user_info_discogs(client: Client) -> list[dict[str, dict[Any, Any]]]:
    """
    Retrieve information about the authenticated Discogs user.

    This function fetches the user's identity information and collection value
    statistics from the Discogs API.

    Args:
        client: An authenticated Discogs client instance.

    Returns:
        list[dict[str, dict[Any, Any]]]: A list containing a dictionary with user
            information and collection value statistics.

    Note:
        The function refreshes the user_info object because the Discogs client
        sometimes returns incomplete data without refreshing.
    """
    user_info: User = client.identity()
    uinf: dict = {}

    user_info.refresh()  # need to refresh because client behaves weirdly
    for k, v in user_info.data.items():
        uinf[k] = v
    return [
        {
            "user_info": uinf,
            "user_collection": {
                "collection_value": {
                    "maximum": user_info.collection_value.maximum,
                    "median": user_info.collection_value.median,
                    "minimum": user_info.collection_value.minimum,
                }
            },
        }
    ]


async def search_discogs(query_dict: dict[str, str], client: Client) -> list[dict]:
    """
    Search the Discogs database using the provided query parameters.

    This function performs a search on Discogs with the given query parameters
    and returns the first page of results.

    Args:
        query_dict: A dictionary containing search parameters. Must include at
            least a 'query' key. May include other parameters like 'type',
            'artist', 'title', etc.
        client: An authenticated Discogs client instance.

    Returns:
        list[dict]: A list of dictionaries, each representing a search result
            from Discogs.
    """
    single_result: dict = {}
    result: list = []
    result_raw: MixedPaginatedList = client.search(**query_dict)
    for res in result_raw.page(1):
        for k, v in res.data.items():
            single_result[k] = v
        result.append(single_result)
    return result
