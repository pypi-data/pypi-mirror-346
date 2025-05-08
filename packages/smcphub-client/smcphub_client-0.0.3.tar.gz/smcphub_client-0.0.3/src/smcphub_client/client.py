import asyncio
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from dotenv import load_dotenv
import os

load_dotenv()  # load environment variables from .env

class SmcphubClient:
    def __init__(self, url = '', api_key = '', env = {}):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.url = url
        self.api_key = api_key

    async def connect(self, command = 'uvx', args = ['smcphub-server'], env = {}):
        """Connect to an MCP server

        Args:
            options: include command, args and environment variables
        """

        # Connect to the server
        env = {**os.environ, **env}
        server_params = StdioServerParameters(
            command=command,
            args=args,
            env=env
        )
        
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
        
        await self.session.initialize()
        # List available tools
        response = await self.session.list_tools()
        tools = response.tools
        
        return tools

    async def callTool(self, name = '', args = {}):
        """Call a tool

        Args:
            name(str): name of the tool
            args(dict): arguments to pass to the tool
        """
        result = await self.session.call_tool(name, args)

        return result.content

    async def close(self):
        """Close the connection to the server
        """
        await self.exit_stack.aclose()