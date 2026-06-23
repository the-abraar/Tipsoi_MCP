"""
OAuth 2.1 Authorization Server routes for the Tipsoi MCP connector.

Tipsoi uses email/password, not OAuth. This module wraps that into a
proper OAuth 2.1 Authorization Code + PKCE flow so Claude (and any
MCP-compatible client) can authenticate users without handling passwords.

Flow:
  1. Claude opens /authorize?client_id=...&redirect_uri=...&state=...&code_challenge=...
  2. User sees our login form and enters their Tipsoi email + password
  3. We authenticate against Tipsoi, get a session token
  4. We issue a short-lived auth code and redirect to Claude's callback
  5. Claude POSTs to /token with the code + code_verifier → gets our access token
  6. Every subsequent MCP call includes Authorization: Bearer <our_token>
  7. Our middleware maps that token back to the Tipsoi session
"""

from __future__ import annotations

import json
import os
import secrets
import urllib.parse
from typing import Any

import httpx
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, RedirectResponse, Response
from starlette.routing import Route

from .token_store import token_store, UserSession

_BASE_URL = os.environ.get("TIPSOI_BASE_URL", "https://hrm.tipsoi.pro/inovace-client/api/v1").rstrip("/")


# ---------------------------------------------------------------------------
# Login page HTML
# ---------------------------------------------------------------------------

_LOGIN_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Tipsoi · Connect to Claude</title>
  <style>
    *,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
    body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
         background:#f5f5f5;min-height:100vh;display:flex;align-items:center;justify-content:center}
    .card{background:#fff;border-radius:12px;box-shadow:0 4px 24px rgba(0,0,0,.10);
          padding:40px;width:100%;max-width:400px}
    .logo{display:flex;align-items:center;gap:10px;margin-bottom:28px}
    .logo-dot{width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,#4f46e5,#7c3aed);
              display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:16px}
    .logo-name{font-size:20px;font-weight:700;color:#111}
    h1{font-size:18px;font-weight:600;color:#111;margin-bottom:6px}
    p.sub{font-size:14px;color:#666;margin-bottom:24px}
    label{display:block;font-size:13px;font-weight:500;color:#444;margin-bottom:6px}
    input{width:100%;padding:10px 14px;border:1.5px solid #ddd;border-radius:8px;font-size:14px;
          outline:none;transition:border-color .2s}
    input:focus{border-color:#4f46e5}
    .field{margin-bottom:16px}
    .error{background:#fef2f2;border:1px solid #fecaca;color:#dc2626;
           padding:10px 14px;border-radius:8px;font-size:13px;margin-bottom:16px}
    button{width:100%;padding:12px;background:#4f46e5;color:#fff;border:none;
           border-radius:8px;font-size:15px;font-weight:600;cursor:pointer;transition:background .2s}
    button:hover{background:#4338ca}
    .footer{margin-top:20px;text-align:center;font-size:12px;color:#999}
  </style>
</head>
<body>
  <div class="card">
    <div class="logo">
      <div class="logo-dot">T</div>
      <span class="logo-name">Tipsoi HRM</span>
    </div>
    <h1>Connect to Claude</h1>
    <p class="sub">Sign in with your Tipsoi credentials to let Claude access your HRM data.</p>
    {error_block}
    <form method="POST" action="/authorize">
      <input type="hidden" name="redirect_uri" value="{redirect_uri}">
      <input type="hidden" name="state" value="{state}">
      <input type="hidden" name="client_id" value="{client_id}">
      <input type="hidden" name="code_challenge" value="{code_challenge}">
      <input type="hidden" name="code_challenge_method" value="{code_challenge_method}">
      <div class="field">
        <label for="email">Work email</label>
        <input id="email" type="email" name="email" required placeholder="you@company.com" value="{prefill_email}">
      </div>
      <div class="field">
        <label for="password">Password</label>
        <input id="password" type="password" name="password" required placeholder="••••••••">
      </div>
      <button type="submit">Connect →</button>
    </form>
    <p class="footer">Your credentials are sent directly to Tipsoi and never stored.</p>
  </div>
</body>
</html>"""


def _login_page(
    redirect_uri: str = "",
    state: str = "",
    client_id: str = "",
    code_challenge: str = "",
    code_challenge_method: str = "",
    error: str = "",
    prefill_email: str = "",
) -> HTMLResponse:
    error_block = f'<div class="error">{_esc(error)}</div>' if error else ""
    # NOTE: use literal-string replacement, NOT str.format(): the <style> block
    # contains CSS braces ({...}) that str.format() would parse as replacement
    # fields and raise KeyError. Replacement on explicit {token} markers is safe.
    replacements = {
        "{redirect_uri}": _esc(redirect_uri),
        "{state}": _esc(state),
        "{client_id}": _esc(client_id),
        "{code_challenge}": _esc(code_challenge),
        "{code_challenge_method}": _esc(code_challenge_method),
        "{error_block}": error_block,
        "{prefill_email}": _esc(prefill_email),
    }
    html = _LOGIN_HTML
    for token, value in replacements.items():
        html = html.replace(token, value)
    return HTMLResponse(html)


def _esc(s: str) -> str:
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _server_base(request: Request) -> str:
    """Best-effort server base URL."""
    fwd_proto = request.headers.get("x-forwarded-proto")
    fwd_host = request.headers.get("x-forwarded-host")
    if fwd_proto and fwd_host:
        return f"{fwd_proto}://{fwd_host}"
    return str(request.base_url).rstrip("/")


async def _tipsoi_sign_in(email: str, password: str) -> dict[str, Any]:
    """Call Tipsoi sign-in; return response JSON or raise ValueError."""
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.post(
            f"{_BASE_URL}/auth/external-sync/sign-in",
            json={"email": email, "password": password},
        )
    if resp.status_code >= 400:
        raise ValueError(f"Invalid email or password ({resp.status_code})")
    return resp.json()


def _extract_tokens(data: Any) -> tuple[str | None, str | None, str | None]:
    if not isinstance(data, dict):
        return None, None, None
    candidates = [data]
    for wrap in ("data", "result", "payload", "body"):
        inner = data.get(wrap)
        if isinstance(inner, dict):
            candidates.append(inner)
    access = refresh = user_id = None
    for c in candidates:
        access = access or _first(c, ["accessToken", "token", "access_token", "jwt"])
        refresh = refresh or _first(c, ["refreshToken", "refresh_token"])
        user_id = user_id or _first(c, ["userId", "user_id", "employeeId", "id"])
    return access, refresh, (str(user_id) if user_id is not None else None)


def _first(d: dict, keys: list) -> Any:
    for k in keys:
        if k in d and d[k]:
            return d[k]
    return None


async def _get_employee_office(access_token: str, user_id: str) -> tuple[str | None, str | None]:
    """Fetch the employee's officeId and companyId from their profile."""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(
                f"{_BASE_URL}/employee/basic-profile/{user_id}",
                headers={"Authorization": f"Bearer {access_token}"},
            )
        if resp.status_code == 200:
            data = resp.json()
            # Flatten candidates
            candidates = [data]
            for wrap in ("data", "result", "employee"):
                inner = data.get(wrap)
                if isinstance(inner, dict):
                    candidates.append(inner)
            for c in candidates:
                oid = _first(c, ["officeId", "office_id", "workplaceId"])
                cid = _first(c, ["companyId", "company_id"])
                if oid:
                    return str(oid), (str(cid) if cid else None)
    except Exception:
        pass
    # Fall back to env vars
    return os.environ.get("TIPSOI_OFFICE_ID"), os.environ.get("TIPSOI_COMPANY_ID")


# ---------------------------------------------------------------------------
# Route handlers
# ---------------------------------------------------------------------------

async def oauth_metadata(request: Request) -> JSONResponse:
    """RFC 8414 — Authorization Server Metadata."""
    base = _server_base(request)
    return JSONResponse({
        "issuer": base,
        "authorization_endpoint": f"{base}/authorize",
        "token_endpoint": f"{base}/token",
        "registration_endpoint": f"{base}/register",
        "response_types_supported": ["code"],
        "grant_types_supported": ["authorization_code"],
        "code_challenge_methods_supported": ["S256"],
        "token_endpoint_auth_methods_supported": ["none"],
    })


async def protected_resource_metadata(request: Request) -> JSONResponse:
    """RFC 9728 — Protected Resource Metadata."""
    base = _server_base(request)
    return JSONResponse({
        "resource": f"{base}/mcp",
        "authorization_servers": [base],
    })


async def register(request: Request) -> JSONResponse:
    """RFC 7591 — Dynamic Client Registration."""
    try:
        body = await request.json()
    except Exception:
        body = {}
    client_id = secrets.token_urlsafe(16)
    token_store.register_client(client_id, body)
    return JSONResponse({
        "client_id": client_id,
        "client_id_issued_at": int(__import__("time").time()),
        "redirect_uris": body.get("redirect_uris", []),
        "grant_types": ["authorization_code"],
        "response_types": ["code"],
        "token_endpoint_auth_method": "none",
    }, status_code=201)


async def authorize_get(request: Request) -> HTMLResponse:
    """Show the Tipsoi login form."""
    p = request.query_params
    redirect_uri = p.get("redirect_uri", "")
    state = p.get("state", "")
    client_id = p.get("client_id", "")
    code_challenge = p.get("code_challenge", "")
    code_challenge_method = p.get("code_challenge_method", "S256")

    if not redirect_uri:
        return HTMLResponse("Missing redirect_uri", status_code=400)
    if not token_store.client_allows_redirect(client_id, redirect_uri):
        return HTMLResponse("Invalid redirect_uri for this client", status_code=400)
    # OAuth 2.1 / MCP require PKCE on the authorization code flow.
    if not code_challenge:
        return HTMLResponse("Missing code_challenge (PKCE required)", status_code=400)
    if code_challenge_method != "S256":
        return HTMLResponse("Unsupported code_challenge_method (S256 required)", status_code=400)

    return _login_page(
        redirect_uri=redirect_uri,
        state=state,
        client_id=client_id,
        code_challenge=code_challenge,
        code_challenge_method=code_challenge_method,
    )


async def authorize_post(request: Request) -> Response:
    """Handle login form submission."""
    form = await request.form()
    email = str(form.get("email", "")).strip()
    password = str(form.get("password", ""))
    redirect_uri = str(form.get("redirect_uri", ""))
    state = str(form.get("state", ""))
    client_id = str(form.get("client_id", ""))
    code_challenge = str(form.get("code_challenge", ""))
    code_challenge_method = str(form.get("code_challenge_method", "S256"))

    if not redirect_uri:
        return HTMLResponse("Missing redirect_uri", status_code=400)
    if not token_store.client_allows_redirect(client_id, redirect_uri):
        return HTMLResponse("Invalid redirect_uri for this client", status_code=400)
    if not code_challenge:
        return HTMLResponse("Missing code_challenge (PKCE required)", status_code=400)

    def show_error(msg: str) -> HTMLResponse:
        return _login_page(
            redirect_uri=redirect_uri,
            state=state,
            client_id=client_id,
            code_challenge=code_challenge,
            code_challenge_method=code_challenge_method,
            error=msg,
            prefill_email=email,
        )

    # Authenticate against Tipsoi
    try:
        data = await _tipsoi_sign_in(email, password)
    except ValueError as e:
        return show_error(str(e))
    except Exception:
        return show_error("Could not reach Tipsoi. Please try again.")

    access_token, refresh_token, user_id = _extract_tokens(data)
    if not access_token:
        return show_error("Sign-in succeeded but no token received. Contact support.")

    # Get user's office
    office_id, company_id = None, None
    if user_id:
        office_id, company_id = await _get_employee_office(access_token, user_id)

    session = UserSession(
        email=email,
        access_token=access_token,
        refresh_token=refresh_token,
        user_id=user_id,
        office_id=office_id,
        company_id=company_id,
    )

    code = token_store.create_code(
        session=session,
        redirect_uri=redirect_uri,
        client_id=client_id,
        code_challenge=code_challenge or None,
        code_challenge_method=code_challenge_method or None,
    )

    # Redirect back to Claude with code
    params = {"code": code}
    if state:
        params["state"] = state
    sep = "&" if "?" in redirect_uri else "?"
    location = redirect_uri + sep + urllib.parse.urlencode(params)
    return RedirectResponse(location, status_code=302)


async def authorize(request: Request) -> Response:
    if request.method == "GET":
        return await authorize_get(request)
    return await authorize_post(request)


async def token(request: Request) -> JSONResponse:
    """Token endpoint — exchange auth code for access token."""
    content_type = request.headers.get("content-type", "")
    if "application/json" in content_type:
        try:
            body = await request.json()
        except Exception:
            body = {}
    else:
        form = await request.form()
        body = dict(form)

    grant_type = body.get("grant_type", "")
    if grant_type != "authorization_code":
        return JSONResponse({"error": "unsupported_grant_type"}, status_code=400)

    code = body.get("code", "")
    redirect_uri = body.get("redirect_uri", "")
    code_verifier = body.get("code_verifier") or None

    session = token_store.exchange_code(
        code=code,
        redirect_uri=redirect_uri,
        code_verifier=code_verifier,
    )
    if session is None:
        return JSONResponse({"error": "invalid_grant"}, status_code=400)

    access_token = token_store.create_token(session)
    return JSONResponse({
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": 86400 * 7,
        "scope": "tipsoi:read tipsoi:write",
    })


# ---------------------------------------------------------------------------
# Route list
# ---------------------------------------------------------------------------

def make_routes() -> list[Route]:
    return [
        Route("/.well-known/oauth-authorization-server", oauth_metadata, methods=["GET"]),
        Route("/.well-known/oauth-protected-resource", protected_resource_metadata, methods=["GET"]),
        Route("/register", register, methods=["POST"]),
        Route("/authorize", authorize, methods=["GET", "POST"]),
        Route("/token", token, methods=["POST"]),
    ]
