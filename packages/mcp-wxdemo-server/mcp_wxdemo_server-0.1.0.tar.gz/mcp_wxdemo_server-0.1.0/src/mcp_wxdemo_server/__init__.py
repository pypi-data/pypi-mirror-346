from .testmcp import mcp
def main() -> None:
    print("Hello from mcp-wxdemo-server!")
    mcp.run(transport='stdio')