# client is ollama
import json
import ollama
from fastmcp import Client as MCPClient
import asyncio
import sys

#config
OLLAMA_MODEL = "llama3.2"
MCP_SERVER_URL = "http://127.0.0.1:8080/mcp"

#Step 1: discover tools from MCP server
async def load_mcp_tools():
    """Connect to MCP server and get list of tools"""
    try:
        async with MCPClient(MCP_SERVER_URL) as mcp:
            #asks the server what tools are there
            tools_list = await mcp.list_tools()

            #convert and make ollama understand
            ollama_tools = []
            for tool in tools_list:
                ollama_tools.append({
                    "type": "function", 
                    "function": {
                        "name": tool.name,
                        "description": tool.description, 
                        "parameters": tool.inputSchema,
                    },
                })
            return ollama_tools
    except Exception as e:
        print(f"Error connectiong to MCP server: {e}")
        print(f"\nmake sure the server is running")
        print("  python mcp_server.py")
        sys.exit(1)
    