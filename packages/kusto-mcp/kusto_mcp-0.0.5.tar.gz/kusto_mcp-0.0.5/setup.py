from setuptools import setup, find_packages
import os
from pathlib import Path

def get_platform_binaries():
    """Get the list of binary files for the current platform."""
    bin_dir = Path("kusto_mcp/bin")
    if not bin_dir.exists():
        return []
    return [str(path.relative_to("kusto_mcp")) for path in bin_dir.glob("*")]

setup(
    name="kusto-mcp",
    packages=find_packages(),
    package_data={
        "kusto_mcp": get_platform_binaries()
    },
    include_package_data=True,
    platform="win_amd64",  # Specify Windows AMD64 platform
)
