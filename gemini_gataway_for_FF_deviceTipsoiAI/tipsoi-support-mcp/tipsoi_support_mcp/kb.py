"""
Knowledge-base loader + in-process BM25 search.

The bundled Tipsoi KB (markdown, bilingual EN/BN) lives in ``kb_docs/``.
At import time we load every ``*.md`` file, strip YAML front-matter into
structured metadata, and build a tiny BM25 index over title + tags + body.

Zero external dependencies — pure standard library. Fully offline.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any

KB_DIR = Path(__file__).parent / "kb_docs"

_TOKEN_RE = re.compile(r"[a-z0-9]+|[ঀ-৿]+")

_STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "to", "in", "is", "are", "for",
    "on", "how", "do", "i", "my", "with", "it", "this", "that", "be", "can",
    "what", "why", "when", "not", "no", "you", "your", "we", "from", "at",
}


def tokenize(text: str) -> list[str]:
    toks = _TOKEN_RE.findall(text.lower())
    return [t for t in toks if t not in _STOPWORDS and len(t) > 1]


_FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def _parse_front_matter(raw: str) -> tuple[dict[str, Any], str]:
    m = _FM_RE.match(raw)
    if not m:
        return {}, raw
    meta: dict[str, Any] = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip()
        if not key:
            continue
        if val.startswith("[") and val.endswith("]"):
            items = [v.strip().strip('"').strip("'") for v in val[1:-1].split(",")]
            meta[key] = [v for v in items if v]
        else:
            meta[key] = val.strip('"').strip("'")
    return meta, raw[m.end():]


@dataclass
class Article:
    doc_id: str
    title: str
    category: str
    description: str
    tags: list[str]
    body: str
    _tokens: list[str] = field(default_factory=list, repr=False)

    def summary(self, max_chars: int = 320) -> str:
        text = self.description.strip()
        if not text:
            for block in re.split(r"\n\s*\n", self.body):
                block = block.strip()
                if block and not block.startswith(("#", "---", "|", "```")):
                    text = block
                    break
        text = re.sub(r"\s+", " ", text)
        return text[:max_chars] + ("…" if len(text) > max_chars else "")


class _BM25:
    K1 = 1.5
    B = 0.75
    TITLE_BOOST = 3
    TAG_BOOST = 2

    def __init__(self, articles: list[Article]):
        self.articles = articles
        self.N = len(articles)
        self.doc_freq: dict[str, int] = {}
        self.doc_len: list[int] = []
        for art in articles:
            toks = (
                tokenize(art.title) * self.TITLE_BOOST
                + tokenize(" ".join(art.tags)) * self.TAG_BOOST
                + tokenize(art.category)
                + tokenize(art.body)
            )
            art._tokens = toks
            self.doc_len.append(len(toks))
            for term in set(toks):
                self.doc_freq[term] = self.doc_freq.get(term, 0) + 1
        self.avgdl = (sum(self.doc_len) / self.N) if self.N else 0.0
        self._tf: list[dict[str, int]] = []
        for art in articles:
            tf: dict[str, int] = {}
            for t in art._tokens:
                tf[t] = tf.get(t, 0) + 1
            self._tf.append(tf)

    def _idf(self, term: str) -> float:
        n = self.doc_freq.get(term, 0)
        if n == 0:
            return 0.0
        return math.log(1 + (self.N - n + 0.5) / (n + 0.5))

    def search(self, query: str, limit: int) -> list[tuple[Article, float]]:
        q_terms = tokenize(query)
        if not q_terms:
            return []
        scored: list[tuple[Article, float]] = []
        for i, art in enumerate(self.articles):
            tf = self._tf[i]
            dl = self.doc_len[i] or 1
            score = 0.0
            for term in q_terms:
                f = tf.get(term, 0)
                if not f:
                    continue
                idf = self._idf(term)
                denom = f + self.K1 * (1 - self.B + self.B * dl / (self.avgdl or 1))
                score += idf * (f * (self.K1 + 1)) / denom
            if score > 0:
                scored.append((art, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:limit]


@lru_cache(maxsize=1)
def _load() -> tuple[dict[str, Article], _BM25]:
    articles: dict[str, Article] = {}
    for path in sorted(KB_DIR.rglob("*.md")):
        raw = path.read_text(encoding="utf-8")
        meta, body = _parse_front_matter(raw)
        doc_id = path.relative_to(KB_DIR).with_suffix("").as_posix()
        title = str(meta.get("title") or _first_heading(body) or doc_id)
        tags = meta.get("tags") or []
        if isinstance(tags, str):
            tags = [tags]
        articles[doc_id] = Article(
            doc_id=doc_id,
            title=title,
            category=str(meta.get("category") or path.parent.name),
            description=str(meta.get("description") or ""),
            tags=list(tags),
            body=body.strip(),
        )
    index = _BM25(list(articles.values()))
    return articles, index


def _first_heading(body: str) -> str | None:
    for line in body.splitlines():
        line = line.strip()
        if line.startswith("#"):
            return line.lstrip("#").strip()
    return None


def doc_count() -> int:
    articles, _ = _load()
    return len(articles)


def search(query: str, limit: int = 5) -> list[dict[str, Any]]:
    _, index = _load()
    results = index.search(query, limit)
    out: list[dict[str, Any]] = []
    for art, score in results:
        out.append({
            "doc_id": art.doc_id,
            "title": art.title,
            "category": art.category,
            "tags": art.tags,
            "score": round(score, 3),
            "snippet": art.summary(),
        })
    return out


def get_article(doc_id: str) -> dict[str, Any] | None:
    articles, _ = _load()
    art = articles.get(doc_id)
    if not art:
        key = doc_id.strip("/").removesuffix(".md")
        art = articles.get(key)
    if not art:
        return None
    return {
        "doc_id": art.doc_id,
        "title": art.title,
        "category": art.category,
        "tags": art.tags,
        "description": art.description,
        "content": art.body,
    }


def list_doc_ids() -> list[str]:
    articles, _ = _load()
    return sorted(articles.keys())
