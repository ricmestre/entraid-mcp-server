# EntraID MCP Server (Microsoft Graph FastMCP)

This project provides a modular, resource-oriented FastMCP server for interacting with Microsoft Graph API. It is designed for extensibility, maintainability, and security, supporting advanced queries for users, sign-in logs, MFA status, and privileged users.

## Features

- **Modular Resource Structure:**
  - Each resource (users, sign-in logs, MFA, etc.) is implemented in its own module under `src/msgraph_mcp_server/resources/`.
  - Easy to extend with new resources (e.g., groups, devices).
- **Centralized Graph Client:**
  - Handles authentication and client initialization.
  - Shared by all resource modules.
- **Comprehensive User Operations:**
  - Search users by name/email.
  - Get user by ID.
  - List all privileged users (directory role members).
- **Sign-in Log Operations:**
  - Query sign-in logs for a user for the last X days.
- **MFA Operations:**
  - Get MFA status for a user.
  - Get MFA status for all members of a group.
- **Error Handling & Logging:**
  - Consistent error handling and progress reporting via FastMCP context.
  - Detailed logging for troubleshooting.
- **Security:**
  - `.env` and secret files are excluded from version control.
  - Uses Microsoft best practices for authentication.

## Project Structure

```
src/msgraph_mcp_server/
├── auth/           # Authentication logic (GraphAuthManager)
├── resources/      # Resource modules (users, signin_logs, mfa, ...)
├── utils/          # Core GraphClient
├── server.py       # FastMCP server entry point (registers tools/resources)
├── __init__.py     # Package marker
```

## Usage

### 1. Setup
- Clone the repo.
- Create a `config/.env` file with your Azure AD credentials:
  ```
  TENANT_ID=your-tenant-id
  CLIENT_ID=your-client-id
  CLIENT_SECRET=your-client-secret
  ```
- (Optional) Set up certificate-based auth if needed.

### 2. Testing & Development

You can test and develop your MCP server directly using the FastMCP CLI:

```bash
fastmcp dev '/path/to/src/msgraph_mcp_server/server.py'
```

This launches an interactive development environment with the MCP Inspector. For more information and advanced usage, see the [FastMCP documentation](https://github.com/jlowin/fastmcp).

### 3. Available Tools

#### User Tools
- `search_users(query, ctx, limit=10)` — Search users by name/email
- `get_user_by_id(user_id, ctx)` — Get user details by ID
- `get_privileged_users(ctx)` — List all users in privileged directory roles
- `get_user_roles(user_id, ctx)` — Get all directory roles assigned to a user
- `get_user_groups(user_id, ctx)` — Get all groups (including transitive memberships) for a user

#### Group Tools
- `get_all_groups(limit=100)` — Get all groups (with paging)
- `search_groups_by_name(name, limit=50)` — Search for groups by display name
- `get_group_members(group_id, limit=100)` — Get members of a group by group ID

#### Sign-in Log Tools
- `get_user_sign_ins(user_id, ctx, days=7)` — Get sign-in logs for a user

#### MFA Tools
- `get_user_mfa_status(user_id, ctx)` — Get MFA status for a user
- `get_group_mfa_status(group_id, ctx)` — Get MFA status for all group members

#### Device Tools
- `get_all_managed_devices(filter_os=None)` — Get all managed devices (optionally filter by OS)
- `get_managed_devices_by_user(user_id)` — Get all managed devices for a specific user

#### Conditional Access Policy Tools
- `get_conditional_access_policies(ctx)` — Get all conditional access policies
- `get_conditional_access_policy_by_id(policy_id, ctx)` — Get a single conditional access policy by its ID

#### Audit Log Tools
- `get_user_audit_logs(user_id, days=30)` — Get all relevant directory audit logs for a user by user_id within the last N days

#### Example Resource
- `greeting://{name}` — Returns a personalized greeting

## Extending the Server
- Add new resource modules under `resources/` (e.g., `groups.py`, `devices.py`).
- Register new tools in `server.py` using the FastMCP `@mcp.tool()` decorator.
- Use the shared `GraphClient` for all API calls.

## Security & Best Practices
- **Never commit secrets:** `.env` and other sensitive files are gitignored.
- **Use least privilege:** Grant only the necessary Microsoft Graph permissions to your Azure AD app.
- **Audit & monitor:** Use the logging output for troubleshooting and monitoring.

## Required Graph API Permissions
| API / Permission            | Type        | Description                               |
|-----------------------------|-------------|-------------------------------------------|
| AuditLog.Read.All           | Application | Read all audit log data                   |
| AuthenticationContext.Read.All | Application | Read all authentication context information |
| DeviceManagementManagedDevices.Read.All | Application | Read Microsoft Intune devices |
| Directory.Read.All          | Application | Read directory data                       |
| Group.Read.All              | Application | Read all groups                           |
| GroupMember.Read.All        | Application | Read all group memberships                |
| Policy.Read.All             | Application | Read your organization's policies         |
| RoleManagement.Read.Directory | Application | Read all directory RBAC settings        |
| User.Read.All               | Application | Read all users' full profiles             |
| UserAuthenticationMethod.Read.All | Application | Read all users' authentication methods |

## Advanced: Using with Claude or Cursor

### Using with Claude (Anthropic)
To install and run this server as a Claude MCP tool, use:

```bash
fastmcp install '/path/to/src/msgraph_mcp_server/server.py' \
  --with msgraph-sdk --with azure-identity --with azure-core --with msgraph-core \
  -f /path/to/.env
```
- Replace `/path/to/` with your actual project path.
- The `-f` flag points to your `.env` file (never commit secrets!).

### Using with Cursor
Add the following to your `.cursor/mcp.json` (do **not** include actual secrets in version control):

```json
{
  "EntraID MCP Server": {
    "command": "uv",
    "args": [
      "run",
      "--with", "azure-core",
      "--with", "azure-identity",
      "--with", "fastmcp",
      "--with", "msgraph-core",
      "--with", "msgraph-sdk",
      "fastmcp",
      "run",
      "/path/to/src/msgraph_mcp_server/server.py"
    ],
    "env": {
      "TENANT_ID": "<your-tenant-id>",
      "CLIENT_ID": "<your-client-id>",
      "CLIENT_SECRET": "<your-client-secret>"
    }
  }
}
```
- Replace `/path/to/` and the environment variables with your actual values.
- **Never commit real secrets to your repository!**

## License

MIT
