from __future__ import annotations

import logging
import re
from urllib.parse import urldefrag, urljoin

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,text/plain,text/markdown,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

IRRELEVANT_TAGS = [
    "script",
    "style",
    "img",
    "input",
    "noscript",
    "header",
    "footer",
    "nav",
    "aside",
    "form",
    "button",
    "iframe",
    "svg",
    "canvas",
]

NOISE_CLASS_PATTERN = re.compile(
    r"^(nav|navbar|navigation|sidebar|footer|header|menu|cookie|banner)(-|$)",
    re.IGNORECASE,
)

TEXT_CONTENT_TYPES = ("text/plain", "text/markdown", "text/x-markdown")


def _is_noise_class(class_value) -> bool:
    if not class_value:
        return False
    tokens = class_value if isinstance(class_value, list) else str(class_value).split()
    for token in tokens:
        base = token.split(":")[0].lower()
        if NOISE_CLASS_PATTERN.match(base):
            return True
        if base.startswith(("ad-", "advertisement-")):
            return True
    return False


def _clean_text(text: str) -> str:
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    return "\n".join(lines)


def _extract_html_content(soup: BeautifulSoup) -> tuple[str, str]:
    title = "No title found"
    if soup.title and soup.title.string:
        title = soup.title.get_text(strip=True)

    root = soup.find("main") or soup.find("article") or soup.body
    if root is None:
        return title, ""

    for tag_name in IRRELEVANT_TAGS:
        for tag in root.find_all(tag_name):
            tag.decompose()

    for element in root.find_all(class_=_is_noise_class):
        element.decompose()

    return title, _clean_text(root.get_text(separator="\n", strip=True))


def _fetch_text_response(url: str, response: requests.Response) -> str:
    text = response.text.strip()
    if not text:
        return f"Error: Empty response from {url}"

    lines = text.split("\n", 1)
    title = lines[0].lstrip("#").strip() if lines else "Untitled"
    if title.startswith("Error") or len(title) > 200:
        title = url.rstrip("/").split("/")[-1] or "Untitled"

    return f"{title}\n\n{text}"


def fetch_website_contents(
    url: str,
    max_chars: int = 5_000,
    timeout: int = 15,
) -> str:
    """Return the title and visible text of the website at the given URL."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=timeout)
        response.raise_for_status()
    except requests.Timeout:
        return f"Error: Request timed out after {timeout} seconds for {url}"
    except requests.ConnectionError:
        return f"Error: Could not connect to {url}"
    except requests.RequestException as exc:
        return f"Error fetching {url}: {exc}"

    content_type = response.headers.get("Content-Type", "").lower()

    if any(media in content_type for media in TEXT_CONTENT_TYPES):
        return _fetch_text_response(url, response)[:max_chars]

    if "text/html" not in content_type:
        return f"Non-HTML content at {url} (Content-Type: {content_type})"

    soup = BeautifulSoup(response.text, "html.parser")
    title, text = _extract_html_content(soup)

    if len(text) < 100 and not url.endswith(".md"):
        markdown_url = url.rstrip("/") + ".md"
        try:
            md_response = requests.get(markdown_url, headers=HEADERS, timeout=timeout)
            md_type = md_response.headers.get("Content-Type", "").lower()
            if md_response.ok and any(media in md_type for media in TEXT_CONTENT_TYPES):
                md_content = _fetch_text_response(markdown_url, md_response)
                md_body = md_content.split("\n\n", 1)[1] if "\n\n" in md_content else ""
                if len(md_body) > len(text):
                    return md_content[:max_chars]
        except requests.RequestException:
            pass

    return (title + "\n\n" + text)[:max_chars]


def fetch_website_links(url: str, timeout: int = 15) -> list[str]:
    """Return normalized, absolute links on the website at the given URL."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=timeout)
        response.raise_for_status()
    except requests.RequestException as exc:
        logger.error("Error fetching links from %s: %s", url, exc)
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    links: list[str] = []
    for anchor in soup.find_all("a"):
        href = anchor.get("href")
        if not href:
            continue
        if href.startswith(("mailto:", "tel:", "javascript:", "#")):
            continue

        absolute_url = urljoin(url, href)
        absolute_url, _ = urldefrag(absolute_url)
        links.append(absolute_url)

    seen: set[str] = set()
    unique_links: list[str] = []
    for link in links:
        if link not in seen:
            seen.add(link)
            unique_links.append(link)

    return unique_links
