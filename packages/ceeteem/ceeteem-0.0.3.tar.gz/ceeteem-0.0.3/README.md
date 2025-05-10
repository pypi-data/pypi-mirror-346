# ceeteem

*Token‑aware Python client for the **Control‑M Automation API***

[![PyPI](https://img.shields.io/pypi/v/ceeteem.svg)](https://pypi.org/project/ceeteem)
[![Python](https://img.shields.io/pypi/pyversions/ceeteem.svg)](https://pypi.org/project/ceeteem)
[![License](https://img.shields.io/github/license/<your‑github‑user>/ceeteem)](LICENSE)

---

`ceeteem` lets you talk to **Control‑M Workbench or a real Control‑M server** with three lines of code:

```python
from ceeteem import ControlMSession

s = ControlMSession(
    base_url="https://workbench:8443",        # host or agent port
    creds={"username": "admin", "password": "secret"},
    ca_file="certs/controlm_root.pem",        # or verify=False in dev
)

for srv in s.get_servers():
    print(srv["name"], srv.get("runAs"))
```

Behind the scenes `ceeteem`:

* Logs in once (`/session/login`) and caches the bearer token.
* Refreshes automatically when the token expires or on **401**.
* Re‑uses a single `requests.Session` so TLS handshakes are cheap.
* Lets you keep TLS **on** for self‑signed Workbench certs with a one‑liner.

---

## Installation

```bash
pip install ceeteem        # or: uv pip install ceeteem
```

Supported on **Python 3.10 +**.

---

## Key Features

| Feature             | Why it’s handy                                                                                             |
| ------------------- | ---------------------------------------------------------------------------------------------------------- |
| `ControlMSession`   | Thin wrapper around `requests.Session`; base‑URL aware; typed helpers for common Automation API endpoints. |
| `BearerTokenAuth`   | Drop‑in `AuthBase` subclass that handles login, expiry, retry.                                             |
| Custom CA bundle    | Works with Workbench’s self‑signed root CA *without* disabling TLS.                                        |
| Convenience helpers | `get_servers()`, `job_status()`, `agents_using("admin")`, … add your own easily.                           |

---

## Quick‑start

```python
from ceeteem import ControlMSession

creds = {"username": "admin", "password": "secret"}
s = ControlMSession("https://localhost:8443", creds, verify=False)

print(s.job_status("JOB123"))
```

### Using a custom CA instead of `verify=False`

```python
s = ControlMSession(
    "https://workbench:8443",
    creds,
    ca_file="certs/controlm_root.pem",
)
```

Generate the PEM once:

```bash
openssl s_client -showcerts -connect workbench:8443 </dev/null \
  | awk '/BEGIN/,/END/{print}' > certs/controlm_root.pem
```

---

## Roadmap

* [ ] Add async variant (`aiohttp`)
* [ ] Coverage for more Automation API endpoints
* [ ] Built‑in retry + backoff helpers
* [ ] CLI chat demo powered by LLM (see `/examples`)

---

## Contributing

Pull requests welcome — see [CONTRIBUTING.md](CONTRIBUTING.md) for a quick guide.

1. `git clone` & `uv sync --dev`
2. `pytest -q`
3. `pre‑commit run ‑‑all‑files`

---

## License

Licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## Acknowledgements

* BMC for the Control‑M Workbench container.
* The `requests` maintainers for rock‑solid HTTP.
* The OpenAI & Mistral teams for making language models fun to hack with.

