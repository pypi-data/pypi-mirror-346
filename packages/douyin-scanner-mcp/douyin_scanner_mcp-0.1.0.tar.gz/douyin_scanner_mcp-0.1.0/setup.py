from setuptools import setup, find_packages

setup(
    name="douyin-scanner-mcp",
    version="0.1.0",
    description="MCP client for Douyin Scanner",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "pydantic>=2.0.0",
        "rich>=13.6.0",
        "typer>=0.9.0",
        "httpx>=0.24.0",
        "aiohttp>=3.8.5",
        "asyncio>=3.4.3",
        "fastmcp>=0.1.0"  # Added this requirement
    ],
    entry_points={
        'console_scripts': [
            'douyin-scanner-mcp=douyin_scanner_mcp.main:run_mcp',
        ],
    },
) 