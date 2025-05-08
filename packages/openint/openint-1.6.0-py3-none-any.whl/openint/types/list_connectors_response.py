# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["ListConnectorsResponse", "Integration", "Schemas", "Scope"]


class Integration(BaseModel):
    id: str

    connector_name: Literal[
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

    created_at: str

    external: Union[str, float, bool, Dict[str, object], List[object], None] = None

    name: str

    standard: Union[str, float, bool, Dict[str, object], List[object], None] = None

    updated_at: str

    auth_type: Optional[str] = None

    category: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop"]]] = None

    stage: Optional[Literal["alpha", "beta", "ga"]] = None

    version: Optional[str] = None


class Schemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class Scope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ListConnectorsResponse(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    integrations: Optional[List[Integration]] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[Schemas] = None

    scopes: Optional[List[Scope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None
