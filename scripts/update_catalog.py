#!/usr/bin/env python

"""Update the OpenAPI schema from the Hook API.

Copyright (c) 2026 Edgar Ramírez-Mondragón
"""

from __future__ import annotations

import http
import json
import logging
import pathlib
import sys

import requests

from tap_hookdeck.client import API_VERSION

OPENAPI_URL = f"https://api.hookdeck.com/{API_VERSION}/openapi"
PATH = "tap_hookdeck/openapi.json"

logging.basicConfig(format="%(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger()


def main() -> None:
    """Update the OpenAPI schema from the Hookdeck API."""
    logger.info("Updating OpenAPI schema from %s", OPENAPI_URL)
    response = requests.get(OPENAPI_URL, timeout=60, allow_redirects=True)
    if response.status_code != http.HTTPStatus.OK:
        logger.error("Failed to fetch OpenAPI spec: %s", response.reason)
        sys.exit(1)

    spec = response.json()
    content = json.dumps(spec, indent=2) + "\n"
    pathlib.Path(PATH).write_text(content, encoding="utf-8")


if __name__ == "__main__":
    main()
