"""Example MCP server implementation."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from typing import Any

app = FastAPI()

class ScraperInput(BaseModel):
    url: str

class ScrapeHtmlArguments(BaseModel):
    input: ScraperInput


@app.get("/tools")
async def get_tools():
    """Return the list of available tools."""
    return {
        "tools": [
            {
                "description": "Scrape HTML content from a URL.\n\n    This function fetches the HTML content from a given URL using httpx.\n    It handles redirects and raises appropriate exceptions for HTTP errors.\n\n    Args:\n        input (ScrapeHtmlInput): The input containing the URL to scrape\n\n    Returns:\n        ScrapeHtmlOutput: The HTML content of the page\n\n    Raises:\n        httpx.HTTPError: If there's an HTTP error while fetching the page\n        Exception: For any other unexpected errors\n    ",
                "input_schema": {
                    "$defs": {
                        "ScrapeHtmlInput": {
                            "properties": {
                                "url": {
                                    "description": "The URL to scrape HTML from",
                                    "minLength": 1,
                                    "title": "Url",
                                    "type": "string",
                                }
                            },
                            "required": ["url"],
                            "title": "ScrapeHtmlInput",
                            "type": "object",
                        }
                    },
                    "properties": {"input": {"$ref": "#/$defs/ScrapeHtmlInput"}},
                    "required": ["input"],
                    "title": "scrape_htmlArguments",
                    "type": "object",
                },
                "internal_url": "http://localhost:8000/tools/scrape_html/invoke",
                "name": "scrape_html",
                "service": "html-structure-analyser",
                "strict": True,
            }
        ]
    }


@app.post("/tools/scrape_html/invoke")
async def scrape_html(arguments: ScrapeHtmlArguments):
    sample_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sample Page</title>
    </head>
    <body>
        <header>
            <h1>Welcome to Sample Page</h1>
            <nav>
                <ul>
                    <li><a href="#home">Home</a></li>
                    <li><a href="#about">About</a></li>
                    <li><a href="#contact">Contact</a></li>
                </ul>
            </nav>
        </header>
        <main>
            <section id="content">
                <h2>Main Content</h2>
                <p>This is a sample HTML page that was scraped from {arguments.input.url}</p>
                <article>
                    <h3>Article Title</h3>
                    <p>This is a sample article with some content.</p>
                </article>
            </section>
        </main>
        <footer>
            <p>&copy; 2024 Sample Website</p>
        </footer>
    </body>
    </html>
    """
    return sample_html

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 
