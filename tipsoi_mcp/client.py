"""
Thin async HTTP client for the Tipsoi HRM API.

Handles:
  - Sign-in (email/password -> access token + refresh token + userId)
  - Automatic token refresh on 401
  - Bearer-authenticated GET requests for read-only endpoints

This module is intentionally transport-agnostic: it knows nothing about MCP.
"""

from __future__ import annotations

import os
import json
import time
import asyncio
from dataclasses import dataclass, field
from typing import Any

import httpx

DEFAULT_BASE_URL = "https://hrm.tipsoi.pro/inovace-client/api/v1"


class TipsoiAuthError(RuntimeError):
    """Raised when authentication fails or no session is available."""


class TipsoiAPIError(RuntimeError):
    """Raised when the Tipsoi API returns a non-success response."""

    def __init__(self, status: int, url: str, detail: str):
        self.status = status
        self.url = url
        self.detail = detail
        super().__init__(f"Tipsoi API {status} on {url}: {detail}")


@dataclass
class Session:
    """Holds tokens for one authenticated Tipsoi user."""
    access_token: str
    refresh_token: str | None
    user_id: str | None
    # Best-effort expiry tracking; we still rely on 401 -> refresh as the source of truth.
    obtained_at: float = field(default_factory=time.time)


class TipsoiClient:
    """
    A single-session Tipsoi client.

    In Phase 1 (read-only) we run one client per server process, authenticated
    with one service/user account supplied via environment variables. The OAuth
    multi-user flow is a Phase 2+ concern and deliberately not implemented here.
    """

    @classmethod
    def with_session(
        cls,
        access_token: str,
        refresh_token: str | None = None,
        user_id: str | None = None,
        office_id: str | None = None,
        company_id: str | None = None,
    ) -> "TipsoiClient":
        """Create a client that starts with a pre-authenticated Tipsoi token."""
        client = cls(
            default_office_id=office_id or os.environ.get("TIPSOI_OFFICE_ID"),
            default_company_id=company_id or os.environ.get("TIPSOI_COMPANY_ID"),
        )
        client._session = Session(
            access_token=access_token,
            refresh_token=refresh_token,
            user_id=user_id,
        )
        return client

    def __init__(
        self,
        base_url: str | None = None,
        email: str | None = None,
        password: str | None = None,
        default_office_id: str | None = None,
        default_company_id: str | None = None,
        timeout: float = 30.0,
    ):
        self.base_url = (base_url or os.environ.get("TIPSOI_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
        self._email = email or os.environ.get("TIPSOI_EMAIL")
        self._password = password or os.environ.get("TIPSOI_PASSWORD")
        self.default_office_id = default_office_id or os.environ.get("TIPSOI_OFFICE_ID")
        self.default_company_id = default_company_id or os.environ.get("TIPSOI_COMPANY_ID")
        self._timeout = timeout
        self._session: Session | None = None
        self._lock = asyncio.Lock()

    # ---- auth -------------------------------------------------------------

    async def _sign_in(self, http: httpx.AsyncClient) -> Session:
        if not self._email or not self._password:
            raise TipsoiAuthError(
                "Missing credentials. Set TIPSOI_EMAIL and TIPSOI_PASSWORD."
            )
        url = f"{self.base_url}/auth/external-sync/sign-in"
        resp = await http.post(url, json={"email": self._email, "password": self._password})
        if resp.status_code >= 400:
            raise TipsoiAuthError(f"Sign-in failed ({resp.status_code}): {resp.text[:300]}")
        data = resp.json()
        token, refresh, user_id = _extract_tokens(data)
        if not token:
            raise TipsoiAuthError(f"Sign-in succeeded but no token found in response: {list(_flatten_keys(data))}")
        return Session(access_token=token, refresh_token=refresh, user_id=user_id)

    async def _refresh(self, http: httpx.AsyncClient) -> Session | None:
        sess = self._session
        if not sess or not sess.refresh_token:
            return None
        url = f"{self.base_url}/auth/refresh"
        payload: dict[str, Any] = {"refreshToken": sess.refresh_token}
        if sess.user_id:
            payload["userId"] = sess.user_id
        resp = await http.post(url, json=payload)
        if resp.status_code >= 400:
            return None
        data = resp.json()
        token, refresh, user_id = _extract_tokens(data)
        if not token:
            return None
        return Session(
            access_token=token,
            refresh_token=refresh or sess.refresh_token,
            user_id=user_id or sess.user_id,
        )

    async def _ensure_session(self, http: httpx.AsyncClient) -> Session:
        async with self._lock:
            if self._session is None:
                self._session = await self._sign_in(http)
            return self._session

    # ---- core request -----------------------------------------------------

    async def get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        """
        Authenticated GET. Transparently refreshes / re-signs on 401 once.
        `path` may start with '/' and is appended to base_url.
        """
        clean_params = {k: v for k, v in (params or {}).items() if v is not None}
        url = f"{self.base_url}/{path.lstrip('/')}"

        async with httpx.AsyncClient(timeout=self._timeout) as http:
            sess = await self._ensure_session(http)
            resp = await self._do_get(http, url, clean_params, sess.access_token)

            if resp.status_code == 401:
                # Try refresh, then full re-sign.
                async with self._lock:
                    new_sess = await self._refresh(http)
                    if new_sess is None:
                        new_sess = await self._sign_in(http)
                    self._session = new_sess
                resp = await self._do_get(http, url, clean_params, self._session.access_token)

            if resp.status_code >= 400:
                raise TipsoiAPIError(resp.status_code, url, resp.text[:500])

            if not resp.content:
                return None
            ctype = resp.headers.get("content-type", "")
            if "application/json" in ctype:
                return resp.json()
            return resp.text

    async def post(self, path: str, body: dict[str, Any] | None = None) -> Any:
        """
        Authenticated POST. Transparently refreshes / re-signs on 401 once.
        """
        url = f"{self.base_url}/{path.lstrip('/')}"
        async with httpx.AsyncClient(timeout=self._timeout) as http:
            sess = await self._ensure_session(http)
            resp = await self._do_post(http, url, body or {}, sess.access_token)

            if resp.status_code == 401:
                async with self._lock:
                    new_sess = await self._refresh(http)
                    if new_sess is None:
                        new_sess = await self._sign_in(http)
                    self._session = new_sess
                resp = await self._do_post(http, url, body or {}, self._session.access_token)

            if resp.status_code >= 400:
                raise TipsoiAPIError(resp.status_code, url, resp.text[:500])

            if not resp.content:
                return {"success": True}
            ctype = resp.headers.get("content-type", "")
            if "application/json" in ctype:
                return resp.json()
            return resp.text

    async def post_form(self, path: str, post_body: dict[str, Any]) -> Any:
        """
        Authenticated multipart/form-data POST.

        Several Tipsoi leave endpoints (apply / adjust) expect a `multipart/form-data`
        body with a JSON string in a `postBody` field and an optional `file` part —
        NOT an application/json body. This sends exactly that shape.
        Transparently refreshes / re-signs on 401 once.
        """
        url = f"{self.base_url}/{path.lstrip('/')}"
        async with httpx.AsyncClient(timeout=self._timeout) as http:
            sess = await self._ensure_session(http)
            resp = await self._do_post_form(http, url, post_body, sess.access_token)

            if resp.status_code == 401:
                async with self._lock:
                    new_sess = await self._refresh(http)
                    if new_sess is None:
                        new_sess = await self._sign_in(http)
                    self._session = new_sess
                resp = await self._do_post_form(http, url, post_body, self._session.access_token)

            if resp.status_code >= 400:
                raise TipsoiAPIError(resp.status_code, url, resp.text[:500])

            if not resp.content:
                return {"success": True}
            ctype = resp.headers.get("content-type", "")
            if "application/json" in ctype:
                return resp.json()
            return resp.text

    @staticmethod
    async def _do_post_form(http, url, post_body, token):
        # `data` carries the JSON string in a `postBody` form field; an empty
        # `file` part forces httpx to encode as multipart/form-data, matching
        # the API's expected request shape.
        return await http.post(
            url,
            data={"postBody": json.dumps(post_body)},
            files={"file": ("", b"", "application/octet-stream")},
            headers={"Authorization": f"Bearer {token}"},
        )

    @staticmethod
    async def _do_get(http, url, params, token):
        # Pass None (not {}) when there are no params: httpx STRIPS any query
        # string already present in the URL when handed an empty dict, which
        # breaks endpoints (e.g. leave-history) that embed the query in the path.
        return await http.get(url, params=(params or None), headers={"Authorization": f"Bearer {token}"})

    @staticmethod
    async def _do_post(http, url, body, token):
        return await http.post(url, json=body, headers={"Authorization": f"Bearer {token}"})


# ---- helpers --------------------------------------------------------------

def _flatten_keys(obj, prefix=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield f"{prefix}{k}"
            yield from _flatten_keys(v, prefix=f"{prefix}{k}.")


def _extract_tokens(data: Any) -> tuple[str | None, str | None, str | None]:
    """
    The exact response envelope isn't documented, so search common locations.
    Returns (access_token, refresh_token, user_id).
    """
    if not isinstance(data, dict):
        return None, None, None

    # Many APIs wrap payload in 'data' or 'result'.
    candidates = [data]
    for wrap in ("data", "result", "payload", "body"):
        inner = data.get(wrap)
        if isinstance(inner, dict):
            candidates.append(inner)

    access = refresh = user_id = None
    for c in candidates:
        access = access or _first(c, ["accessToken", "token", "access_token", "jwt", "idToken"])
        refresh = refresh or _first(c, ["refreshToken", "refresh_token"])
        user_id = user_id or _first(c, ["userId", "user_id", "id", "employeeId"])
    return access, refresh, (str(user_id) if user_id is not None else None)


def _first(d: dict, keys: list[str]):
    for k in keys:
        if k in d and d[k]:
            return d[k]
    return None
