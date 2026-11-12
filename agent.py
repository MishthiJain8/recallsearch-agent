import re
from datetime import datetime
from zoneinfo import ZoneInfo
from search_cache import web_search

def answer(question, previous):
    q = question.lower()

    recall_phrases = (
        "what did i ask",
        "my previous question",
        "my last question",
        "my earlier question",
        "when did i ask",
        "what was my previous"
    )

    if any(phrase in q for phrase in recall_phrases):
        questions = [
            (text, timestamp)
            for role, text, timestamp in previous
            if role == "user"
        ]

        if not questions:
            return "You haven't asked anything earlier.", []

        text, timestamp = questions[-1]
        local = datetime.fromisoformat(
            timestamp
        ).astimezone(ZoneInfo("Asia/Kolkata"))

        return (
            f'Your previous question was: "{text}"\n\n'
            f'You asked it on '
            f'{local.strftime("%d %B %Y at %I:%M:%S %p IST")}.',
            []
        )

    query = question

    prior_questions = [
        text for role, text, _ in previous
        if role == "user"
    ]

    if prior_questions and (
        len(question.split()) < 6
        or re.search(
            r"\b(it|they|that|those|this|their)\b",
            q
        )
    ):
        query = prior_questions[-1] + " " + question

    try:
        data = web_search(query)
    except Exception as error:
        return f"Search unavailable: {error}", []

    sources = [
        (item["title"], item["url"])
        for item in data["results"]
    ]

    summary = data.get("answer", "").strip()

    if summary:
        response = (
            "Search-backed answer:\n\n"
            + summary
        )
    else:
        lines = []
        for i, item in enumerate(data["results"][:3], 1):
            lines.append(
                f'[{i}] {item["title"]}\n\n'
                f'{item["content"][:500]}'
            )

        response = (
            "Here's what the web search found. "
            "These excerpts are not independently verified:\n\n"
            + "\n\n".join(lines)
        )

    return response, sources
