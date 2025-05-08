# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, TypedDict

__all__ = ["ClientListConnectionConfigsParams"]


class ClientListConnectionConfigsParams(TypedDict, total=False):
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

    expand: List[Literal["connector", "connector.schemas", "connection_count"]]

    limit: int
    """Limit the number of items returned"""

    offset: int
    """Offset the items returned"""
