"""
CLI to issue, list, and revoke gateway API keys.

    python -m gateway.manage_keys create --label "Pilot HR" --rpm 20
    python -m gateway.manage_keys list
    python -m gateway.manage_keys revoke k_ab12cd34

The keys file path comes from GATEWAY_KEYS_FILE (default ./keys.json).
The plaintext key is printed ONCE on creation — copy it then; it isn't stored.
"""

from __future__ import annotations

import argparse
import os
from datetime import datetime, timezone

from .auth import KeyStore


def _fmt_ts(ts: float) -> str:
    if not ts:
        return "—"
    return datetime.fromtimestamp(ts, timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def main() -> None:
    parser = argparse.ArgumentParser(description="Manage Tipsoi Support gateway keys")
    parser.add_argument(
        "--keys-file",
        default=os.environ.get("GATEWAY_KEYS_FILE", "./keys.json"),
        help="Path to keys JSON store (default: ./keys.json or $GATEWAY_KEYS_FILE)",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("create", help="Issue a new key")
    c.add_argument("--label", required=True, help="Who/what this key is for")
    c.add_argument("--rpm", type=int, default=20, help="Requests per minute (default 20)")

    sub.add_parser("list", help="List all keys (no secrets)")

    r = sub.add_parser("revoke", help="Revoke a key by key_id")
    r.add_argument("key_id", help="The key_id (e.g. k_ab12cd34)")

    args = parser.parse_args()
    store = KeyStore(args.keys_file)

    if args.cmd == "create":
        key, rec = store.create(label=args.label, rpm=args.rpm)
        print("Key created. Copy the secret now — it will NOT be shown again:\n")
        print(f"  key_id : {rec.key_id}")
        print(f"  label  : {rec.label}")
        print(f"  rpm    : {rec.rpm}")
        print(f"  SECRET : {key}\n")
        print("Give SECRET to the user. Revoke anytime with:")
        print(f"  python -m gateway.manage_keys revoke {rec.key_id}")

    elif args.cmd == "list":
        records = store.list()
        if not records:
            print("No keys yet. Create one with: manage_keys create --label ...")
            return
        print(f"{'key_id':<12} {'active':<7} {'rpm':<5} {'uses':<6} {'last used':<20} label")
        print("-" * 80)
        for r in records:
            print(f"{r.key_id:<12} {str(r.active):<7} {r.rpm:<5} {r.use_count:<6} "
                  f"{_fmt_ts(r.last_used):<20} {r.label}")

    elif args.cmd == "revoke":
        ok = store.revoke(args.key_id)
        print(f"Revoked {args.key_id}." if ok else f"No key with id {args.key_id}.")


if __name__ == "__main__":
    main()
