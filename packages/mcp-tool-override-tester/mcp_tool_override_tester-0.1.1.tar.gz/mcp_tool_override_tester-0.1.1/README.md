## MCP Tool Override Server
A Model Context Protocol server implementation that demonstrates how tools can be dynamically overridden across multiple servers.

### Overview
This project implements a Model Context Protocol (MCP) server that registers tools using the same names as existing server tools to demonstrate how tools can be dynamically overridden when a new server is added to the configuration.
- `read_file` from [Filesystem](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem)
- `send_email` from [Gmail MCP Server](https://github.com/GongRzhe/Gmail-MCP-Server)
- `slack_list_channels` from [Slack MCP Server](https://github.com/modelcontextprotocol/servers/tree/main/src/slack)

### How It Works
I simply added an MCP Tool Override tester MCP to mimic the tools of other servers.
Surprisingly, they are easily overriden by the new tools (which are fake).
```
┌───────────┐     ┌────────────────────────────────────┐  
│ MCP Client│     │ MCP Tool Servers                   │  
│  (Claude  │────▶│ - File System MCP                  │  
│  Desktop) │     │    - Tool: read_file, ...          │  
└───────────┘     │ - Gmail MCP                        │  
                  │   - Tool: send_email, ...          │  
                  │ - Slack MCP                        │  
                  │   - Tool: slack_list_channels, ... │  
                  │ - MCP Tool Override Tester         │  
                  │   - Tool: read_file, send_email    │  
                  │        and slack_list_channels     │  
                  └────────────────────────────────────┘  
```
The Claude Desktop still confuses even after all tools of the Override tester MCP are turned off.

### Usage

```JSON
{
  "mcpServers": {
    "slack": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-slack"
      ],
      "env": {
        "SLACK_BOT_TOKEN": "YOUR SLACK BOT TOKEN",
        "SLACK_TEAM_ID": "YOUR SLACK TEAM ID",
        "SLACK_CHANNEL_IDS": "CHANNEL1_ID, CHANNEL2_ID, ..."
      }
    },
    "gmail": {
      "command": "npx",
      "args": [
        "@gongrzhe/server-gmail-autoauth-mcp"
      ]
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/your/directory/path/to/allow"
      ]
    },
    "override_tester": {
      "command": "/path/to/your/uvx",
      "args": [
        "--from",
        "mcp-tool-override-tester",
        "override_mcp_tools"
      ]
    }
  }
}
```

### License
This project is licensed under the MIT License.
