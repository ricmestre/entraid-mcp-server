# Microsoft Graph MCP Server

A FastMCP server implementation that provides tools and resources for interacting with Microsoft Graph services using the Machine Communication Protocol (MCP).

## Features

- Authentication with Microsoft Graph API via Azure Identity
- User profile operations (get current user, search users)
- Email operations (send emails)
- Resource templates for accessing Microsoft Graph entities

## Requirements

- Python 3.8+
- UV package manager

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/entraid-mcp-server.git
   cd entraid-mcp-server
   ```

2. Set up a virtual environment with UV:
   ```
   pip install uv
   uv venv
   ```

3. Activate the virtual environment:
   - On Windows: `.venv\Scripts\activate`
   - On macOS/Linux: `source .venv/bin/activate`

4. Install the dependencies:
   ```
   uv pip install -r requirements.txt
   ```

## Authentication

The server supports authentication using:

1. **Environment Variables**:
   ```
   export GRAPH_TENANT_ID=your_tenant_id
   export GRAPH_CLIENT_ID=your_client_id
   export GRAPH_CLIENT_SECRET=your_client_secret
   ```

2. **Command Line Arguments**:
   ```
   python main.py --tenant-id=your_tenant_id --client-id=your_client_id --client-secret=your_client_secret
   ```

3. **Passing Directly to the Server**:
   ```python
   from src.msgraph_mcp_server.server import create_server
   
   server = create_server(
       tenant_id="your_tenant_id",
       client_id="your_client_id",
       client_secret="your_client_secret"
   )
   server.run()
   ```

## Usage

### Running the Server

Run the server using the main script:

```
python main.py
```

By default, the server uses the stdio transport. To use SSE transport:

```
python main.py --transport=sse --host=127.0.0.1 --port=5000
```

### Available Tools

- `get_current_user`: Get the current user's profile information
- `search_users`: Search for users by name or email
- `send_email`: Send an email

### Available Resources

- `user://me`: Get the current user's profile
- `user://{user_id}`: Get a user's profile by ID

## Development

To add more tools and resources:

1. Add new tool methods in the `_register_tools` method in `src/msgraph_mcp_server/server.py`
2. Add new resource methods in the `_register_resources` method
3. Add new Graph API functionality in `src/msgraph_mcp_server/utils/graph_client.py`

## License

MIT
