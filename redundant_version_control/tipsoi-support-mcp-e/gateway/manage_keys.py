"""
CLI to issue / list / revoke gateway API keys.

    python -m gateway.manage_keys create --label "Pilot HR" --rpm 20
    python -m gateway.manage_keys list
    python -m gateway.manage_keys revoke k_ab12cd34

Keys file path from GATEWAY_KEYS_FILE (default ./keys.json). The plaintext key
is printed ONCE on creation.
"""

from __future__ import annotations

import argparse
import os
from datetime import datetime, timezone

from .auth import KeyStore


def _fmt_ts(ts: float) -> str:
    return datetime.fromtimestamp(ts, timezone.utc).strftime("%Y-%m-%d %H:%M UTC") if ts else "—"


def main() -> None:
    p = argparse.ArgumentParser(description="Manage Tipsoi Support gateway keys")
    p.add_argument("--keys-file", default=os.environ.get("GATEWAY_KEYS_FILE", "./keys.json"))
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("create"); c.add_argument("--label", required=True); c.add_argument("--rpm", type=int, default=20)
    sub.add_parser("list")
    r = sub.add_parser("revoke"); r.add_argument("key_id")
    args = p.parse_args()
    store = KeyStore(args.keys_file)

    if args.cmd == "create":
        key, rec = store.create(label=args.label, rpm=args.rpm)
        print("Key created. Copy the secret now — it will NOT be shown again:\n")
        print(f"  key_id : {rec.key_id}\n  label  : {rec.label}\n  rpm    : {rec.rpm}\n  SECRET : {key}\n")
        print(f"Revoke with: python -m gateway.manage_keys revoke {rec.key_id}")
    elif args.cmd == "list":
        records = store.list()
        if not records:
            print("No keys yet."); return
        print(f"{'key_id':<12} {'active':<7} {'rpm':<5} {'uses':<6} {'last used':<20} label")
        print("-" * 80)
        for r in records:
            print(f"{r.key_id:<12} {str(r.active):<7} {r.rpm:<5} {r.use_count:<6} {_fmt_ts(r.last_used):<20} {r.label}")
    elif args.cmd == "revoke":
        print(f"Revoked {args.key_id}." if store.revoke(args.key_id) else f"No key with id {args.key_id}.")


if __name__ == "__main__":
    main()
