import os
import sys
import asyncio
import json
from pathlib import Path

from mcp import Resource
from mcp.types import Prompt

from commons.constants import OPENAI_API_KEY
from commons.models.message import Message
from commons.models.role import Role
from t9_mcp_fundamentals.agent.agent import AgentMCPFundamentals
from t9_mcp_fundamentals.agent.mcp_clients.http import HttpMCPClient
from t9_mcp_fundamentals.agent.mcp_clients.stdio import StdioMCPClient
from t9_mcp_fundamentals.agent.prompts import SYSTEM_PROMPT


async def main():
    #TODO:
    # 1. Create `HttpMCPClient(mcp_server_url="http://localhost:8005/mcp")` as an async context manager
    #    (`async with ... as mcp_client:`) — all steps below happen inside this block
    # 2. Print Available Resources
    # 3. Print Available Tools
    # 4. Create `AgentMCPFundamentals`
    # 5. Create `messages` list with a single system prompt
    # 6. Print Available Prompts
    # 7. Run an infinite loop:
    #    - get user input with `input("\n> ").strip()`
    #    - if user_input.lower() == 'exit': break
    #    - append Message(role=Role.USER, content=user_input) to `messages`
    #    - call `await agent.get_response(messages)` and append the returned `ai_message` to `messages`
    raise NotImplementedError()


if __name__ == "__main__":
    asyncio.run(main())
