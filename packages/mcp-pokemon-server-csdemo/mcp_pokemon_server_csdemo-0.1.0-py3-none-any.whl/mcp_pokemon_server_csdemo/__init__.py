from .zekang import mcp


def main() -> None:
    print("Hello from mcp-pokemon-server-csdemo!")
    mcp.run(transport='stdio')
