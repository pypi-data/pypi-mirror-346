"""
Discogs MCP Server package.

This package provides a Model Context Protocol (MCP) server for interacting with
the Discogs API. It allows searching the Discogs database and retrieving user information.
"""

import asyncio

from mcp_server_discogs.server import serve


def main() -> None:
    """
    Entry point function for running the Discogs MCP server.

    This function initializes and runs the server using asyncio.

    Returns:
        None
    """
    asyncio.run(serve())


if __name__ == "__main__":
    main()
