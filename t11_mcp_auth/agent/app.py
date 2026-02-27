import asyncio
import json

from commons.constants import OPENAI_API_KEY, DEFAULT_SYSTEM_PROMPT
from commons.models.message import Message
from commons.models.role import Role
from t11_mcp_auth.agent._agent import AgentMCPAuth
from t11_mcp_auth.agent.mcp_clients.api_key_mcp_client import ApiKeyMCPClient
from t11_mcp_auth.agent.mcp_clients.oauth_mcp_client import OauthHttpMCPClient

MCP_API_KEY: str = "dev-secret-key"

async def main():
    #TODO:
    # 1. Use either `ApiKeyMCPClient(mcp_server_url="http://localhost:8007/mcp", api_key=MCP_API_KEY)`
    #    or `OauthHttpMCPClient(mcp_server_url="http://localhost:8008/mcp")` as an async context manager
    #    (`async with ... as mcp_client:`) — all steps below happen inside this block
    # 2. Get available tools and print each one as indented JSON
    # 3. Create `AgentMCPAuth` with `api_key`, `model`, `tools`, and `mcp_client`
    # 4. Create a `messages` list with a single system `Message`
    # 5. Print a ready message and run an infinite loop:
    #    - Get user input; break if it equals "exit"
    #    - Append a user `Message` to `messages`
    #    - Call `await agent.get_completion(messages)` and append the returned `ai_message`
    raise NotImplementedError()


if __name__ == "__main__":
    asyncio.run(main())