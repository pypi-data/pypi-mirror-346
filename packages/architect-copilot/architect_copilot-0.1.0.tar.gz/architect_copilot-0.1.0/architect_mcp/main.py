"""
Architect Copilot MCP Server

This module implements a server that uses Azure OpenAI and Azure Search
to provide architecture guidance based on organizational knowledge.
"""
import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI

# Load .env
load_dotenv()

# === Azure Search Setup ===
search_client = SearchClient(
    endpoint=f"https://{os.getenv('AZURE_SEARCH_SERVICE')}.search.windows.net",
    index_name=os.getenv("AZURE_SEARCH_INDEX"),
    credential=AzureKeyCredential(os.getenv("AZURE_SEARCH_KEY"))
)

# === Azure OpenAI Client Setup ===
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_PREVIEW_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

# === MCP Server Setup ===
mcp = FastMCP(
    name="architect-copilot",
    host="127.0.0.1",
    port=5001,
    timeout=30
)

@mcp.tool()
def answer_architect_question(question: str) -> str:
    """Answer questions using grounded data via Azure AI Search and OpenAI."""
    try:
        results = search_client.search(question, top=3)
        context_chunks = []

        for result in results:
            snippet = result.get('content') or result.get('text') or str(result)
            context_chunks.append(snippet.strip())

        context = "\n\n".join(context_chunks)

        prompt = f"""
You are Architect Copilot. Use the following context to answer the question below.

### Context:
{context}

### Question:
{question}

### Answer:
"""

        response = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_MODEL_NAME", "gpt-4o"),
            messages=[{"role": "user", "content": prompt}],
            temperature=float(os.getenv("AZURE_OPENAI_TEMPERATURE", "0")),
            top_p=float(os.getenv("AZURE_OPENAI_TOP_P", "1.0")),
            max_tokens=int(os.getenv("AZURE_OPENAI_MAX_TOKENS", "1000"))
        )

        return response.choices[0].message.content

    except (ValueError, KeyError, RuntimeError) as e:  # Replace with specific exceptions
        return f"Error during processing: {e}"

def main():
    print("Starting MCP server 'architect-copilot'...")
    mcp.run()


