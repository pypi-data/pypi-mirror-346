from setuptools import setup, find_packages

setup(
    name="architect-copilot",
    version="0.1.0",
    packages=find_packages(include=["architect_mcp*"]),
    install_requires=[
        "mcp-server",
        "openai",
        "python-dotenv",
        "azure-search-documents",
        "azure-core"
    ],
    entry_points={
        "console_scripts": [
            "architect-copilot=architect_mcp.main:main"
        ]
    },
    author="Your Name",
    description="Architect Copilot MCP tool using Azure OpenAI and Search.",
    python_requires=">=3.7",
)
