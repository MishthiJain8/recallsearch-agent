import json
import os
import sqlite3
import time
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

DB = Path(__file__).with_name("search_cache.sqlite3")
TTL = 1800

def web_search(query):
    key = query.strip().casefold()
    now = int(time.time())

    with sqlite3.connect(DB) as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS cache (
                query TEXT PRIMARY KEY,
                saved_at INTEGER,
                response TEXT
            )
        """)
        cached = db.execute(
            "SELECT saved_at, response FROM cache WHERE query=?",
            (key,)
        ).fetchone()

    if cached and now - cached[0] < TTL:
        return json.loads(cached[1])

    api_key = os.getenv("TAVILY_API_KEY", "").strip()

    headers = {
        "Content-Type": "application/json"
    }

    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    else:
        headers["X-Tavily-Access-Mode"] = "keyless"

    body = json.dumps({
        "query": query,
        "search_depth": "basic",
        "max_results": 5,
        "include_answer": "basic"
    }).encode("utf-8")

    request = Request(
        "https://api.tavily.com/search",
        data=body,
        headers=headers,
        method="POST"
    )

    try:
        with urlopen(request, timeout=25) as response:
            data = json.load(response)
    except HTTPError as error:
        if error.code in (401, 403, 429):
            raise RuntimeError(
                "Tavily free search limit or access restriction. "
                "Try later or use a free Tavily API key."
            ) from error
        raise RuntimeError(
            f"Tavily returned HTTP {error.code}"
        ) from error
    except (URLError, TimeoutError) as error:
        raise RuntimeError(
            "Could not connect to the search service."
        ) from error

    results = {
        "answer": data.get("answer") or "",
        "results": [
            {
                "title": item.get("title") or "Source",
                "url": item.get("url") or "",
                "content": item.get("content") or ""
            }
            for item in data.get("results", [])
            if item.get("url")
        ]
    }

    if not results["results"]:
        raise RuntimeError("Search returned no sources.")

    with sqlite3.connect(DB) as db:
        db.execute(
            "INSERT OR REPLACE INTO cache VALUES (?, ?, ?)",
            (key, now, json.dumps(results))
        )

    return results
