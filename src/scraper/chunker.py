import re
from bs4 import BeautifulSoup

MAX_CHUNK_CHARS = 2000  # ~500 tokens
OVERLAP_CHARS = 200     # ~50 tokens

def recursive_character_split(text: str, max_chars: int = MAX_CHUNK_CHARS, overlap: int = OVERLAP_CHARS) -> list:
    """
    Recursively splits long unstructured text into chunks of at most max_chars
    with overlap characters between adjacent chunks.
    """
    if len(text) <= max_chars:
        return [text]

    chunks = []
    start = 0
    while start < len(text):
        end = start + max_chars
        if end >= len(text):
            chunks.append(text[start:])
            break

        cut_point = text.rfind("\n\n", start, end)
        if cut_point == -1 or cut_point < start + max_chars // 2:
            cut_point = text.rfind(". ", start, end)
        if cut_point == -1 or cut_point < start + max_chars // 2:
            cut_point = text.rfind(" ", start, end)
        if cut_point == -1:
            cut_point = end
        else:
            cut_point += 1

        chunks.append(text[start:cut_point].strip())
        start = max(start + 1, cut_point - overlap)

    return [c for c in chunks if c.strip()]

def derive_topic_tags(heading: str, text: str, default_tags: str) -> str:
    """
    Maps topic keywords from heading and text content to build relevant topic tags.
    """
    combined = f"{heading} {text}".lower()
    tag_rules = [
        ("home-business", ["home-based", "home occupation", "residential zone"]),
        ("landlord", ["landlord", "dwelling units", "residential units", "commercial property"]),
        ("contractor", ["contractor", "cslb", "construction", "plumbing", "electrical"]),
        ("police-permit", ["police permit", "massage", "firearms", "pawnshop", "secondhand"]),
        ("CUP", ["conditional use permit", "cup", "planning division", "zoning clearance"]),
        ("fees", ["fee", "gross receipts", "sb 1186", "cost", "payment"]),
        ("renewal", ["renew", "renewal", "december 31", "delinquent", "penalty"]),
        ("code-enforcement", ["violation", "misdemeanor", "fine", "unlicensed", "stop-work"]),
        ("state-permits", ["calgold", "seller's permit", "oc health", "scaqmd", "cdtfa", "permit"])
    ]

    tags = set([t.strip() for t in default_tags.split(",") if t.strip()])
    for tag, keywords in tag_rules:
        if any(kw in combined for kw in keywords):
            tags.add(tag)

    return ",".join(sorted(list(tags)))

def chunk_scraped_page(page_data: dict) -> list:
    """
    Parses HTML content from a scraped page and generates structured chunks.
    Splits by headings/sections, falling back to block splitting.
    """
    raw_html = page_data["raw_html"]
    soup = BeautifulSoup(raw_html, "html.parser")

    # Clean non-content elements
    for element in soup(["script", "style", "nav", "footer", "header", "noscript", "svg"]):
        element.decompose()

    main_content = soup.find("main") or soup.find("article") or soup.find("body") or soup

    sections = []
    
    # Check for explicitly structured <section> blocks
    section_tags = main_content.find_all("section")
    if section_tags:
        for sec in section_tags:
            h_tag = sec.find(["h1", "h2", "h3", "h4", "dt"])
            heading = h_tag.get_text(strip=True) if h_tag else page_data["title"]
            text = sec.get_text(separator="\n", strip=True)
            if heading and text.startswith(heading):
                text = text[len(heading):].strip()
            if text:
                sections.append({"heading": heading, "text": text})
    else:
        # Heading-based splitting for pages without <section> tags
        headings = main_content.find_all(["h1", "h2", "h3", "h4", "dt"])
        if headings:
            for i, h in enumerate(headings):
                heading_text = h.get_text(strip=True)
                content_elements = []
                sibling = h.next_sibling
                while sibling and sibling not in headings:
                    if hasattr(sibling, "get_text"):
                        content_elements.append(sibling.get_text(separator="\n", strip=True))
                    sibling = sibling.next_sibling

                sec_text = "\n".join([c for c in content_elements if c.strip()])
                if not sec_text:
                    sec_text = heading_text
                sections.append({"heading": heading_text, "text": sec_text})

    # If still no sections extracted, split whole body text
    if not sections:
        full_text = main_content.get_text(separator="\n", strip=True)
        if full_text:
            sections.append({"heading": page_data["title"], "text": full_text})

    final_chunks = []
    chunk_index = 1
    slug = page_data["slug"]
    source_url = page_data["url"]
    scrape_date = page_data["scrape_date"]
    default_tags = page_data["default_tags"]

    for sec in sections:
        sec_heading = sec["heading"]
        sec_text = sec["text"]

        if len(sec_text) > MAX_CHUNK_CHARS:
            sub_texts = recursive_character_split(sec_text)
        else:
            sub_texts = [sec_text]

        for sub_t in sub_texts:
            if not sub_t.strip():
                continue
            chunk_id = f"chk_{slug}_{chunk_index:03d}"
            tags = derive_topic_tags(sec_heading, sub_t, default_tags)
            
            chunk_record = {
                "id": chunk_id,
                "source_url": source_url,
                "section_heading": sec_heading,
                "chunk_text": sub_t,
                "topic_tags": tags,
                "scrape_date": scrape_date
            }
            final_chunks.append(chunk_record)
            chunk_index += 1

    return final_chunks
