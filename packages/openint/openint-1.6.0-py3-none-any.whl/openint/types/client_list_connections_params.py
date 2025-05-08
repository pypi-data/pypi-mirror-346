# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, TypedDict

__all__ = ["ClientListConnectionsParams"]


class ClientListConnectionsParams(TypedDict, total=False):
    connector_config_id: str
    """The id of the connector config, starts with `ccfg_`"""

    connector_names: List[
        Literal[
            "acme-oauth2",
            "aircall",
            "airtable",
            "apollo",
            "brex",
            "coda",
            "confluence",
            "discord",
            "facebook",
            "finch",
            "firebase",
            "foreceipt",
            "github",
            "gong",
            "google-calendar",
            "google-docs",
            "google-drive",
            "google-mail",
            "google-sheet",
            "greenhouse",
            "heron",
            "hubspot",
            "instagram",
            "intercom",
            "jira",
            "lever",
            "linear",
            "linkedin",
            "lunchmoney",
            "mercury",
            "merge",
            "moota",
            "notion",
            "onebrick",
            "outreach",
            "pipedrive",
            "plaid",
            "postgres",
            "quickbooks",
            "ramp",
            "reddit",
            "salesloft",
            "saltedge",
            "sharepoint",
            "slack",
            "splitwise",
            "stripe",
            "teller",
            "toggl",
            "twenty",
            "twitter",
            "venmo",
            "wise",
            "xero",
            "yodlee",
            "zoho-desk",
        ]
    ]

    customer_id: str
    """The id of the customer in your application.

    Ensure it is unique for that customer.
    """

    expand: List[Literal["connector"]]
    """Expand the response with additional optionals"""

    include_secrets: bool

    limit: int
    """Limit the number of items returned"""

    offset: int
    """Offset the items returned"""
