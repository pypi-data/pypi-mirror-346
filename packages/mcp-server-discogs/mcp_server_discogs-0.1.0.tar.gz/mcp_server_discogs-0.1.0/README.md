# MCP Server Discogs

A Model Context Protocol (MCP) server for interacting with the Discogs API. This server allows searching the Discogs database and retrieving user information.

## Konwn issues
- searches can be very expensive, there is simply too much data coming back. Also search pagination is NOT used, the search currently looks only at the first page of results.

## Features

- **Search Discogs**: Search for releases, masters, artists, or labels using various filters
- **User Info**: Retrieve authenticated user information including collection value statistics
- **MCP Integration**: Use with Claude, GPT or other MCP-compatible AI assistants

## Prerequisites

- Python 3.13 or higher
- Discogs API token ([Get one here](https://www.discogs.com/settings/developers))
- For MCP Inspector: Node.js (as a development dependency)
- For Open WebUI integration: mcpo package

## Installation

### From Source

1. Clone the repository:
   ```bash
   git clone https://gitlab.com/konstantinpae/mcp-server-discogs.git
   cd /path/to/mcp-server-discogs
   ```

2. Create and activate a virtual environment:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install the package in development mode:
   ```bash
   uv sync
   ```

## Usage

### Basic Usage

1. Set your Discogs API token as an environment variable:
   ```bash
   export DISCOGS_API_TOKEN="your_discogs_api_token"
   ```

2. Run the MCP server:
   ```bash
   uvx --refresh /path/to/mcp-server-discogs
   ```
   > Note: --refresh rebuilds the package on every start

### Usage with Claud, Cline or anything supporting MCP

1. Go to the settings file for your MCP server, it should look something like this
   ```json
   {
      "mcpServers": {
         "mcp-server1": {...}, 
         "mcp-server2": {...},    
      }
   }
   ```
   Add the following, so it looks something like this
   ```json
   {
      "mcpServers": {
         "mcp-server1": {...}, 
         "mcp-server2": {...},
         "discogs-mcp-server": {
            "disabled": false,
            "timeout": 300,
            "command": "uvx",
            "args": [
               "/path/to/mcp-server-discogs"
            ],
            "env": {
               "DISCOGS_API_TOKEN": "your_discogs_api_token"
            }
         }              
      }
   }
   ```
2. You should now be able to use the MCP server from your client of choice.

### Using with MCP Inspector

The MCP Inspector provides a UI for testing and inspecting the server's capabilities.

1. Install the MCP Inspector (if not already installed):
   ```bash
   npm install -g @modelcontextprotocol/inspector
   ```

2. Run the MCP server with Inspector:
   ```bash
   env DISCOGS_API_TOKEN="YOUR_API_TOKEN" npx @modelcontextprotocol/inspector uvx --refresh /path/to/mcp-server-discogs
   ```

### Using with Open WebUI

> Known Issue: mcpo only implements tools but not resources, so user-info will not work!

To integrate with Open WebUI, you'll need the ([mcpo](https://www.discogs.com/settings/developers)) package:

1. In the repository, run:
   ```bash
   uvx mcpo --port 8000 --api-key "ANY API KEY" -- uvx /path/to/mcp-server-discogs
   ```
   > Note: Set any API key here, you will need it for setup with Open Web UI

2. Configure Open WebUI to use this MCP server (refer to Open WebUI documentation for specific steps)

## Server Capabilities

### Tools

#### search

Searches Discogs for a given search string and returns results.

**Parameters:**
- `query` (required): The search string to be used in the search
- `type`: The type of the query can be 'release', 'master', 'artist' or 'label'
- `title`: Search by combined "Artist Name - Release Title" title field
- `release_title`: Search release titles
- `credit`: Search release credits
- `artist`: Search artist names
- `anv`: Search artist ANV
- `label`: Search label names
- `genre`: Search genres
- `style`: Search styles
- `country`: Search release country
- `year`: Search release year
- `format`: Search formats
- `catno`: Search catalog number
- `barcode`: Search barcodes
- `track`: Search track titles
- `submitter`: Search submitter username
- `contributor`: Search contributor usernames

### Resources

#### discogs-user-info

Returns all relevant information of the Discogs user currently authenticated.

**URI:** `data://discogs/userinfo`

## Development

### Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/mcp-server-discogs.git
   cd /path/to/repository
   ```

2. Create and activate a virtual environment:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install development dependencies:
   ```bash
   uv pip install -e .
   uv pip install bandit mypy pytest pytest-cov ruff
   ```

4. Install Node.js (required for MCP Inspector):
   ```bash
   # Using nvm (recommended)
   nvm install node
   # Or download from https://nodejs.org/
   ```

### Running Tests


```bash
uv run pytest
```

### Code Quality

The project uses several tools to maintain code quality:

- **ruff**: For linting and formatting
  ```bash
  uv run ruff check 
  uv run ruff format 
  ```

- **mypy**: For type checking
  ```bash
  uv run mypy . --follow-untyped-imports # we need this as the discogs client doesn't offer stubs
  ```

- **bandit**: For security analysis
  ```bash
  uv run bandit -c pyproject.toml -r .
  ```

## License

See the [LICENSE](LICENSE) file for details.

## Acknowledgements
- [Discogs Client](https://github.com/joalla/discogs_client) by the [Joalla Team](https://github.com/joalla) 

## TODO
- [ ] Unit Tests  
- [ ] More functionality  
- [ ] Optimization of the search function  