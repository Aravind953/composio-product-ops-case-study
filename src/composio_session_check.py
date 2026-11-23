import os
from dotenv import load_dotenv
from composio import Composio

load_dotenv()
if not os.getenv("COMPOSIO_API_KEY"):
    raise SystemExit("Add COMPOSIO_API_KEY to your local .env file.")
client = Composio()
session = client.sessions.create(user_id="composio-app-research", mcp=True)
print("Session created:", session.session_id)
print("MCP URL:", session.mcp.url)
print("Do not print or commit MCP headers or API keys.")
