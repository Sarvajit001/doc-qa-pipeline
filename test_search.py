import os
from dotenv import load_dotenv
try:
    from tavily import TavilyClient  # pyright: ignore[reportMissingImports]
except ImportError as exc:
    raise ImportError(
        "The Tavily client is not installed. Run: pip install tavily-python"
    ) from exc

load_dotenv()

tavily = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)

response = tavily.search(
    query="latest Nepal flood news",
    max_results=5
)

for result in response["results"]:
    print("TITLE:", result["title"])
    print("URL:", result["url"])
    print("CONTENT:", result["content"])
    print("-" * 80)