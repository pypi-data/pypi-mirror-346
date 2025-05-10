"""controlm_session.py
A thin, typed wrapper around ``requests.Session`` that automatically:

* Authenticates against Control‑M (Workbench or a real server) using the
  custom ``ControlMAuth`` class we sketched earlier.
* Prepends ``base_url`` so callers can use nice, relative paths ("/automation-api/..."),
  just like ``Flask.test_client``.
* Exposes a handful of convenience helpers for common Control‑M Automation API
  endpoints—you can add your own domain‑specific helpers later.

Usage
-----
>>> from controlm_session import ControlMSession
>>> s = ControlMSession(
...         base_url="https://workbench:8443",                 # Control‑M host
...         creds={"username": "admin", "password": "secret"},
...         ca_file="certs/controlm_root.pem",                 # or verify=False during dev
... )
>>> s.get_servers()
[{'name': 'ctm-ag-agent', 'host': 'ctm-ag', ...}, ...]

If you pass ``verify=False`` or point to a PEM bundle in ``ca_file`` the same
setting applies to the hidden login request made by ``ControlMAuth`` because
it re‑uses **the same Session instance**.
"""
from __future__ import annotations

import pathlib
from typing import Any, Dict, Iterable, List, Optional
from urllib.parse import urljoin

import requests
from requests.auth import AuthBase

# Import your custom AuthBase subclass.
# Rename this import if you called the class BearerTokenAuth, etc.
from .auth import BearerTokenAuth  # type: ignore


class ControlMSession(requests.Session):
    """Session pre‑configured for Control‑M Automation API calls.

    Parameters
    ----------
    base_url : str
        The *root* URL for the Control‑M Automation API, e.g.
        ``"https://workbench:8443"``.
    creds : dict[str, str]
        Whatever payload your ``/session/login`` endpoint expects—typically
        ``{"username": "...", "password": "..."}``.
    verify : bool | str, default ``True``
        Passed straight to :pyclass:`requests.Session.request`.  Use ``False``
        to disable validation (dev only) **or** provide the path to a PEM file
        that contains the Control‑M Root CA.
    ca_file : str | None, default ``None``
        Convenience alias for *verify* when you want to be explicit.  If set
        it overrides *verify*.
    auth_cls : type[AuthBase], default :pyclass:`ControlMAuth`
        Lets you drop‑in a different token strategy if needed (OIDC, etc.).
    **auth_kwargs
        Extra keyword arguments forwarded to ``auth_cls``.
    """

    def __init__(
        self,
        base_url: str,
        creds: Dict[str, str],
        *,
        verify: bool | str = True,
        ca_file: Optional[str] = None,
        auth_cls: type[AuthBase] = BearerTokenAuth,
        **auth_kwargs: Any,
    ) -> None:
        super().__init__()

        self.base_url = base_url.rstrip("/")
        if not(base_url.rstrip("/").endswith("automation-api")):
            self.base_url = self.base_url.rstrip("/") + "/automation-api"
        # verify precedence: explicit ca_file > verify param > default True
        self.verify = ca_file if ca_file is not None else verify

        # Instantiate custom Auth once and re‑use *this* Session for the
        # login calls so "verify" settings propagate.
        self.auth = auth_cls(
            auth_url=f"{self.base_url}/session/login",
            auth_payload=creds,
            session=self,
            **auth_kwargs,
        )

        # JSON everywhere 🚀
        self.headers.setdefault("Accept", "application/json")

    # ---------------------------------------------------------------------
    # Core override: prepend base_url so callers can use nice relative paths.
    # ---------------------------------------------------------------------
    def request(self, method: str, url: str, *args: Any, **kwargs: Any):  # type: ignore[override]
        full_url = (
            urljoin(self.base_url + "/", url.lstrip("/")) if url.startswith("/") else url
        )
        return super().request(method, full_url, *args, **kwargs)

    # ------------------------------------------------------------------
    # Convenience helpers – thin wrappers that return .json() or Response.
    # ------------------------------------------------------------------
    # Config / topology
    def get_servers(self) -> List[Dict[str, Any]]:
        """Return *all* servers/agents as JSON list."""
        return self.get("/config/servers").json()

    def get_server(self, server_name: str) -> Dict[str, Any]:
        return self.get(f"/config/servers/{server_name}").json()

    # Runtime queries
    def job_status(self, job_id: str) -> Dict[str, Any]:
        return self.get(f"/run/jobs/{job_id}/status").json()

    def folder_status(self, folder: str) -> Dict[str, Any]:
        return self.get(f"/run/folders/{folder}/instances").json()

    # Custom example – find agents whose RunAs matches a given user.
    def agents_using(self, username: str) -> List[str]:
        """Return server names whose *runAs* equals *username*."""
        return [srv["name"] for srv in self.get_servers() if srv.get("runAs") == username]

    # You can add more domain‑specific helpers below ...


# ---------------------------------------------------------------------
# __all__ for tidy star‑imports
# ---------------------------------------------------------------------
__all__: Iterable[str] = ["ControlMSession"]

