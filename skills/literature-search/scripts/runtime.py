"""Shared configuration and bounded HTTP requests; Python standard library only."""

import json
import os
import threading
import time
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import ProxyHandler, Request, build_opener


FIELDS = {
    "email": "LITERATURE_EMAIL",
    "openalex_api_key": "OPENALEX_API_KEY",
    "semantic_scholar_api_key": "SEMANTIC_SCHOLAR_API_KEY",
    "ncbi_api_key": "NCBI_API_KEY",
    "http_proxy": "HTTP_PROXY",
    "https_proxy": "HTTPS_PROXY",
}
DEFAULT_CONFIG = Path.home() / ".config" / "literature-search" / "config.json"


class SourceError(Exception):
    def __init__(self, status, message):
        self.status = status
        super().__init__(message)


def load_config(path=None):
    target = Path(path) if path else DEFAULT_CONFIG
    data = json.loads(target.read_text(encoding="utf-8-sig")) if target.exists() else {}
    if not isinstance(data, dict) or set(data) - set(FIELDS):
        raise ValueError("Config must be an object containing only the documented six fields")
    if any(not isinstance(v, str) for v in data.values()):
        raise ValueError("Config values must be strings")
    return {key: (os.environ.get(env) or data.get(key, "")).strip() for key, env in FIELDS.items()}


class Http:
    def __init__(self, config, timeout=20, retries=1):
        self.config = config
        self.timeout = timeout
        self.retries = retries
        proxies = {p: config[p + "_proxy"] for p in ("http", "https") if config[p + "_proxy"]}
        self.opener = build_opener(ProxyHandler(proxies)) if proxies else build_opener()
        self._guard = threading.Lock()
        self._locks = {}
        self._last = {}
        self._cache = {}

    def get(self, source, url, params=None, headers=None, interval=0.3):
        if params:
            url += "?" + urlencode({k: v for k, v in params.items() if v is not None})
        request_headers = {"User-Agent": "literature-search/1.0"}
        if self.config["email"]:
            request_headers["User-Agent"] += " (mailto:" + self.config["email"] + ")"
        request_headers.update(headers or {})
        cache_key = (url, tuple(sorted(request_headers.items())))
        with self._guard:
            lock = self._locks.setdefault(source, threading.Lock())
        # Serialise requests per provider, including retry attempts, across worker threads.
        with lock:
            if cache_key in self._cache:
                return self._cache[cache_key]
            for attempt in range(self.retries + 1):
                time.sleep(max(0, interval - (time.monotonic() - self._last.get(source, 0))))
                self._last[source] = time.monotonic()
                try:
                    with self.opener.open(Request(url, headers=request_headers), timeout=self.timeout) as response:
                        raw = response.read()
                    self._cache[cache_key] = raw
                    return raw
                except HTTPError as exc:
                    retryable = exc.code == 429 or 500 <= exc.code < 600
                    delay = exc.headers.get("Retry-After", "") if exc.headers else ""
                    if retryable and attempt < self.retries:
                        seconds = int(delay) if delay.isdigit() else 0
                        if delay and not delay.isdigit():
                            try:
                                retry_date = parsedate_to_datetime(delay)
                                if retry_date.tzinfo is None:
                                    retry_date = retry_date.replace(tzinfo=timezone.utc)
                                seconds = max(0, (retry_date - datetime.now(timezone.utc)).total_seconds())
                            except (ValueError, TypeError, OverflowError):
                                pass
                        if seconds > 30:
                            raise SourceError("rate_limited", "Retry-After exceeds automatic retry budget") from None
                        time.sleep(max(2 ** attempt, seconds))
                        continue
                    status = {401: "unauthorized", 403: "forbidden", 404: "not_found", 429: "rate_limited"}.get(exc.code, "http_error")
                    raise SourceError(status, f"{source}: HTTP {exc.code}") from None
                except (URLError, TimeoutError, OSError):
                    if attempt < self.retries:
                        time.sleep(2 ** attempt)
                        continue
                    # Exception URLs can contain NCBI keys or proxy credentials.
                    raise SourceError("network_error", f"{source}: network, TLS, or timeout failure") from None

    def json(self, *args, **kwargs):
        try:
            return json.loads(self.get(*args, **kwargs))
        except (ValueError, UnicodeError):
            raise SourceError("invalid_response", "Source returned invalid JSON") from None
