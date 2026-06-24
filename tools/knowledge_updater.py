
# -*- coding: utf-8 -*-
"""knowledge_updater.py - self-improving knowledge pipeline for the eia-report-automation skill.

This tool fetches recent academic and domain-authoritative content, scores it by
recency, relevance, and source tier, deduplicates by URL/DOI hash, and appends
date-stamped entries to SECOND-KNOWLEDGE-BRAIN.md.

Design principles:
  - Pluggable fetchers (ArXiv, domain crawl, WebSearch).
  - Graceful degradation when offline or dependencies are missing.
  - Deterministic, reproducible dry-run mode.
  - Production-grade logging and structured run records.

Usage:
  python tools/knowledge_updater.py [--dry-run] [--since YYYY-MM-DD] [--max-results N]
"""

import argparse
import dataclasses
import datetime
import hashlib
import json
import logging
import os
import re
import sys
import urllib.parse
import urllib.request
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional, Sequence, Set

logger = logging.getLogger("knowledge_updater")

DEFAULT_CONFIG = {
    "brain_path": "../SECOND-KNOWLEDGE-BRAIN.md",
    "arxiv_categories": ["physics.geo-ph", "q-bio.PE"],
    "search_queries": [
        "environmental impact assessment methodology RIAM",
        "cumulative impact assessment",
        "mitigation hierarchy biodiversity offset",
        "EIA regulatory standards update",
    ],
    "domains": ["iaia.org", "ifc.org", "iucnredlist.org", "protectedplanet.net"],
    "source_tiers": {
        "arxiv": 1.0,
        "scholar": 0.9,
        "domain": 0.85,
        "web": 0.7,
    },
    "max_results": 15,
    "score_weights": {"recency": 2.0, "relevance": 1.0, "tier": 1.0},
}


@dataclasses.dataclass(frozen=True)
class KnowledgeEntry:
    title: str
    authors: str
    date: str
    url: str
    abstract: str
    source_tier: float
    source_label: str
    doi: str = ""

    def dedup_key(self) -> str:
        key = (self.doi or self.url or self.title).strip().lower()
        return hashlib.sha1(key.encode("utf-8", "ignore")).hexdigest()[:12]

    def as_markdown_row(self, score: float) -> str:
        return (
            f"| {self.title[:90].replace(chr(124), chr(47))} | "
            f"{(self.authors[:40] or '-')} | "
            f"{(self.date[:4] if self.date else '-')} | "
            f"{self.source_label} | "
            f"{(self.url or '-')} | "
            f"score={score:.2f} <!--h:{self.dedup_key()}--> |"
        )


class Fetcher(ABC):
    @abstractmethod
    def fetch(self, config: dict) -> List[KnowledgeEntry]:
        ...


class ArxivFetcher(Fetcher):
    """Fetch recent papers from the ArXiv Atom API."""

    API = "http://export.arxiv.org/api/query"

    def fetch(self, config: dict) -> List[KnowledgeEntry]:
        entries: List[KnowledgeEntry] = []
        max_results = config.get("max_results", DEFAULT_CONFIG["max_results"])
        tier = config.get("source_tiers", DEFAULT_CONFIG["source_tiers"]).get("arxiv", 1.0)
        for category in config.get("arxiv_categories", DEFAULT_CONFIG["arxiv_categories"]):
            url = (
                f"{self.API}?" + urllib.parse.urlencode(
                    {
                        "search_query": f"cat:{category}",
                        "sortBy": "submittedDate",
                        "sortOrder": "descending",
                        "max_results": max_results,
                    }
                )
            )
            try:
                with urllib.request.urlopen(url, timeout=30) as resp:
                    data = resp.read().decode("utf-8", "ignore")
            except Exception as exc:
                logger.warning("ArXiv fetch failed for %s: %s", category, exc)
                continue
            entries.extend(self._parse(data, tier))
        return entries

    @staticmethod
    def _parse(xml: str, tier: float) -> List[KnowledgeEntry]:
        entries = []
        for block in re.findall(r"<entry>(.*?)</entry>", xml, re.S):
            def get(tag: str) -> str:
                m = re.search(rf"<{tag}>(.*?)</{tag}>", block, re.S)
                if not m:
                    return ""
                return re.sub(r"\s+", " ", m.group(1)).strip()

            title = get("title")
            if not title:
                continue
            summary = get("summary")
            published = get("published")[:10]
            link = ""
            m = re.search(r"<id>(.*?)</id>", block, re.S)
            if m:
                link = m.group(1).strip()
            authors = ", ".join(re.findall(r"<name>(.*?)</name>", block))
            entries.append(
                KnowledgeEntry(
                    title=title,
                    authors=authors,
                    date=published,
                    url=link,
                    abstract=summary,
                    source_tier=tier,
                    source_label="ArXiv",
                )
            )
        return entries


class DomainCrawler(Fetcher):
    """Optional crawl4ai-based fetcher for authoritative domains."""

    def fetch(self, config: dict) -> List[KnowledgeEntry]:
        entries: List[KnowledgeEntry] = []
        tier = config.get("source_tiers", DEFAULT_CONFIG["source_tiers"]).get("domain", 0.85)
        try:
            from crawl4ai import WebCrawler  # type: ignore
        except Exception as exc:
            logger.info("crawl4ai not installed; skipping domain crawl: %s", exc)
            return entries

        crawler = WebCrawler()
        crawler.warmup()
        for domain in config.get("domains", DEFAULT_CONFIG["domains"]):
            url = f"https://{domain}"
            try:
                result = crawler.run(url=url)
                text = (result.markdown or "")[:600]
                entries.append(
                    KnowledgeEntry(
                        title=f"Domain scan: {domain}",
                        authors="",
                        date=str(datetime.date.today()),
                        url=url,
                        abstract=text,
                        source_tier=tier,
                        source_label="Domain",
                    )
                )
            except Exception as exc:
                logger.warning("crawl4ai failed for %s: %s", domain, exc)
        return entries



class WebSearchFetcher(Fetcher):
    """Pluggable WebSearch fetcher.

    Expects an environment variable WEB_SEARCH_ENDPOINT to be set to a JSON API
    that accepts a POST body {"queries": [...], "max_results": N} and returns
    a list of objects with title, authors, date, url, abstract, doi, source.
    If the endpoint is unavailable the fetcher degrades to a no-op.
    """

    def fetch(self, config: dict) -> List[KnowledgeEntry]:
        endpoint = os.environ.get("WEB_SEARCH_ENDPOINT")
        if not endpoint:
            logger.info("WEB_SEARCH_ENDPOINT not set; skipping web search fetch.")
            return []
        queries = config.get("search_queries", DEFAULT_CONFIG["search_queries"])
        max_results = config.get("max_results", DEFAULT_CONFIG["max_results"])
        tier = config.get("source_tiers", DEFAULT_CONFIG["source_tiers"]).get("web", 0.7)
        payload = json.dumps({"queries": queries, "max_results": max_results}).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        try:
            req = urllib.request.Request(endpoint, data=payload, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=45) as resp:
                data = json.loads(resp.read().decode("utf-8", "ignore"))
        except Exception as exc:
            logger.warning("WebSearch fetch failed: %s", exc)
            return []

        entries = []
        for item in data if isinstance(data, list) else data.get("results", []):
            entries.append(
                KnowledgeEntry(
                    title=str(item.get("title", "")),
                    authors=str(item.get("authors", "")),
                    date=str(item.get("date", "")),
                    url=str(item.get("url", "")),
                    abstract=str(item.get("abstract", "")),
                    doi=str(item.get("doi", "")),
                    source_tier=tier,
                    source_label=str(item.get("source", "Web")),
                )
            )
        return entries



class Scorer:
    """Score entries by recency, keyword relevance, and source tier."""

    def __init__(self, config: dict):
        self.weights = config.get("score_weights", DEFAULT_CONFIG["score_weights"])
        queries = config.get("search_queries", DEFAULT_CONFIG["search_queries"])
        self.keywords = set()
        for q in queries:
            self.keywords.update(w.lower() for w in q.split() if len(w) > 2)

    def score(self, entry: KnowledgeEntry) -> float:
        text = (entry.title + " " + entry.abstract).lower()
        relevance = sum(1 for k in self.keywords if k in text)
        try:
            d = datetime.date.fromisoformat(entry.date)
            age_days = (datetime.date.today() - d).days
            recency = max(0.0, 1.0 - age_days / 730.0)
        except Exception:
            recency = 0.0
        tier = float(entry.source_tier)
        return (
            self.weights["relevance"] * relevance
            + self.weights["recency"] * recency
            + self.weights["tier"] * tier
        )


class KnowledgeBrain:
    def __init__(self, path: Path):
        self.path = path

    def existing_hashes(self) -> Set[str]:
        if not self.path.exists():
            return set()
        text = self.path.read_text(encoding="utf-8")
        return set(re.findall(r"<!--h:([0-9a-f]{12})-->", text))


    def append(self, entries: Sequence[KnowledgeEntry], scorer: Scorer, dry_run: bool = False) -> int:
        existing = self.existing_hashes()
        scored = [(entry, scorer.score(entry)) for entry in entries]
        scored.sort(key=lambda x: x[1], reverse=True)

        new_rows, log_lines = [], []
        for entry, score in scored:
            key = entry.dedup_key()
            if key in existing:
                continue
            existing.add(key)
            new_rows.append(entry.as_markdown_row(score))
            log_lines.append(
                f"- {datetime.date.today().isoformat()} - added: {entry.title[:90]}".replace(chr(124), chr(47))
            )

        if not new_rows:
            logger.info("No new entries to append.")
            return 0

        if dry_run:
            logger.info("Dry-run: would append %d entries.", len(new_rows))
            for row in new_rows:
                logger.info(row)
            return len(new_rows)

        with self.path.open("a", encoding="utf-8") as f:
            f.write(f"\n<!-- auto-appended {datetime.date.today().isoformat()} -->\n")
            f.write("\n".join(new_rows) + "\n")
            f.write("\n".join(log_lines) + "\n")
        logger.info("Appended %d new entries.", len(new_rows))
        return len(new_rows)


class RunLogger:
    """Append structured run records to a JSONL log file."""

    def __init__(self, path: Path):
        self.path = path

    def record(self, fetched: int, appended: int, dry_run: bool, since: Optional[str]) -> None:
        record = {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "fetched": fetched,
            "appended": appended,
            "dry_run": dry_run,
            "since": since,
        }
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")



def load_config(path: Optional[Path] = None) -> dict:
    config = DEFAULT_CONFIG.copy()
    if path and path.exists():
        with path.open(encoding="utf-8") as f:
            config.update(json.load(f))
    return config


def filter_since(entries: List[KnowledgeEntry], since: Optional[str]) -> List[KnowledgeEntry]:
    if not since:
        return entries
    try:
        cutoff = datetime.date.fromisoformat(since)
    except Exception:
        logger.warning("Invalid --since date: %s", since)
        return entries
    filtered = []
    for entry in entries:
        try:
            d = datetime.date.fromisoformat(entry.date)
        except Exception:
            continue
        if d >= cutoff:
            filtered.append(entry)
    return filtered


def main() -> int:
    parser = argparse.ArgumentParser(description="Update SECOND-KNOWLEDGE-BRAIN.md")
    parser.add_argument("--config", type=Path, help="Path to JSON config file")
    parser.add_argument("--dry-run", action="store_true", help="Do not write the brain file")
    parser.add_argument("--since", help="Only consider entries on or after YYYY-MM-DD")
    parser.add_argument("--max-results", type=int, help="Override max results per source")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    config = load_config(args.config)
    if args.max_results:
        config["max_results"] = args.max_results

    script_dir = Path(__file__).resolve().parent
    brain_path = script_dir / config.get("brain_path", DEFAULT_CONFIG["brain_path"])
    log_path = brain_path.with_suffix(".log.jsonl")

    fetchers: List[Fetcher] = [ArxivFetcher(), WebSearchFetcher(), DomainCrawler()]
    entries: List[KnowledgeEntry] = []
    for fetcher in fetchers:
        try:
            entries.extend(fetcher.fetch(config))
        except Exception as exc:
            logger.exception("Fetcher %s failed: %s", fetcher.__class__.__name__, exc)

    entries = filter_since(entries, args.since)
    scorer = Scorer(config)
    brain = KnowledgeBrain(brain_path)
    appended = brain.append(entries, scorer, dry_run=args.dry_run)

    RunLogger(log_path).record(fetched=len(entries), appended=appended, dry_run=args.dry_run, since=args.since)
    logger.info("Run complete: fetched=%d appended=%d", len(entries), appended)
    return 0


if __name__ == "__main__":
    sys.exit(main())
