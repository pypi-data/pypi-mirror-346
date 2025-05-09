import time
import threading
from typing import Dict, Optional

import requests
from requests.auth import AuthBase
from requests import Response


class BearerTokenAuth(AuthBase):
    """
    Plug this into `session.auth` (or the `auth=` kwarg) and every request
    will carry a fresh Bearer token automatically.

    Parameters
    ----------
    auth_url : str
        Endpoint that issues tokens (e.g. "/v1/login").
    auth_payload : dict[str, str]
        Whatever the endpoint expects (user, password, client_id …).
    token_field : str, default "access_token"
        JSON key in the auth response that contains the new token.
    expires_field : str|None, default "expires_in"
        Key whose value (seconds) tells us when the token becomes invalid.
        If None, a 401 will be the only refresh trigger.
    header_name : str, default "Authorization"
        Header that should carry the token.
    scheme : str, default "Bearer"
        Prepended to the raw token in the header.
    refresh_slack : int, default 30
        Seconds before *expires_at* at which we proactively refresh.
    """

    def __init__(
        self,
        auth_url: str,
        auth_payload: Dict[str, str],
        *,
        token_field: str = "token",
        expires_field: Optional[str] = "expires_in",
        header_name: str = "Authorization",
        scheme: str = "Bearer",
        refresh_slack: int = 30,
        session: Optional[requests.Session] = None,
    ) -> None:
        self.auth_url = auth_url
        self.auth_payload = auth_payload
        self.token_field = token_field
        self.expires_field = expires_field
        self.header_name = header_name
        self.scheme = scheme
        self.refresh_slack = refresh_slack
        self._session = session or requests.Session()

        # Internal state
        self._token: Optional[str] = None
        self._expires_at: Optional[float] = None
        self._lock = threading.Lock()  # ← thread‑safe in multi‑threaded programs

    # ------------------------------------------------------------------ #
    # Public API – this is what Requests calls for *every* outgoing req. #
    # ------------------------------------------------------------------ #
    def __call__(self, r: requests.PreparedRequest) -> requests.PreparedRequest:
        # Ensure we have a usable token before the request leaves.
        if self._needs_refresh():
            self._refresh_token()

        r.headers[self.header_name] = f"{self.scheme} {self._token}"
        # Hook so we can retry automatically on 401s:
        r.register_hook("response", self._response_hook)

        return r

    # -------------------- #
    # Internal helpers     #
    # -------------------- #
    def _needs_refresh(self) -> bool:
        if self._token is None:  # first call
            return True
        if self._expires_at is None:  # lifetime unknown – rely on 401 hook
            return False
        return time.time() + self.refresh_slack >= self._expires_at  # about to expire

    def _refresh_token(self) -> None:
        """POST credentials → cache token (and optional expiry)."""
        with self._lock:  # keep threads from racing the refresh
            # Another thread may have refreshed while we waited
            if not self._needs_refresh():
                return

            response = self._session.post(
                self.auth_url, json=self.auth_payload, timeout=10
            )
            response.raise_for_status()

            data = response.json()
            self._last_repsonse = response
            try:
                self._token = data[self.token_field]
            except KeyError as e:
                raise ValueError(
                    f"Auth response missing '{self.token_field}' field"
                ) from e

            if self.expires_field in data:
                self._expires_at = time.time() + int(data[self.expires_field])

    # 401 handler – retry once with a fresh token
    def _response_hook(self, r: Response, *args, **kwargs) -> Response:
        if r.status_code == 401 and not r.request.headers.get("_retry"):
            # Invalidate and fetch a new token
            self._token = None
            self._refresh_token()

            new_req = r.request.copy()
            new_req.headers[self.header_name] = f"{self.scheme} {self._token}"
            new_req.headers["_retry"] = "1"  # guard against infinite loop
            # Send the cloned request through the same connection
            return r.connection.send(new_req, **kwargs)

        return r

