from .weathertest import mcp

def main() -> None:
    print("Hello from mcpserver-zyq!")
    mcp.run(transport='stdio')
