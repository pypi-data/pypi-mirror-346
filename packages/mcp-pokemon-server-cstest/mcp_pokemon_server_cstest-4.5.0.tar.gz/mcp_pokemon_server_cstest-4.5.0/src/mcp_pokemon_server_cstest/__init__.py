from .zekang import mcp
def main() -> None:
    print("Hello from mcp-pokemon-server-cstest!")
    mcp.run(transport='stdio')
