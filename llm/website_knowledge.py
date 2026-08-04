from urllib.parse import urlparse

from llm.models import slugify_task_name
from llm.scraper import fetch_website_links

MIN_CONTENT_LENGTH = 100


def _normalize_netloc(netloc: str) -> str:
    netloc = netloc.lower()
    if netloc.startswith("www."):
        return netloc[4:]
    return netloc


def same_domain_links(root_url: str, links: list[str]) -> list[str]:
    root_netloc = _normalize_netloc(urlparse(root_url).netloc)
    filtered: list[str] = []
    seen: set[str] = set()

    for link in links:
        link_netloc = _normalize_netloc(urlparse(link).netloc)
        if link_netloc != root_netloc:
            continue
        if link in seen:
            continue
        seen.add(link)
        filtered.append(link)

    return filtered


def discover_links(root_url: str) -> list[str]:
    root_url = root_url.strip()
    links = fetch_website_links(root_url)
    same_domain = same_domain_links(root_url, links)

    if root_url not in same_domain:
        same_domain.insert(0, root_url)

    return same_domain


def parse_page_title(raw_content: str) -> str:
    if "\n\n" in raw_content:
        return raw_content.split("\n\n", 1)[0].strip()
    first_line = raw_content.strip().split("\n", 1)[0]
    return first_line.strip() or "Untitled page"


def parse_page_body(raw_content: str) -> str:
    if "\n\n" in raw_content:
        return raw_content.split("\n\n", 1)[1].strip()
    lines = raw_content.strip().split("\n")
    if len(lines) > 1:
        return "\n".join(lines[1:]).strip()
    return raw_content.strip()


def website_source_id(url: str) -> str:
    parsed = urlparse(url)
    slug_source = f"{parsed.netloc}{parsed.path}".strip("/")
    slug = slugify_task_name(slug_source.replace("/", "_").replace(".", "_"))
    return f"knowledge:web:{slug or 'page'}"


def is_fetch_error(content: str) -> bool:
    return content.startswith("Error") or content.startswith("Non-HTML")


def is_usable_content(content: str) -> bool:
    if is_fetch_error(content):
        return False
    body = parse_page_body(content)
    return len(body.strip()) >= MIN_CONTENT_LENGTH
