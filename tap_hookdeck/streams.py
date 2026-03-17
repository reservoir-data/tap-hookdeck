"""Stream type classes for tap-hookdeck."""

from __future__ import annotations

from importlib import resources
from typing import TYPE_CHECKING, Any, override

from singer_sdk import OpenAPISchema, StreamSchema

from tap_hookdeck.client import HookdeckStream

if TYPE_CHECKING:
    from singer_sdk.helpers.types import Context

CONFIG_SCHEMA = {
    "type": ["object", "null"],
    "additionalProperties": True,
}


class HookdeckOpenAPI(OpenAPISchema[str]):
    """Schema for all workspace-scoped streams."""

    @override
    def fetch_schema(self, key: str) -> dict[str, Any]:
        schema = super().fetch_schema(key)
        if key == "Connection":
            schema["properties"]["destination"]["properties"]["config"] = CONFIG_SCHEMA
            schema["properties"]["source"]["properties"]["config"] = CONFIG_SCHEMA
        if key == "Destination":
            schema["properties"]["config"] = CONFIG_SCHEMA
        if key == "Source":
            schema["properties"]["config"] = CONFIG_SCHEMA
        return schema


OPENAPI = HookdeckOpenAPI(resources.files("tap_hookdeck") / "openapi.json")


class Connections(HookdeckStream):
    """Connections stream."""

    name = "connections"
    path = "/connections"
    primary_keys = ("id",)
    schema = StreamSchema(OPENAPI, key="Connection")

    # Incremental not supported
    replication_key = None

    @override
    @property
    def is_sorted(self) -> bool:
        return True

    @override
    def get_url_params(
        self,
        context: Context | None,
        next_page_token: str | None,
    ) -> dict[str, Any]:
        """Get URL query parameters.

        Returns:
            Query paramaters.
        """
        params = super().get_url_params(context, next_page_token)
        params["archived"] = True
        return params


class Destinations(HookdeckStream):
    """Destinations stream."""

    name = "destinations"
    path = "/destinations"
    primary_keys = ("id",)
    schema = StreamSchema(OPENAPI, key="Destination")

    # Incremental not supported
    replication_key = None


class Sources(HookdeckStream):
    """Sources stream."""

    name = "sources"
    path = "/sources"
    primary_keys = ("id",)
    schema = StreamSchema(OPENAPI, key="Source")

    # Incremental not supported
    replication_key = None


class IssueTriggers(HookdeckStream):
    """Issue triggers stream."""

    name = "issue_triggers"
    path = "/issue-triggers"
    primary_keys = ("id",)
    schema = StreamSchema(OPENAPI, key="IssueTrigger")

    # Incremental not supported
    replication_key = None


class Transformations(HookdeckStream):
    """Transformations stream."""

    name = "transformations"
    path = "/transformations"
    primary_keys = ("id",)
    schema = StreamSchema(OPENAPI, key="Transformation")

    # Incremental not supported
    replication_key = None


class Requests(HookdeckStream):
    """Requests stream."""

    name = "requests"
    path = "/requests"
    primary_keys = ("id",)
    schema = StreamSchema(OPENAPI, key="Request")

    # Incremental not supported
    replication_key = "ingested_at"
