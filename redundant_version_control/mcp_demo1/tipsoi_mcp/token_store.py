"""
In-memory token store for the Tipsoi OAuth 2.1 proxy.

Stores:
  - Authorization codes (short-lived, single-use)
  - Access tokens (longer-lived, maps to a Tipsoi user session)

This is intentionally simple: an in-memory dict is fine for Phase 2.
Phase 3+ can swap this for Redis or a DB without touching the OAuth routes.
"""

from __future__ import annotations

import hashlib
import secrets
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class UserSession:
    """Everything we know about a Tipsoi-authenticated user."""
    email: str
    access_token: str
    refresh_token: Optional[str]
    user_id: Optional[str]
    office_id: Optional[str]
    company_id: Optional[str]
    expires_at: float = field(default_factory=lambda: time.time() + 86400 * 7)

    def is_valid(self) -> bool:
        return time.time() < self.expires_at


@dataclass
class AuthCode:
    session: UserSession
    code_challenge: Optional[str]      # PKCE S256
    code_challenge_method: Optional[str]
    redirect_uri: str
    client_id: str
    expires_at: float = field(default_factory=lambda: time.time() + 300)

    def is_valid(self) -> bool:
        return time.time() < self.expires_at


class TokenStore:
    def __init__(self) -> None:
        self._codes: dict[str, AuthCode] = {}
        self._tokens: dict[str, UserSession] = {}
        # Dynamic client registrations
        self._clients: dict[str, dict] = {}

    # ---- client registration ------------------------------------------------

    def register_client(self, client_id: str, metadata: dict) -> None:
        self._clients[client_id] = metadata

    def client_exists(self, client_id: str) -> bool:
        return client_id in self._clients

    def get_client(self, client_id: str) -> Optional[dict]:
        return self._clients.get(client_id)

    def client_allows_redirect(self, client_id: str, redirect_uri: str) -> bool:
        """True if the redirect_uri is registered for this client.

        Unknown clients (no registration on record) are allowed through to
        preserve compatibility with clients that skip dynamic registration;
        registered clients are held to their declared redirect_uris to prevent
        open-redirect / authorization-code phishing.
        """
        meta = self._clients.get(client_id)
        if not meta:
            return True
        registered = meta.get("redirect_uris")
        if not registered:
            return True
        return redirect_uri in registered

    # ---- auth codes ---------------------------------------------------------

    def create_code(
        self,
        session: UserSession,
        redirect_uri: str,
        client_id: str,
        code_challenge: Optional[str] = None,
        code_challenge_method: Optional[str] = None,
    ) -> str:
        code = secrets.token_urlsafe(40)
        self._codes[code] = AuthCode(
            session=session,
            code_challenge=code_challenge,
            code_challenge_method=code_challenge_method,
            redirect_uri=redirect_uri,
            client_id=client_id,
        )
        return code

    def exchange_code(
        self,
        code: str,
        redirect_uri: str,
        code_verifier: Optional[str] = None,
    ) -> Optional[UserSession]:
        entry = self._codes.pop(code, None)
        if entry is None or not entry.is_valid():
            return None
        if entry.redirect_uri != redirect_uri:
            return None
        # PKCE validation
        if entry.code_challenge:
            if not code_verifier:
                return None
            expected = _s256(code_verifier)
            if expected != entry.code_challenge:
                return None
        return entry.session

    # ---- access tokens ------------------------------------------------------

    def create_token(self, session: UserSession) -> str:
        token = secrets.token_urlsafe(48)
        self._tokens[token] = session
        return token

    def get_session(self, token: str) -> Optional[UserSession]:
        session = self._tokens.get(token)
        if session and session.is_valid():
            return session
        if session:
            del self._tokens[token]
        return None

    def revoke_token(self, token: str) -> None:
        self._tokens.pop(token, None)


# Singleton
token_store = TokenStore()


def _s256(verifier: str) -> str:
    """base64url(sha256(verifier)) — PKCE S256 method."""
    import base64
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
