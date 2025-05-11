# tinyAgent_deepsearch

`tinyAgent_deepsearch` is a Python library designed to facilitate deep research on various topics using AI agents, powered by OpenAI and Firecrawl for web scraping and content analysis. It leverages the `tiny_agent_os` framework for structuring AI agent interactions.

## Features

*   Perform recursive, multi-step research on a given topic.
*   Generate focused search queries based on evolving learnings.
*   Utilize Firecrawl to scrape web content.
*   Employ OpenAI's language models to digest information and identify follow-up questions.
*   Configurable research depth and breadth.

## Installation

You can install `tinyAgent_deepsearch` using pip:

```bash
pip install tinyAgent_deepsearch 
```
*(Note: This command assumes the package will be published to PyPI. For local installation from source, navigate to the project root directory where `pyproject.toml` is located and run `pip install .`)*

## Prerequisites

Before using the library, ensure you have the following API keys set as environment variables:

*   `OPENAI_KEY`: Your API key for OpenAI.
*   `FIRECRAWL_KEY`: Your API key for Firecrawl.

You can set them in your shell environment or by using a `.env` file in your project root (requires `python-dotenv` to be installed in your project).

Example `.env` file:
```
OPENAI_KEY="your_openai_api_key_here"
FIRECRAWL_KEY="your_firecrawl_api_key_here"
```

## Usage

Here's a basic example of how to use the `deep_research` function:

```python
import asyncio
from tinyAgent_deepsearch import deep_research
from dotenv import load_dotenv # Optional: if you use a .env file

async def main():
    # Optional: Load environment variables from .env file
    # load_dotenv()

    topic = "The future of renewable energy sources"
    breadth = 3  # Number of search queries per depth level
    depth = 2    # Number of recursive research levels

    try:
        print(f"Starting deep research on: {topic}")
        results = await deep_research(
            topic=topic,
            breadth=breadth,
            depth=depth,
            llm_model="gpt-4o-mini", # Optional: specify LLM model
            concurrency=2           # Optional: specify concurrency
        )
        print("\n=== Research Complete ===")
        print("\nLearnings:")
        for i, learning in enumerate(results.get("learnings", [])):
            print(f"{i+1}. {learning}")

        print("\nVisited URLs:")
        for i, url in enumerate(results.get("visited", [])):
            print(f"{i+1}. {url}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Configuration

The `deep_research` function accepts the following parameters:

*   `topic` (str): The initial research topic.
*   `breadth` (int): The number of search queries to generate at each depth level.
*   `depth` (int): The number of recursive research levels.
*   `llm_model` (str, optional): The OpenAI model to use. Defaults to `"gpt-4o-mini"`.
*   `concurrency` (int, optional): The maximum number of concurrent search and digest operations. Defaults to `2`.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue. (Further details to be added)

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.