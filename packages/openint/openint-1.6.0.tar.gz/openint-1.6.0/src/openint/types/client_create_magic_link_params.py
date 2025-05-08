# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, TypedDict

__all__ = ["ClientCreateMagicLinkParams", "ConnectOptions"]


class ClientCreateMagicLinkParams(TypedDict, total=False):
    connect_options: ConnectOptions

    validity_in_seconds: float
    """How long the magic link will be valid for (in seconds) before it expires"""


class ConnectOptions(TypedDict, total=False):
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
    """The names of the connectors to show in the connect page.

    If not provided, all connectors will be shown
    """

    debug: bool
    """Whether to enable debug mode"""

    is_embedded: bool
    """Whether to enable embedded mode.

    Embedded mode hides the side bar with extra context for the end user (customer)
    on the organization
    """

    return_url: str
    """
    Optional URL to return customers after adding a connection or if they press the
    Return To Organization button
    """

    view: Literal["add", "manage"]
    """The default view to show when the magic link is opened.

    If omitted, by default it will smartly load the right view based on whether the
    user has connections or not
    """
