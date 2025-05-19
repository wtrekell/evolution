#!/usr/bin/env python3
import os
import re
import yaml
from pathlib import Path
import markdown
from bs4 import BeautifulSoup

base_dir = Path("articles")
index_path = base_dir / "README.md"
timeline_path = Path("timeline.md")

def extract_title_and_summary(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        html = markdown.markdown(f.read())
    soup = BeautifulSoup(html, "html.parser")

    title = "-"
    summary = "-"
    in_tldr = False

    for tag in soup.find_all(["h1", "h2", "p"]):
        if tag.name == "h1" and title == "-":
            title = tag.text.strip()
        elif tag.name == "h2" and tag.text.strip().lower() == "tl;dr":
            in_tldr = True
        elif in_tldr and tag.name == "p":
            summary = tag.text.strip()
            break

    return title, summary

def get_existing_folders(index_file):
    if not index_file.exists():
        return set()
    with open(index_file, "r") as f:
        return {line.split("|")[2].split("]")[0].strip() for line in f if line.startswith("|")}

def load_metadata(yml_path):
    if not yml_path.exists():
        return {}
    with open(yml_path, "r") as f:
        return yaml.safe_load(f)

def append_index_row(f, title, folder_name, summary):
    f.write(f"| {title} | [{folder_name}](./{folder_name}/) | {summary} | - |\n")


def append_timeline_entry(f, year, month, date, title, folder_name, summary):
    f.write(f"\n## {year}\n\n### {month}\n")
    f.write(f"- **{date}** – [{title}](./articles/{folder_name}/)  \n  {summary}\n")

def generate_article_readme(folder_path, title, summary, meta, article_file):
    tags = ", ".join(meta.get("tags", ["-"]))
    related = meta.get("related", ["-"])
    related_links = "\n".join([f"- [{rel}](../{rel}/)" for rel in related]) if related != ["-"] else "-"

    content = f"""# {title}

## Summary
{summary}

## SEO Title
{meta.get('seo_title', '-')}

## SEO Description
{meta.get('seo_description', '-')}

## Tags
{tags}

## Related Articles
{related_links}

## Folder Contents
- `{article_file.name}`
- `prompts/`
- `images/`
- `data/`
- `notes.md`

## Navigation
- [Back to Repo Root](../../)
- [Article Index](../README.md)
- [Timeline](../../timeline.md)
"""
    (folder_path / "README.md").write_text(content)

existing_folders = get_existing_folders(index_path)

new_entries = []
timeline_updates = {}
for folder in base_dir.iterdir():
    if not folder.is_dir() or folder.name in existing_folders:
        continue

    match = re.match(r"^(\d{4})(\d{2})(\d{2})-(.+)", folder.name)
    if not match:
        continue

    year, month, day, slug = match.groups()
    date = f"{year}-{month}-{day}"
    folder_name = folder.name
    final_md = next(folder.glob("final-*.md"), None)
    if not final_md:
        continue

    title, summary = extract_title_and_summary(final_md)
    if title == "-":
        title = slug.replace("-", " ").title()

    meta = load_metadata(folder / "metadata.yml")
    generate_article_readme(folder, title, summary, meta, final_md)

    new_entries.append((title, folder_name, summary))
    timeline_updates.setdefault((year, month), []).append((date, title, folder_name, summary))

# Append new index entries
if new_entries:
    with open(index_path, "a", encoding="utf-8") as f:
        for title, folder_name, summary in new_entries:
            append_index_row(f, title, folder_name, summary)

# Append timeline entries
if timeline_updates:
    with open(timeline_path, "a", encoding="utf-8") as f:
        for (year, month), entries in timeline_updates.items():
            append_timeline_entry(f, year, month, *entries[0])
