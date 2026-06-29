"""
API-key store for the gateway.

Keys are opaque strings you hand to users (format: ``tsg_<random>``). Only a
salted SHA-256 hash of each key is stored on disk — the plaintext is shown once
at creation and never persisted. Keys can be revoked individually; revocation
takes effect without restarting the server (the store reloads when the file's
mtime changes).

This is a single-file JSON store, fine for a pilot / modest user count. For
larger deployments back it with a database.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
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
    key_id: str            # public id (safe to log), e.g. "k_ab12cd34"
    label: str             # who/what this key is for
    salt: str
    hash: str
    active: bool = True
    rpm: int = 20          # per-key requests-per-minute limit
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

    # ---- persistence -----------------------------------------------------
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
        payload = {"keys": [asdict(r) for r in self._records]}
        self.path.write_text(json.dumps(payload, indent=2), "utf-8")
        self._mtime = self.path.stat().st_mtime

    # ---- management ------------------------------------------------------
    def create(self, label: str, rpm: int = 20) -> tuple[str, KeyRecord]:
        """Create a key. Returns (plaintext_key, record). Plaintext is only
        available here — store it somewhere safe to give to the user."""
        self.reload()
        key = generate_key()
        salt = secrets.token_hex(8)
        rec = KeyRecord(
            key_id="k_" + secrets.token_hex(4),
            label=label,
            salt=salt,
            hash=_hash(salt, key),
            rpm=rpm,
            created=time.time(),
        )
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

    # ---- verification ----------------------------------------------------
    def verify(self, presented: str) -> KeyRecord | None:
        """Return the active record matching the presented key, else None.
        Constant-time hash comparison; does not reveal which key matched."""
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
        # best-effort persistence of usage counters
        try:
            self._save()
        except OSError:
            pass
