"""Website manager endpoints: view registered scrape targets, enable/disable
them, or register a new custom target for future scraper implementation."""

from __future__ import annotations

import re

from flask import Blueprint, jsonify, request

from services.storage import (
    add_custom_website,
    get_websites,
    remove_website,
    set_website_enabled,
    website_exists,
)
from utils.errors import APIError
from utils.validation import require_str

websites_bp = Blueprint("websites", __name__)

_KEY_SAFE_PATTERN = re.compile(r"^[a-z0-9_\-]+$")


def _get_json_body() -> dict:
    body = request.get_json(silent=True)
    if body is None or not isinstance(body, dict):
        raise APIError(
            "Request body must be valid JSON with a Content-Type of application/json.",
            status_code=400,
        )
    return body


@websites_bp.get("/api/websites")
def api_get_websites():
    """Fetch all websites (scrape targets) currently registered."""
    return jsonify({"status": "ok", "count": len(get_websites()), "websites": get_websites()}), 200


@websites_bp.post("/api/websites")
def api_post_websites():
    """Register a new custom website, or toggle an existing one on/off.

    Body shapes supported:
      - {"key": "ewn_latest", "enabled": false}          -> toggle existing target
      - {"source": "Reuters", "topic": "world",
         "url": "https://reuters.com/world", "key": "reuters_world"}
                                                          -> register a new custom target

    New custom targets are stored for tracking only -- scraping logic is
    source-specific, so a developer still needs to add a matching scraper
    module before a custom target will actually produce articles.
    """
    body = _get_json_body()

    # Toggle path: caller supplied "enabled" for an existing key.
    if "enabled" in body:
        key = require_str(body.get("key"), field_name="key")
        enabled = bool(body.get("enabled"))
        if not website_exists(key):
            raise APIError(f"No website registered with key '{key}'.", status_code=404)
        set_website_enabled(key, enabled)
        return jsonify({"status": "ok", "action": "toggled", "key": key, "enabled": enabled}), 200

    # Registration path: caller wants to add a brand-new target.
    source = require_str(body.get("source"), field_name="source")
    url = require_str(body.get("url"), field_name="url")
    topic = body.get("topic")
    key = body.get("key") or f"{source.lower().replace(' ', '_')}_{(topic or 'default').lower().replace(' ', '_')}"

    if not _KEY_SAFE_PATTERN.match(key):
        raise APIError(
            f"Invalid 'key': '{key}'. Use only lowercase letters, numbers, '_' or '-'.",
            status_code=400,
        )

    created = add_custom_website(key=key, source=source, topic=topic, url=url)
    if not created:
        raise APIError(f"A website with key '{key}' already exists.", status_code=409)

    return jsonify({"status": "ok", "action": "created", "key": key}), 201


@websites_bp.delete("/api/websites/<key>")
def api_delete_website(key: str):
    """Remove a registered website (typically a custom one)."""
    if not website_exists(key):
        raise APIError(f"No website registered with key '{key}'.", status_code=404)
    remove_website(key)
    return jsonify({"status": "ok", "action": "deleted", "key": key}), 200
