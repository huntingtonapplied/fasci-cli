"""fasci API client — thin wrapper around httpx."""

import json
import os
import time
from typing import Any, Dict, Optional

import httpx

from fasci_cli.config import get_api_key, get_api_url, load_config
from fasci_cli.log import logger

MAX_RETRIES = int(os.getenv("FASCI_MAX_RETRIES", "3"))
RETRY_BACKOFF_BASE = 1.0
RETRY_BACKOFF_MAX = 30.0
RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}
RETRYABLE_EXCEPTIONS = (httpx.ConnectError, httpx.TimeoutException)


def as_list(data: Any, *resource_keys: str) -> list:
    """Normalize a list endpoint's response to a plain list of rows.

    Backends return list collections in several envelope shapes: a bare array,
    or a dict keyed by the resource name ({"boosts":[...]}), or a generic wrapper
    ({"data"/"items"/"results":[...]}). Returning the raw dict makes callers iterate
    its KEYS -> `'str' has no attribute 'get'`, and slicing it -> `unhashable slice`
    (the HQ2 🅐 class). Try the resource key(s) first, then the generic wrappers.
    """
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in (*resource_keys, "items", "data", "results"):
            value = data.get(key)
            if isinstance(value, list):
                return value
        return []
    return []


_ERROR_HINTS = {
    401: ["Run: fasci login", "Or set FASCI_API_KEY env var"],
    403: ["You may not have access to this resource."],
    404: ["The resource was not found.", "Run: fasci campaigns list"],
    422: ["The request data is invalid."],
    429: ["Rate limit exceeded."],
    500: ["Server error. Try again in a few minutes."],
}


def format_error_hint(status_code: int) -> str:
    hints = _ERROR_HINTS.get(status_code, [])
    if not hints:
        return ""
    return "\n".join(f"  {h}" for h in hints)


class AuthError(Exception):
    pass


class APIError(Exception):
    def __init__(self, message: str, status_code: int = 0):
        super().__init__(message)
        self.status_code = status_code


class FasciClient:
    """HTTP client for the fasci API."""

    def __init__(self, api_key: Optional[str] = None, api_url: Optional[str] = None):
        self.api_key = api_key or get_api_key()
        self.api_url = api_url or get_api_url()

        if not self.api_key:
            raise AuthError("Not authenticated.\n  Run: fasci login")

        config = load_config()
        self._timeout = float(os.getenv("FASCI_TIMEOUT", config.get("timeout", 60)))
        self._client = httpx.Client(base_url=self.api_url, timeout=self._timeout)

    def _headers(self) -> Dict[str, str]:
        # X-API-Key is fasci's canonical api-key header — it authenticates on every
        # route (campaigns/boosts/subscriptions). The legacy `Authorization: ApiKey`
        # form is only honored by the permissive campaigns dependency, so sending it
        # alone 401s `boosts list`/`subscriptions me`. Send both (additive, no regression).
        return {
            "Content-Type": "application/json",
            "X-API-Key": self.api_key,
            "Authorization": f"ApiKey {self.api_key}",
        }

    def _request_with_retry(self, method: str, path: str, **kwargs) -> httpx.Response:
        last_exc = None
        for attempt in range(MAX_RETRIES + 1):
            try:
                resp = getattr(self._client, method)(path, headers=self._headers(), **kwargs)
                if resp.status_code not in RETRYABLE_STATUS_CODES or attempt == MAX_RETRIES:
                    return resp
                delay = min(RETRY_BACKOFF_BASE * (2 ** attempt), RETRY_BACKOFF_MAX)
                time.sleep(delay)
            except RETRYABLE_EXCEPTIONS as exc:
                last_exc = exc
                if attempt == MAX_RETRIES:
                    raise
                time.sleep(min(RETRY_BACKOFF_BASE * (2 ** attempt), RETRY_BACKOFF_MAX))
        raise last_exc or APIError("Request failed after retries")

    def get(self, path: str, params: Optional[Dict] = None) -> Any:
        resp = self._request_with_retry("get", path, params=params)
        return self._handle_response(resp)

    def post(self, path: str, data: Optional[Dict] = None) -> Any:
        resp = self._request_with_retry("post", path, json=data)
        return self._handle_response(resp)

    def put(self, path: str, data: Optional[Dict] = None) -> Any:
        resp = self._request_with_retry("put", path, json=data)
        return self._handle_response(resp)

    def delete(self, path: str) -> Any:
        resp = self._request_with_retry("delete", path)
        if resp.status_code == 204:
            return None
        return self._handle_response(resp)

    def _handle_response(self, resp: httpx.Response) -> Any:
        if resp.status_code == 401:
            raise AuthError("Not authenticated.")
        if resp.status_code >= 400:
            detail = ""
            try:
                body = resp.json()
                detail = body.get("detail", resp.text)
            except Exception:
                detail = resp.text
            hint = format_error_hint(resp.status_code)
            msg = f"API error {resp.status_code}: {detail}"
            if hint:
                msg += f"\n{hint}"
            raise APIError(msg, status_code=resp.status_code)
        if resp.status_code == 204 or not resp.content:
            return None
        return resp.json()

    # Campaign operations
    def list_campaigns(self, params: Optional[Dict] = None) -> list:
        data = self.get("/v1/campaigns", params=params)
        return as_list(data, "campaigns")

    def get_campaign(self, campaign_id: str) -> dict:
        return self.get(f"/v1/campaigns/{campaign_id}")

    def create_campaign(self, data: dict) -> dict:
        return self.post("/v1/campaigns", data)

    def update_campaign(self, campaign_id: str, data: dict) -> dict:
        return self.put(f"/v1/campaigns/{campaign_id}", data)

    def delete_campaign(self, campaign_id: str) -> None:
        self.delete(f"/v1/campaigns/{campaign_id}")

    # Boost operations
    def list_boosts(self, params: Optional[Dict] = None) -> list:
        data = self.get("/v1/boosts", params=params)
        return as_list(data, "boosts")

    def get_boost(self, boost_id: str) -> dict:
        return self.get(f"/v1/boosts/{boost_id}")

    def create_boost(self, data: dict) -> dict:
        return self.post("/v1/boosts", data)

    def cancel_boost(self, boost_id: str) -> dict:
        return self.post(f"/v1/boosts/{boost_id}/cancel", {})

    # Subscription operations
    def get_my_subscription(self) -> Optional[dict]:
        return self.get("/v1/subscriptions/me")

    def list_subscription_tiers(self) -> list:
        return self.get("/v1/subscriptions/tiers")

    # User operations
    def get_current_user(self) -> dict:
        return self.get("/v1/users/me")

    # Metrics operations
    def get_portfolio_metrics(self) -> dict:
        return self.get("/v1/metrics/portfolio")
