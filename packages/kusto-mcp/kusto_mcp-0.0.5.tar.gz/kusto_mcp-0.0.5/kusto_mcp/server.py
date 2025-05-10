import sys
from kusto_mcp import __version__


def main():
    print("Starting Kusto MCP server")
    print("Version:", __version__)
    print("Python version:", sys.version)
    print("Platform:", sys.platform)

    # import later to allow for environment variables to be set from command line
    from kusto_mcp.kusto_service import mcp

    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
