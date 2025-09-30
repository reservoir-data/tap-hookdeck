"""Stream type classes for tap-hookdeck."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, override

from singer_sdk import typing as th

from tap_hookdeck.client import HookdeckStream

if TYPE_CHECKING:
    from singer_sdk.helpers.types import Context


DESTINATION: list[th.Property[Any]] = [
    th.Property("id", th.StringType, required=True),
    th.Property("name", th.StringType, required=True),
    th.Property("description", th.StringType),
    th.Property("team_id", th.StringType, required=True),
    th.Property("path_forwarding_disabled", th.BooleanType),
    th.Property("url", th.StringType),
    th.Property("cli_path", th.StringType),
    th.Property("rate_limit", th.IntegerType),
    th.Property(
        "rate_limit_period",
        th.StringType(allowed_values=["second", "minute", "hour", "concurrent"]),
    ),
    th.Property(
        "http_method",
        th.StringType(
            allowed_values=[
                None,
                "GET",
                "POST",
                "PUT",
                "PATCH",
                "DELETE",
            ]
        ),
    ),
    th.Property("auth_method", th.ObjectType()),
    th.Property("archived_at", th.DateTimeType),
    th.Property("updated_at", th.DateTimeType, required=True),
    th.Property("created_at", th.DateTimeType, required=True),
    th.Property("disabled_at", th.DateTimeType),
]

SOURCE: list[th.Property[Any]] = [
    th.Property("id", th.StringType, required=True),
    th.Property("name", th.StringType, required=True),
    th.Property("description", th.StringType),
    th.Property("team_id", th.StringType, required=True),
    th.Property("url", th.StringType),
    th.Property("verification", th.ObjectType()),
    th.Property(
        "allowed_http_methods",
        th.ArrayType(
            th.StringType(
                allowed_values=[
                    None,
                    "GET",
                    "POST",
                    "PUT",
                    "PATCH",
                    "DELETE",
                ]
            )
        ),
    ),
    th.Property(
        "custom_response",
        th.ObjectType(
            th.Property(
                "content_type",
                th.StringType(allowed_values=["json", "text", "xml"]),
                required=True,
            ),
            th.Property("body", th.StringType, required=True),
        ),
    ),
    th.Property("archived_at", th.DateTimeType),
    th.Property("updated_at", th.DateTimeType, required=True),
    th.Property("created_at", th.DateTimeType, required=True),
    th.Property("disabled_at", th.DateTimeType),
]


class Connections(HookdeckStream):
    """Connections stream."""

    name = "connections"
    path = "/2024-09-01/connections"
    primary_keys = ("id",)

    # Incremental not supported
    replication_key = None

    schema = th.PropertiesList(
        th.Property("id", th.StringType, required=True),
        th.Property("name", th.StringType),
        th.Property("full_name", th.StringType),
        th.Property("description", th.StringType),
        th.Property("team_id", th.StringType, required=True),
        th.Property(
            "destination",
            th.ObjectType(*DESTINATION, additional_properties=False),
            required=True,
        ),
        th.Property(
            "source",
            th.ObjectType(*SOURCE, additional_properties=False),
            required=True,
        ),
        th.Property("rules", th.ArrayType(th.ObjectType())),
        th.Property("archived_at", th.DateTimeType),
        th.Property("paused_at", th.DateTimeType),
        th.Property("updated_at", th.DateTimeType, required=True),
        th.Property("created_at", th.DateTimeType, required=True),
        additional_properties=False,
    ).to_dict()

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
        """Get URL query parameters."""
        params = super().get_url_params(context, next_page_token)
        params["archived"] = True
        return params


class Destinations(HookdeckStream):
    """Destinations stream."""

    name = "destinations"
    path = "/2024-09-01/destinations"
    primary_keys = ("id",)

    # Incremental not supported
    replication_key = None

    schema = th.PropertiesList(
        *DESTINATION,
        additional_properties=False,
    ).to_dict()


class Sources(HookdeckStream):
    """Sources stream."""

    name = "sources"
    path = "/2024-09-01/sources"
    primary_keys = ("id",)

    # Incremental not supported
    replication_key = None

    schema = th.PropertiesList(
        *SOURCE,
        additional_properties=False,
    ).to_dict()


class IssueTriggers(HookdeckStream):
    """Issue triggers stream."""

    name = "issue_triggers"
    path = "/2024-09-01/issue-triggers"
    primary_keys = ("id",)

    # Incremental not supported
    replication_key = None

    schema = th.PropertiesList(
        th.Property("id", th.StringType, required=True),
        th.Property("team_id", th.StringType),
        th.Property("name", th.StringType),
        th.Property(
            "type",
            th.StringType(allowed_values=["delivery", "transformation", "backpressure"]),
            required=True,
        ),
        th.Property("configs", th.ObjectType()),
        th.Property(
            "channels",
            th.ObjectType(
                th.Property(
                    "slack",
                    th.ObjectType(
                        th.Property("channel_name", th.StringType, required=True),
                    ),
                ),
                th.Property("opsgenie", th.ObjectType()),
                th.Property("email", th.ObjectType()),
            ),
        ),
        th.Property("disabled_at", th.DateTimeType),
        th.Property("updated_at", th.DateTimeType, required=True),
        th.Property("created_at", th.DateTimeType, required=True),
        th.Property("deleted_at", th.DateTimeType),
        additional_properties=False,
    ).to_dict()


class Transformations(HookdeckStream):
    """Transformations stream."""

    name = "transformations"
    path = "/2024-09-01/transformations"
    primary_keys = ("id",)

    # Incremental not supported
    replication_key = None

    schema = th.PropertiesList(
        th.Property("id", th.StringType, required=True),
        th.Property("team_id", th.StringType, required=True),
        th.Property("name", th.StringType, required=True),
        th.Property("code", th.StringType, required=True),
        th.Property("encrypted_env", th.StringType),
        th.Property("iv", th.StringType),
        th.Property("env", th.ObjectType(additional_properties=th.StringType)),
        th.Property("updated_at", th.DateTimeType, required=True),
        th.Property("created_at", th.DateTimeType, required=True),
        additional_properties=False,
    ).to_dict()


class Requests(HookdeckStream):
    """Requests stream."""

    name = "requests"
    path = "/2024-09-01/requests"
    primary_keys = ("id",)

    # Incremental not supported
    replication_key = "ingested_at"

    schema = th.PropertiesList(
        th.Property("id", th.StringType, required=True),
        th.Property("team_id", th.StringType, required=True),
        th.Property("verified", th.BooleanType),
        th.Property("original_event_data_id", th.StringType),
        th.Property(
            "rejection_cause",
            th.StringType(
                allowed_values=[
                    None,
                    "SOURCE_ARCHIVED",
                    "NO_WEBHOOK",
                    "VERIFICATION_FAILED",
                    "UNSUPPORTED_HTTP_METHOD",
                    "UNSUPPORTED_CONTENT_TYPE",
                    "UNPARSABLE_JSON",
                    "PAYLOAD_TOO_LARGE",
                    "INGESTION_FATAL",
                    "UNKNOWN",
                ]
            ),
        ),
        th.Property("ingest_priority", th.StringType(allowed_values=["NORMAL", "LOW"])),
        th.Property("ingested_at", th.DateTimeType),
        th.Property("source_id", th.StringType),
        th.Property("events_count", th.IntegerType),
        th.Property("cli_events_count", th.IntegerType),
        th.Property("ignored_count", th.IntegerType),
        th.Property("updated_at", th.DateTimeType, required=True),
        th.Property("created_at", th.DateTimeType, required=True),
        additional_properties=False,
    ).to_dict()
