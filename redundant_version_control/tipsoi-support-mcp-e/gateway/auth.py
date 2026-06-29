"""
API-key store for the gateway. Salted SHA-256 hashes on disk; plaintext shown
once at creation. Individually revocable; reloads when the file's mtime changes.
Single-file JSON store — fine for a pilot; back with a DB for scale.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import secrets
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

KEY_PREFIX = "tsg_"


def generate_key() -> str:
    return KEY_PREFIX + secrets.token_urlsafe(32)


def _hash(salt: str, key: str) -> str:
    return hashlib.sha256((salt + key).encode("utf-8")).hexdigest()


@dataclass
class KeyRecord:
    key_id: str
    label: str
    salt: str
    hash: str
    active: bool = True
    rpm: int = 20
    created: float = 0.0
    last_used: float = 0.0
    use_count: int = 0

    def public(self) -> dict[str, Any]:
        d = asdict(self)
        d.pop("salt"); d.pop("hash")
        return d


class KeyStore:
    def __init__(self, path: str):
        self.path = Path(path)
        self._records: list[KeyRecord] = []
        self._mtime: float = -1.0
        self.reload(force=True)

    def reload(self, force: bool = False) -> None:
        if not self.path.exists():
            self._records = []
            return
        mtime = self.path.stat().st_mtime
        if not force and mtime == self._mtime:
            return
        data = json.loads(self.path.read_text("utf-8") or '{"keys": []}')
        self._records = [KeyRecord(**k) for k in data.get("keys", [])]
        self._mtime = mtime

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps({"keys": [asdict(r) for r in self._records]}, indent=2), "utf-8")
        self._mtime = self.path.stat().st_mtime

    def create(self, label: str, rpm: int = 20) -> tuple[str, KeyRecord]:
        self.reload()
        key = generate_key()
        salt = secrets.token_hex(8)
        rec = KeyRecord(key_id="k_" + secrets.token_hex(4), label=label, salt=salt,
                        hash=_hash(salt, key), rpm=rpm, created=time.time())
        self._records.append(rec)
        self._save()
        return key, rec

    def revoke(self, key_id: str) -> bool:
        self.reload()
        for r in self._records:
            if r.key_id == key_id:
                r.active = False
                self._save()
                return True
        return False

    def list(self) -> list[KeyRecord]:
        self.reload()
        return list(self._records)

    def verify(self, presented: str) -> KeyRecord | None:
        if not presented or not presented.startswith(KEY_PREFIX):
            return None
        self.reload()
        for r in self._records:
            if not r.active:
                continue
            if hmac.compare_digest(r.hash, _hash(r.salt, presented)):
                return r
        return None

    def mark_used(self, key_id: str) -> None:
        for r in self._records:
            if r.key_id == key_id:
                r.last_used = time.time()
                r.use_count += 1
                break
        try:
            self._save()
        except OSError:
            pass
