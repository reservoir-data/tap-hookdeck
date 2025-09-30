"""Hookdeck tap class."""

from __future__ import annotations

from typing import override

from singer_sdk import Stream, Tap
from singer_sdk import typing as th

from tap_hookdeck import streams


class TapHookdeck(Tap):
    """Singer tap for Hookdeck."""

    name = "tap-hookdeck"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "api_key",
            th.StringType,
            required=True,
            description="API Key for Hookdeck",
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="Earliest datetime to get data from",
        ),
    ).to_dict()

    @override
    def discover_streams(self) -> list[Stream]:
        return [
            streams.Connections(tap=self),
            streams.Destinations(tap=self),
            streams.Sources(tap=self),
            streams.IssueTriggers(tap=self),
            streams.Transformations(tap=self),
            # TODO(edgarrmondragon): transformation execution logs
            # https://github.com/reservoir-data/tap-hookdeck/issues/1
            streams.Requests(tap=self),
            # TODO(edgarrmondragon): events
            # https://github.com/reservoir-data/tap-hookdeck/issues/3
            # TODO(edgarrmondragon): attempts
            # https://github.com/reservoir-data/tap-hookdeck/issues/4
            # TODO(edgarrmondragon): bookmarks
            # https://github.com/reservoir-data/tap-hookdeck/issues/5
            # TODO(edgarrmondragon): issues
            # https://github.com/reservoir-data/tap-hookdeck/issues/6
        ]
