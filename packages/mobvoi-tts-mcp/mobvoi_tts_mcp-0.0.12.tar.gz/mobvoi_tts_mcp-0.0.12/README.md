![Mobvoi Logo](.assets/logo.jpeg)

<p align="center">
  Official Mobvoi TTS <a href="https://github.com/modelcontextprotocol">Model Context Protocol (MCP)</a> server that enables interaction with Mobvoi powerful Text to Speech, Voice Clone APIs. This server allows MCP clients like <a href="https://www.anthropic.com/claude">Claude Desktop</a>, <a href="https://www.cursor.so">Cursor</a>, <a href="https://cline.bot/">Cline</a> </a> and other Client to generate speech, clone voices, and more.
</p>

## Quickstart with Claude Desktop

1. Get your APP_KEY and APP_SECRET from [Mobvoi Sequence Monkey open platform](https://openapi.moyin.com/user/mine-app-detail). New users can claim a free quota.
2. Install `uv` (Python package manager), install with `pip install uv` or see the `uv` [repo](https://github.com/astral-sh/uv) for additional install methods.
3. Go to Cursor -> Cursor Settings -> MCP, click `Add new global MCP server`, and mcp.json will open, paste the following config content:

```
"MobvoiTTS": {
        "command": "uvx",
        "args": [
          "--index", 
          "https://pypi.tuna.tsinghua.edu.cn/simple",
          "mobvoi-tts-mcp"
        ],
        "env": {
          "APP_KEY": "<insert-your-APP_KEY-here>",
          "APP_SECRET": "<insert-your-APP_SECRET-here>"
        },
      },
```

For MacOS and Linux systems, you can refer to the above for configuration. We haven't tested the Windows system yet.

## Troubleshooting

### spawn uvx ENOENT

If you encounter the error "MCP Mobvoi TTS: spawn uvx ENOENT", confirm its absolute path by running this command in your terminal:
`which uvx`
Once you obtain the absolute path (e.g., /usr/local/bin/uvx), update your configuration to use that path (e.g., "command": "/usr/local/bin/uvx"). This ensures that the correct executable is referenced.

### MCP error -32001: Request timed out

If you encounter this error, this indicates that there is a problem with your network. If you are in mainland China, we strongly recommend that you configure extra pypi sources in the following way:

```
"MobvoiTTS": {
        ...
        "args": [
          "--index", 
          "https://pypi.tuna.tsinghua.edu.cn/simple",
          "mobvoi-tts-mcp"
        ],
       ...
      },
```

Note that the extra pypi source needs to be configured at the very front of the args.









