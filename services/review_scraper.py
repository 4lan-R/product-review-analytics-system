"""Scraping helper logic for review ingestion."""
import html
import json
import re
import urllib.error
import urllib.request

from schemas.review import ReviewCreate


def scrape_review_from_link(link: str) -> ReviewCreate:
    """Download a web page and extract review/product metadata."""
    try:
        request = urllib.request.Request(
            link,
            headers={"User-Agent": "Mozilla/5.0 (compatible; review-scraper/1.0)"},
        )
        with urllib.request.urlopen(request, timeout=15) as response:
            content_type = response.headers.get("Content-Type", "")
            if "text/html" not in content_type.lower():
                raise ValueError("URL did not return HTML content")
            html_text = response.read().decode(
                response.headers.get_content_charset("utf-8"),
                errors="ignore",
            )
    except (urllib.error.HTTPError, urllib.error.URLError, ValueError) as exc:
        raise ValueError(f"Unable to fetch review page: {exc}") from exc

    def extract_meta(key: str) -> str | None:
        pattern = fr'<meta[^>]+(?:property|name)=["\']{re.escape(key)}["\'][^>]+content=["\']([^"\']+)["\']'
        match = re.search(pattern, html_text, re.IGNORECASE)
        return match.group(1).strip() if match else None

    title = (
        extract_meta("og:title")
        or extract_meta("twitter:title")
        or None
    )
    if not title:
        title_match = re.search(r"<title[^>]*>(.*?)</title>", html_text, re.IGNORECASE | re.DOTALL)
        title = title_match.group(1).strip() if title_match else None

    description = (
        extract_meta("og:description")
        or extract_meta("twitter:description")
        or extract_meta("description")
        or None
    )

    text = description
    if not text:
        body_match = re.search(r"<body[^>]*>(.*?)</body>", html_text, re.IGNORECASE | re.DOTALL)
        if body_match:
            paragraph_match = re.search(r"<p[^>]*>(.*?)</p>", body_match.group(1), re.IGNORECASE | re.DOTALL)
            if paragraph_match:
                text = paragraph_match.group(1).strip()

    if not title or not text:
        raise ValueError("Unable to extract sufficient review data from the provided link")

    clean_text = re.sub(r"<[^>]+>", "", text)
    clean_text = html.unescape(clean_text).strip()
    if not clean_text:
        raise ValueError("Scraped review text was empty")

    scraped_data = {
        "title": title,
        "text": clean_text,
        "product_name": title,
        "product_description": description or clean_text[:200],
    }

    return ReviewCreate(**scraped_data)
