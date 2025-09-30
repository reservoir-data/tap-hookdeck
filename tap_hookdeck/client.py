"""REST client handling, including HookdeckStream base class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, override

from singer_sdk import RESTStream
from singer_sdk.authenticators import APIKeyAuthenticator
from singer_sdk.helpers._typing import TypeConformanceLevel

if TYPE_CHECKING:
    from singer_sdk.helpers.types import Context


class HookdeckStream(RESTStream[str]):
    """Hookdeck stream class."""

    url_base = "https://api.hookdeck.com"
    records_jsonpath = "$.models[*]"
    next_page_token_jsonpath = "$.pagination.next"  # noqa: S105

    TYPE_CONFORMANCE_LEVEL = TypeConformanceLevel.ROOT_ONLY

    @override
    @property
    def authenticator(self) -> APIKeyAuthenticator:
        """Get an authenticator object.

        Returns:
            The authenticator instance for this REST stream.
        """
        return APIKeyAuthenticator(
            key="Authorization",
            value=f"Bearer {self.config['api_key']}",
            location="header",
        )

    @override
    def get_url_params(
        self,
        context: Context | None,
        next_page_token: str | None,
    ) -> dict[str, Any]:
        """Get URL query parameters.

        Args:
            context: Stream sync context.
            next_page_token: Next offset.

        Returns:
            Mapping of URL query parameters.
        """
        # https://hookdeck.com/docs/api#paging
        params: dict[str, Any] = {
            "limit": 250,
        }

        if next_page_token:
            params["next"] = next_page_token

        if self.replication_key and (start_date := self.get_starting_timestamp(context)):
            params[f"{self.replication_key}[gte]"] = start_date.isoformat(sep="T")

        if self.is_sorted:
            params["order_by"] = self.replication_key
            params["dir"] = "asc"
        return params
