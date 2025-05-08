# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = [
    "ListConnectionConfigsResponse",
    "ConnectorAcmeOauth2DiscriminatedConnectorConfig",
    "ConnectorAcmeOauth2DiscriminatedConnectorConfigConfig",
    "ConnectorAcmeOauth2DiscriminatedConnectorConfigConfigOAuth",
    "ConnectorAcmeOauth2DiscriminatedConnectorConfigConnector",
    "ConnectorAcmeOauth2DiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorAcmeOauth2DiscriminatedConnectorConfigConnectorScope",
    "ConnectorAcmeOauth2DiscriminatedConnectorConfigIntegrations",
    "ConnectorAircallDiscriminatedConnectorConfig",
    "ConnectorAircallDiscriminatedConnectorConfigConfig",
    "ConnectorAircallDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorAircallDiscriminatedConnectorConfigConnector",
    "ConnectorAircallDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorAircallDiscriminatedConnectorConfigConnectorScope",
    "ConnectorAircallDiscriminatedConnectorConfigIntegrations",
    "ConnectorConfluenceDiscriminatedConnectorConfig",
    "ConnectorConfluenceDiscriminatedConnectorConfigConfig",
    "ConnectorConfluenceDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorConfluenceDiscriminatedConnectorConfigConnector",
    "ConnectorConfluenceDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorConfluenceDiscriminatedConnectorConfigConnectorScope",
    "ConnectorConfluenceDiscriminatedConnectorConfigIntegrations",
    "ConnectorDiscordDiscriminatedConnectorConfig",
    "ConnectorDiscordDiscriminatedConnectorConfigConfig",
    "ConnectorDiscordDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorDiscordDiscriminatedConnectorConfigConnector",
    "ConnectorDiscordDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorDiscordDiscriminatedConnectorConfigConnectorScope",
    "ConnectorDiscordDiscriminatedConnectorConfigIntegrations",
    "ConnectorFacebookDiscriminatedConnectorConfig",
    "ConnectorFacebookDiscriminatedConnectorConfigConfig",
    "ConnectorFacebookDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorFacebookDiscriminatedConnectorConfigConnector",
    "ConnectorFacebookDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorFacebookDiscriminatedConnectorConfigConnectorScope",
    "ConnectorFacebookDiscriminatedConnectorConfigIntegrations",
    "ConnectorGitHubDiscriminatedConnectorConfig",
    "ConnectorGitHubDiscriminatedConnectorConfigConfig",
    "ConnectorGitHubDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorGitHubDiscriminatedConnectorConfigConnector",
    "ConnectorGitHubDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorGitHubDiscriminatedConnectorConfigConnectorScope",
    "ConnectorGitHubDiscriminatedConnectorConfigIntegrations",
    "ConnectorGongDiscriminatedConnectorConfig",
    "ConnectorGongDiscriminatedConnectorConfigConfig",
    "ConnectorGongDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorGongDiscriminatedConnectorConfigConnector",
    "ConnectorGongDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorGongDiscriminatedConnectorConfigConnectorScope",
    "ConnectorGongDiscriminatedConnectorConfigIntegrations",
    "ConnectorGoogleCalendarDiscriminatedConnectorConfig",
    "ConnectorGoogleCalendarDiscriminatedConnectorConfigConfig",
    "ConnectorGoogleCalendarDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorGoogleCalendarDiscriminatedConnectorConfigConnector",
    "ConnectorGoogleCalendarDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorGoogleCalendarDiscriminatedConnectorConfigConnectorScope",
    "ConnectorGoogleCalendarDiscriminatedConnectorConfigIntegrations",
    "ConnectorGoogleDocsDiscriminatedConnectorConfig",
    "ConnectorGoogleDocsDiscriminatedConnectorConfigConfig",
    "ConnectorGoogleDocsDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorGoogleDocsDiscriminatedConnectorConfigConnector",
    "ConnectorGoogleDocsDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorGoogleDocsDiscriminatedConnectorConfigConnectorScope",
    "ConnectorGoogleDocsDiscriminatedConnectorConfigIntegrations",
    "ConnectorGoogleDriveDiscriminatedConnectorConfig",
    "ConnectorGoogleDriveDiscriminatedConnectorConfigConfig",
    "ConnectorGoogleDriveDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorGoogleDriveDiscriminatedConnectorConfigConnector",
    "ConnectorGoogleDriveDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorGoogleDriveDiscriminatedConnectorConfigConnectorScope",
    "ConnectorGoogleDriveDiscriminatedConnectorConfigIntegrations",
    "ConnectorGoogleMailDiscriminatedConnectorConfig",
    "ConnectorGoogleMailDiscriminatedConnectorConfigConfig",
    "ConnectorGoogleMailDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorGoogleMailDiscriminatedConnectorConfigConnector",
    "ConnectorGoogleMailDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorGoogleMailDiscriminatedConnectorConfigConnectorScope",
    "ConnectorGoogleMailDiscriminatedConnectorConfigIntegrations",
    "ConnectorGoogleSheetDiscriminatedConnectorConfig",
    "ConnectorGoogleSheetDiscriminatedConnectorConfigConfig",
    "ConnectorGoogleSheetDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorGoogleSheetDiscriminatedConnectorConfigConnector",
    "ConnectorGoogleSheetDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorGoogleSheetDiscriminatedConnectorConfigConnectorScope",
    "ConnectorGoogleSheetDiscriminatedConnectorConfigIntegrations",
    "ConnectorHubspotDiscriminatedConnectorConfig",
    "ConnectorHubspotDiscriminatedConnectorConfigConfig",
    "ConnectorHubspotDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorHubspotDiscriminatedConnectorConfigConnector",
    "ConnectorHubspotDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorHubspotDiscriminatedConnectorConfigConnectorScope",
    "ConnectorHubspotDiscriminatedConnectorConfigIntegrations",
    "ConnectorInstagramDiscriminatedConnectorConfig",
    "ConnectorInstagramDiscriminatedConnectorConfigConfig",
    "ConnectorInstagramDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorInstagramDiscriminatedConnectorConfigConnector",
    "ConnectorInstagramDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorInstagramDiscriminatedConnectorConfigConnectorScope",
    "ConnectorInstagramDiscriminatedConnectorConfigIntegrations",
    "ConnectorIntercomDiscriminatedConnectorConfig",
    "ConnectorIntercomDiscriminatedConnectorConfigConfig",
    "ConnectorIntercomDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorIntercomDiscriminatedConnectorConfigConnector",
    "ConnectorIntercomDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorIntercomDiscriminatedConnectorConfigConnectorScope",
    "ConnectorIntercomDiscriminatedConnectorConfigIntegrations",
    "ConnectorJiraDiscriminatedConnectorConfig",
    "ConnectorJiraDiscriminatedConnectorConfigConfig",
    "ConnectorJiraDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorJiraDiscriminatedConnectorConfigConnector",
    "ConnectorJiraDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorJiraDiscriminatedConnectorConfigConnectorScope",
    "ConnectorJiraDiscriminatedConnectorConfigIntegrations",
    "ConnectorLeverDiscriminatedConnectorConfig",
    "ConnectorLeverDiscriminatedConnectorConfigConfig",
    "ConnectorLeverDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorLeverDiscriminatedConnectorConfigConnector",
    "ConnectorLeverDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorLeverDiscriminatedConnectorConfigConnectorScope",
    "ConnectorLeverDiscriminatedConnectorConfigIntegrations",
    "ConnectorLinearDiscriminatedConnectorConfig",
    "ConnectorLinearDiscriminatedConnectorConfigConfig",
    "ConnectorLinearDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorLinearDiscriminatedConnectorConfigConnector",
    "ConnectorLinearDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorLinearDiscriminatedConnectorConfigConnectorScope",
    "ConnectorLinearDiscriminatedConnectorConfigIntegrations",
    "ConnectorLinkedinDiscriminatedConnectorConfig",
    "ConnectorLinkedinDiscriminatedConnectorConfigConfig",
    "ConnectorLinkedinDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorLinkedinDiscriminatedConnectorConfigConnector",
    "ConnectorLinkedinDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorLinkedinDiscriminatedConnectorConfigConnectorScope",
    "ConnectorLinkedinDiscriminatedConnectorConfigIntegrations",
    "ConnectorNotionDiscriminatedConnectorConfig",
    "ConnectorNotionDiscriminatedConnectorConfigConfig",
    "ConnectorNotionDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorNotionDiscriminatedConnectorConfigConnector",
    "ConnectorNotionDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorNotionDiscriminatedConnectorConfigConnectorScope",
    "ConnectorNotionDiscriminatedConnectorConfigIntegrations",
    "ConnectorOutreachDiscriminatedConnectorConfig",
    "ConnectorOutreachDiscriminatedConnectorConfigConfig",
    "ConnectorOutreachDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorOutreachDiscriminatedConnectorConfigConnector",
    "ConnectorOutreachDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorOutreachDiscriminatedConnectorConfigConnectorScope",
    "ConnectorOutreachDiscriminatedConnectorConfigIntegrations",
    "ConnectorPipedriveDiscriminatedConnectorConfig",
    "ConnectorPipedriveDiscriminatedConnectorConfigConfig",
    "ConnectorPipedriveDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorPipedriveDiscriminatedConnectorConfigConnector",
    "ConnectorPipedriveDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorPipedriveDiscriminatedConnectorConfigConnectorScope",
    "ConnectorPipedriveDiscriminatedConnectorConfigIntegrations",
    "ConnectorQuickbooksDiscriminatedConnectorConfig",
    "ConnectorQuickbooksDiscriminatedConnectorConfigConfig",
    "ConnectorQuickbooksDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorQuickbooksDiscriminatedConnectorConfigConnector",
    "ConnectorQuickbooksDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorQuickbooksDiscriminatedConnectorConfigConnectorScope",
    "ConnectorQuickbooksDiscriminatedConnectorConfigIntegrations",
    "ConnectorRedditDiscriminatedConnectorConfig",
    "ConnectorRedditDiscriminatedConnectorConfigConfig",
    "ConnectorRedditDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorRedditDiscriminatedConnectorConfigConnector",
    "ConnectorRedditDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorRedditDiscriminatedConnectorConfigConnectorScope",
    "ConnectorRedditDiscriminatedConnectorConfigIntegrations",
    "ConnectorSalesloftDiscriminatedConnectorConfig",
    "ConnectorSalesloftDiscriminatedConnectorConfigConfig",
    "ConnectorSalesloftDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorSalesloftDiscriminatedConnectorConfigConnector",
    "ConnectorSalesloftDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorSalesloftDiscriminatedConnectorConfigConnectorScope",
    "ConnectorSalesloftDiscriminatedConnectorConfigIntegrations",
    "ConnectorSharepointDiscriminatedConnectorConfig",
    "ConnectorSharepointDiscriminatedConnectorConfigConfig",
    "ConnectorSharepointDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorSharepointDiscriminatedConnectorConfigConnector",
    "ConnectorSharepointDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorSharepointDiscriminatedConnectorConfigConnectorScope",
    "ConnectorSharepointDiscriminatedConnectorConfigIntegrations",
    "ConnectorSlackDiscriminatedConnectorConfig",
    "ConnectorSlackDiscriminatedConnectorConfigConfig",
    "ConnectorSlackDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorSlackDiscriminatedConnectorConfigConnector",
    "ConnectorSlackDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorSlackDiscriminatedConnectorConfigConnectorScope",
    "ConnectorSlackDiscriminatedConnectorConfigIntegrations",
    "ConnectorTwitterDiscriminatedConnectorConfig",
    "ConnectorTwitterDiscriminatedConnectorConfigConfig",
    "ConnectorTwitterDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorTwitterDiscriminatedConnectorConfigConnector",
    "ConnectorTwitterDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorTwitterDiscriminatedConnectorConfigConnectorScope",
    "ConnectorTwitterDiscriminatedConnectorConfigIntegrations",
    "ConnectorXeroDiscriminatedConnectorConfig",
    "ConnectorXeroDiscriminatedConnectorConfigConfig",
    "ConnectorXeroDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorXeroDiscriminatedConnectorConfigConnector",
    "ConnectorXeroDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorXeroDiscriminatedConnectorConfigConnectorScope",
    "ConnectorXeroDiscriminatedConnectorConfigIntegrations",
    "ConnectorZohoDeskDiscriminatedConnectorConfig",
    "ConnectorZohoDeskDiscriminatedConnectorConfigConfig",
    "ConnectorZohoDeskDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorZohoDeskDiscriminatedConnectorConfigConnector",
    "ConnectorZohoDeskDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorZohoDeskDiscriminatedConnectorConfigConnectorScope",
    "ConnectorZohoDeskDiscriminatedConnectorConfigIntegrations",
    "ConnectorAirtableDiscriminatedConnectorConfig",
    "ConnectorAirtableDiscriminatedConnectorConfigConnector",
    "ConnectorAirtableDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorAirtableDiscriminatedConnectorConfigConnectorScope",
    "ConnectorAirtableDiscriminatedConnectorConfigIntegrations",
    "ConnectorApolloDiscriminatedConnectorConfig",
    "ConnectorApolloDiscriminatedConnectorConfigConnector",
    "ConnectorApolloDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorApolloDiscriminatedConnectorConfigConnectorScope",
    "ConnectorApolloDiscriminatedConnectorConfigIntegrations",
    "ConnectorBrexDiscriminatedConnectorConfig",
    "ConnectorBrexDiscriminatedConnectorConfigConfig",
    "ConnectorBrexDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorBrexDiscriminatedConnectorConfigConnector",
    "ConnectorBrexDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorBrexDiscriminatedConnectorConfigConnectorScope",
    "ConnectorBrexDiscriminatedConnectorConfigIntegrations",
    "ConnectorCodaDiscriminatedConnectorConfig",
    "ConnectorCodaDiscriminatedConnectorConfigConnector",
    "ConnectorCodaDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorCodaDiscriminatedConnectorConfigConnectorScope",
    "ConnectorCodaDiscriminatedConnectorConfigIntegrations",
    "ConnectorFinchDiscriminatedConnectorConfig",
    "ConnectorFinchDiscriminatedConnectorConfigConfig",
    "ConnectorFinchDiscriminatedConnectorConfigConnector",
    "ConnectorFinchDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorFinchDiscriminatedConnectorConfigConnectorScope",
    "ConnectorFinchDiscriminatedConnectorConfigIntegrations",
    "ConnectorFirebaseDiscriminatedConnectorConfig",
    "ConnectorFirebaseDiscriminatedConnectorConfigConnector",
    "ConnectorFirebaseDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorFirebaseDiscriminatedConnectorConfigConnectorScope",
    "ConnectorFirebaseDiscriminatedConnectorConfigIntegrations",
    "ConnectorForeceiptDiscriminatedConnectorConfig",
    "ConnectorForeceiptDiscriminatedConnectorConfigConnector",
    "ConnectorForeceiptDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorForeceiptDiscriminatedConnectorConfigConnectorScope",
    "ConnectorForeceiptDiscriminatedConnectorConfigIntegrations",
    "ConnectorGreenhouseDiscriminatedConnectorConfig",
    "ConnectorGreenhouseDiscriminatedConnectorConfigConnector",
    "ConnectorGreenhouseDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorGreenhouseDiscriminatedConnectorConfigConnectorScope",
    "ConnectorGreenhouseDiscriminatedConnectorConfigIntegrations",
    "ConnectorHeronDiscriminatedConnectorConfig",
    "ConnectorHeronDiscriminatedConnectorConfigConfig",
    "ConnectorHeronDiscriminatedConnectorConfigConnector",
    "ConnectorHeronDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorHeronDiscriminatedConnectorConfigConnectorScope",
    "ConnectorHeronDiscriminatedConnectorConfigIntegrations",
    "ConnectorLunchmoneyDiscriminatedConnectorConfig",
    "ConnectorLunchmoneyDiscriminatedConnectorConfigConfig",
    "ConnectorLunchmoneyDiscriminatedConnectorConfigConnector",
    "ConnectorLunchmoneyDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorLunchmoneyDiscriminatedConnectorConfigConnectorScope",
    "ConnectorLunchmoneyDiscriminatedConnectorConfigIntegrations",
    "ConnectorMercuryDiscriminatedConnectorConfig",
    "ConnectorMercuryDiscriminatedConnectorConfigConfig",
    "ConnectorMercuryDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorMercuryDiscriminatedConnectorConfigConnector",
    "ConnectorMercuryDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorMercuryDiscriminatedConnectorConfigConnectorScope",
    "ConnectorMercuryDiscriminatedConnectorConfigIntegrations",
    "ConnectorMergeDiscriminatedConnectorConfig",
    "ConnectorMergeDiscriminatedConnectorConfigConfig",
    "ConnectorMergeDiscriminatedConnectorConfigConnector",
    "ConnectorMergeDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorMergeDiscriminatedConnectorConfigConnectorScope",
    "ConnectorMergeDiscriminatedConnectorConfigIntegrations",
    "ConnectorMootaDiscriminatedConnectorConfig",
    "ConnectorMootaDiscriminatedConnectorConfigConfig",
    "ConnectorMootaDiscriminatedConnectorConfigConnector",
    "ConnectorMootaDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorMootaDiscriminatedConnectorConfigConnectorScope",
    "ConnectorMootaDiscriminatedConnectorConfigIntegrations",
    "ConnectorOnebrickDiscriminatedConnectorConfig",
    "ConnectorOnebrickDiscriminatedConnectorConfigConfig",
    "ConnectorOnebrickDiscriminatedConnectorConfigConnector",
    "ConnectorOnebrickDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorOnebrickDiscriminatedConnectorConfigConnectorScope",
    "ConnectorOnebrickDiscriminatedConnectorConfigIntegrations",
    "ConnectorPlaidDiscriminatedConnectorConfig",
    "ConnectorPlaidDiscriminatedConnectorConfigConfig",
    "ConnectorPlaidDiscriminatedConnectorConfigConfigCredentials",
    "ConnectorPlaidDiscriminatedConnectorConfigConnector",
    "ConnectorPlaidDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorPlaidDiscriminatedConnectorConfigConnectorScope",
    "ConnectorPlaidDiscriminatedConnectorConfigIntegrations",
    "ConnectorPostgresDiscriminatedConnectorConfig",
    "ConnectorPostgresDiscriminatedConnectorConfigConnector",
    "ConnectorPostgresDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorPostgresDiscriminatedConnectorConfigConnectorScope",
    "ConnectorPostgresDiscriminatedConnectorConfigIntegrations",
    "ConnectorRampDiscriminatedConnectorConfig",
    "ConnectorRampDiscriminatedConnectorConfigConfig",
    "ConnectorRampDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorRampDiscriminatedConnectorConfigConnector",
    "ConnectorRampDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorRampDiscriminatedConnectorConfigConnectorScope",
    "ConnectorRampDiscriminatedConnectorConfigIntegrations",
    "ConnectorSaltedgeDiscriminatedConnectorConfig",
    "ConnectorSaltedgeDiscriminatedConnectorConfigConfig",
    "ConnectorSaltedgeDiscriminatedConnectorConfigConnector",
    "ConnectorSaltedgeDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorSaltedgeDiscriminatedConnectorConfigConnectorScope",
    "ConnectorSaltedgeDiscriminatedConnectorConfigIntegrations",
    "ConnectorSplitwiseDiscriminatedConnectorConfig",
    "ConnectorSplitwiseDiscriminatedConnectorConfigConnector",
    "ConnectorSplitwiseDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorSplitwiseDiscriminatedConnectorConfigConnectorScope",
    "ConnectorSplitwiseDiscriminatedConnectorConfigIntegrations",
    "ConnectorStripeDiscriminatedConnectorConfig",
    "ConnectorStripeDiscriminatedConnectorConfigConfig",
    "ConnectorStripeDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorStripeDiscriminatedConnectorConfigConnector",
    "ConnectorStripeDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorStripeDiscriminatedConnectorConfigConnectorScope",
    "ConnectorStripeDiscriminatedConnectorConfigIntegrations",
    "ConnectorTellerDiscriminatedConnectorConfig",
    "ConnectorTellerDiscriminatedConnectorConfigConfig",
    "ConnectorTellerDiscriminatedConnectorConfigConnector",
    "ConnectorTellerDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorTellerDiscriminatedConnectorConfigConnectorScope",
    "ConnectorTellerDiscriminatedConnectorConfigIntegrations",
    "ConnectorTogglDiscriminatedConnectorConfig",
    "ConnectorTogglDiscriminatedConnectorConfigConnector",
    "ConnectorTogglDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorTogglDiscriminatedConnectorConfigConnectorScope",
    "ConnectorTogglDiscriminatedConnectorConfigIntegrations",
    "ConnectorTwentyDiscriminatedConnectorConfig",
    "ConnectorTwentyDiscriminatedConnectorConfigConnector",
    "ConnectorTwentyDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorTwentyDiscriminatedConnectorConfigConnectorScope",
    "ConnectorTwentyDiscriminatedConnectorConfigIntegrations",
    "ConnectorVenmoDiscriminatedConnectorConfig",
    "ConnectorVenmoDiscriminatedConnectorConfigConfig",
    "ConnectorVenmoDiscriminatedConnectorConfigConfigProxy",
    "ConnectorVenmoDiscriminatedConnectorConfigConnector",
    "ConnectorVenmoDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorVenmoDiscriminatedConnectorConfigConnectorScope",
    "ConnectorVenmoDiscriminatedConnectorConfigIntegrations",
    "ConnectorWiseDiscriminatedConnectorConfig",
    "ConnectorWiseDiscriminatedConnectorConfigConnector",
    "ConnectorWiseDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorWiseDiscriminatedConnectorConfigConnectorScope",
    "ConnectorWiseDiscriminatedConnectorConfigIntegrations",
    "ConnectorYodleeDiscriminatedConnectorConfig",
    "ConnectorYodleeDiscriminatedConnectorConfigConfig",
    "ConnectorYodleeDiscriminatedConnectorConfigConfigProxy",
    "ConnectorYodleeDiscriminatedConnectorConfigConnector",
    "ConnectorYodleeDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorYodleeDiscriminatedConnectorConfigConnectorScope",
    "ConnectorYodleeDiscriminatedConnectorConfigIntegrations",
]


class ConnectorAcmeOauth2DiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: Optional[str] = None

    client_secret: Optional[str] = None

    redirect_uri: Optional[str] = None
    """Custom redirect URI"""

    scopes: Optional[List[str]] = None


class ConnectorAcmeOauth2DiscriminatedConnectorConfigConfig(BaseModel):
    oauth: Optional[ConnectorAcmeOauth2DiscriminatedConnectorConfigConfigOAuth] = None
    """Base oauth configuration for the connector"""


class ConnectorAcmeOauth2DiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorAcmeOauth2DiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorAcmeOauth2DiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorAcmeOauth2DiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorAcmeOauth2DiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorAcmeOauth2DiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorAcmeOauth2DiscriminatedConnectorConfig(BaseModel):
    config: ConnectorAcmeOauth2DiscriminatedConnectorConfigConfig

    connector_name: Literal["acme-oauth2"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorAcmeOauth2DiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorAcmeOauth2DiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorAircallDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: Optional[str] = None

    client_secret: Optional[str] = None

    redirect_uri: Optional[str] = None
    """Custom redirect URI"""

    scopes: Optional[List[str]] = None


class ConnectorAircallDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: Optional[ConnectorAircallDiscriminatedConnectorConfigConfigOAuth] = None
    """Base oauth configuration for the connector"""


class ConnectorAircallDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorAircallDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorAircallDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorAircallDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorAircallDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorAircallDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorAircallDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorAircallDiscriminatedConnectorConfigConfig

    connector_name: Literal["aircall"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorAircallDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorAircallDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorConfluenceDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: Optional[str] = None

    client_secret: Optional[str] = None

    redirect_uri: Optional[str] = None
    """Custom redirect URI"""

    scopes: Optional[List[str]] = None


class ConnectorConfluenceDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: Optional[ConnectorConfluenceDiscriminatedConnectorConfigConfigOAuth] = None
    """Base oauth configuration for the connector"""


class ConnectorConfluenceDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorConfluenceDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorConfluenceDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorConfluenceDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorConfluenceDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorConfluenceDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorConfluenceDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorConfluenceDiscriminatedConnectorConfigConfig

    connector_name: Literal["confluence"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorConfluenceDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorConfluenceDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorDiscordDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: Optional[str] = None

    client_secret: Optional[str] = None

    redirect_uri: Optional[str] = None
    """Custom redirect URI"""

    scopes: Optional[List[str]] = None


class ConnectorDiscordDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: Optional[ConnectorDiscordDiscriminatedConnectorConfigConfigOAuth] = None
    """Base oauth configuration for the connector"""


class ConnectorDiscordDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorDiscordDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorDiscordDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorDiscordDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorDiscordDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorDiscordDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorDiscordDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorDiscordDiscriminatedConnectorConfigConfig

    connector_name: Literal["discord"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorDiscordDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorDiscordDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorFacebookDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: Optional[str] = None

    client_secret: Optional[str] = None

    redirect_uri: Optional[str] = None
    """Custom redirect URI"""

    scopes: Optional[List[str]] = None


class ConnectorFacebookDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: Optional[ConnectorFacebookDiscriminatedConnectorConfigConfigOAuth] = None
    """Base oauth configuration for the connector"""


class ConnectorFacebookDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorFacebookDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorFacebookDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorFacebookDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorFacebookDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorFacebookDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorFacebookDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorFacebookDiscriminatedConnectorConfigConfig

    connector_name: Literal["facebook"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorFacebookDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorFacebookDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorGitHubDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: Optional[str] = None

    client_secret: Optional[str] = None

    redirect_uri: Optional[str] = None
    """Custom redirect URI"""

    scopes: Optional[List[str]] = None


class ConnectorGitHubDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: Optional[ConnectorGitHubDiscriminatedConnectorConfigConfigOAuth] = None
    """Base oauth configuration for the connector"""


class ConnectorGitHubDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorGitHubDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorGitHubDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorGitHubDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorGitHubDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorGitHubDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorGitHubDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorGitHubDiscriminatedConnectorConfigConfig

    connector_name: Literal["github"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorGitHubDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorGitHubDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorGongDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: Optional[str] = None

    client_secret: Optional[str] = None

    redirect_uri: Optional[str] = None
    """Custom redirect URI"""

    scopes: Optional[List[str]] = None


class ConnectorGongDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: Optional[ConnectorGongDiscriminatedConnectorConfigConfigOAuth] = None
    """Base oauth configuration for the connector"""


class ConnectorGongDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorGongDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorGongDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorGongDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorGongDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorGongDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorGongDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorGongDiscriminatedConnectorConfigConfig

    connector_name: Literal["gong"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorGongDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorGongDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorGoogleCalendarDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: Optional[str] = None

    client_secret: Optional[str] = None

    redirect_uri: Optional[str] = None
    """Custom redirect URI"""

    scopes: Optional[List[str]] = None


class ConnectorGoogleCalendarDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: Optional[ConnectorGoogleCalendarDiscriminatedConnectorConfigConfigOAuth] = None
    """Base oauth configuration for the connector"""


class ConnectorGoogleCalendarDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorGoogleCalendarDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorGoogleCalendarDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorGoogleCalendarDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorGoogleCalendarDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorGoogleCalendarDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorGoogleCalendarDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorGoogleCalendarDiscriminatedConnectorConfigConfig

    connector_name: Literal["google-calendar"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorGoogleCalendarDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorGoogleCalendarDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorGoogleDocsDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: Optional[str] = None

    client_secret: Optional[str] = None

    redirect_uri: Optional[str] = None
    """Custom redirect URI"""

    scopes: Optional[List[str]] = None


class ConnectorGoogleDocsDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: Optional[ConnectorGoogleDocsDiscriminatedConnectorConfigConfigOAuth] = None
    """Base oauth configuration for the connector"""


class ConnectorGoogleDocsDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorGoogleDocsDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorGoogleDocsDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorGoogleDocsDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorGoogleDocsDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorGoogleDocsDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorGoogleDocsDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorGoogleDocsDiscriminatedConnectorConfigConfig

    connector_name: Literal["google-docs"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorGoogleDocsDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorGoogleDocsDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorGoogleDriveDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: Optional[str] = None

    client_secret: Optional[str] = None

    redirect_uri: Optional[str] = None
    """Custom redirect URI"""

    scopes: Optional[List[str]] = None


class ConnectorGoogleDriveDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: Optional[ConnectorGoogleDriveDiscriminatedConnectorConfigConfigOAuth] = None
    """Base oauth configuration for the connector"""


class ConnectorGoogleDriveDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorGoogleDriveDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorGoogleDriveDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorGoogleDriveDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorGoogleDriveDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorGoogleDriveDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorGoogleDriveDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorGoogleDriveDiscriminatedConnectorConfigConfig

    connector_name: Literal["google-drive"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorGoogleDriveDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorGoogleDriveDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorGoogleMailDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: Optional[str] = None

    client_secret: Optional[str] = None

    redirect_uri: Optional[str] = None
    """Custom redirect URI"""

    scopes: Optional[List[str]] = None


class ConnectorGoogleMailDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: Optional[ConnectorGoogleMailDiscriminatedConnectorConfigConfigOAuth] = None
    """Base oauth configuration for the connector"""


class ConnectorGoogleMailDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorGoogleMailDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorGoogleMailDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorGoogleMailDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorGoogleMailDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorGoogleMailDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorGoogleMailDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorGoogleMailDiscriminatedConnectorConfigConfig

    connector_name: Literal["google-mail"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorGoogleMailDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorGoogleMailDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorGoogleSheetDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: Optional[str] = None

    client_secret: Optional[str] = None

    redirect_uri: Optional[str] = None
    """Custom redirect URI"""

    scopes: Optional[List[str]] = None


class ConnectorGoogleSheetDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: Optional[ConnectorGoogleSheetDiscriminatedConnectorConfigConfigOAuth] = None
    """Base oauth configuration for the connector"""


class ConnectorGoogleSheetDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorGoogleSheetDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorGoogleSheetDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorGoogleSheetDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorGoogleSheetDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorGoogleSheetDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorGoogleSheetDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorGoogleSheetDiscriminatedConnectorConfigConfig

    connector_name: Literal["google-sheet"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorGoogleSheetDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorGoogleSheetDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorHubspotDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: Optional[str] = None

    client_secret: Optional[str] = None

    redirect_uri: Optional[str] = None
    """Custom redirect URI"""

    scopes: Optional[List[str]] = None


class ConnectorHubspotDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: Optional[ConnectorHubspotDiscriminatedConnectorConfigConfigOAuth] = None
    """Base oauth configuration for the connector"""


class ConnectorHubspotDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorHubspotDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorHubspotDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorHubspotDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorHubspotDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorHubspotDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorHubspotDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorHubspotDiscriminatedConnectorConfigConfig

    connector_name: Literal["hubspot"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorHubspotDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorHubspotDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorInstagramDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: Optional[str] = None

    client_secret: Optional[str] = None

    redirect_uri: Optional[str] = None
    """Custom redirect URI"""

    scopes: Optional[List[str]] = None


class ConnectorInstagramDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: Optional[ConnectorInstagramDiscriminatedConnectorConfigConfigOAuth] = None
    """Base oauth configuration for the connector"""


class ConnectorInstagramDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorInstagramDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorInstagramDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorInstagramDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorInstagramDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorInstagramDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorInstagramDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorInstagramDiscriminatedConnectorConfigConfig

    connector_name: Literal["instagram"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorInstagramDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorInstagramDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorIntercomDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: Optional[str] = None

    client_secret: Optional[str] = None

    redirect_uri: Optional[str] = None
    """Custom redirect URI"""

    scopes: Optional[List[str]] = None


class ConnectorIntercomDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: Optional[ConnectorIntercomDiscriminatedConnectorConfigConfigOAuth] = None
    """Base oauth configuration for the connector"""


class ConnectorIntercomDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorIntercomDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorIntercomDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorIntercomDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorIntercomDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorIntercomDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorIntercomDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorIntercomDiscriminatedConnectorConfigConfig

    connector_name: Literal["intercom"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorIntercomDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorIntercomDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorJiraDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: Optional[str] = None

    client_secret: Optional[str] = None

    redirect_uri: Optional[str] = None
    """Custom redirect URI"""

    scopes: Optional[List[str]] = None


class ConnectorJiraDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: Optional[ConnectorJiraDiscriminatedConnectorConfigConfigOAuth] = None
    """Base oauth configuration for the connector"""


class ConnectorJiraDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorJiraDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorJiraDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorJiraDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorJiraDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorJiraDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorJiraDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorJiraDiscriminatedConnectorConfigConfig

    connector_name: Literal["jira"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorJiraDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorJiraDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorLeverDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: Optional[str] = None

    client_secret: Optional[str] = None

    redirect_uri: Optional[str] = None
    """Custom redirect URI"""

    scopes: Optional[List[str]] = None


class ConnectorLeverDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: Optional[ConnectorLeverDiscriminatedConnectorConfigConfigOAuth] = None
    """Base oauth configuration for the connector"""


class ConnectorLeverDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorLeverDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorLeverDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorLeverDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorLeverDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorLeverDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorLeverDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorLeverDiscriminatedConnectorConfigConfig

    connector_name: Literal["lever"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorLeverDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorLeverDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorLinearDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: Optional[str] = None

    client_secret: Optional[str] = None

    redirect_uri: Optional[str] = None
    """Custom redirect URI"""

    scopes: Optional[List[str]] = None


class ConnectorLinearDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: Optional[ConnectorLinearDiscriminatedConnectorConfigConfigOAuth] = None
    """Base oauth configuration for the connector"""


class ConnectorLinearDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorLinearDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorLinearDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorLinearDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorLinearDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorLinearDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorLinearDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorLinearDiscriminatedConnectorConfigConfig

    connector_name: Literal["linear"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorLinearDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorLinearDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorLinkedinDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: Optional[str] = None

    client_secret: Optional[str] = None

    redirect_uri: Optional[str] = None
    """Custom redirect URI"""

    scopes: Optional[List[str]] = None


class ConnectorLinkedinDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: Optional[ConnectorLinkedinDiscriminatedConnectorConfigConfigOAuth] = None
    """Base oauth configuration for the connector"""


class ConnectorLinkedinDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorLinkedinDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorLinkedinDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorLinkedinDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorLinkedinDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorLinkedinDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorLinkedinDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorLinkedinDiscriminatedConnectorConfigConfig

    connector_name: Literal["linkedin"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorLinkedinDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorLinkedinDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorNotionDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: Optional[str] = None

    client_secret: Optional[str] = None

    redirect_uri: Optional[str] = None
    """Custom redirect URI"""

    scopes: Optional[List[str]] = None


class ConnectorNotionDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: Optional[ConnectorNotionDiscriminatedConnectorConfigConfigOAuth] = None
    """Base oauth configuration for the connector"""


class ConnectorNotionDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorNotionDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorNotionDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorNotionDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorNotionDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorNotionDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorNotionDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorNotionDiscriminatedConnectorConfigConfig

    connector_name: Literal["notion"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorNotionDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorNotionDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorOutreachDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: Optional[str] = None

    client_secret: Optional[str] = None

    redirect_uri: Optional[str] = None
    """Custom redirect URI"""

    scopes: Optional[List[str]] = None


class ConnectorOutreachDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: Optional[ConnectorOutreachDiscriminatedConnectorConfigConfigOAuth] = None
    """Base oauth configuration for the connector"""


class ConnectorOutreachDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorOutreachDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorOutreachDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorOutreachDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorOutreachDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorOutreachDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorOutreachDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorOutreachDiscriminatedConnectorConfigConfig

    connector_name: Literal["outreach"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorOutreachDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorOutreachDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorPipedriveDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: Optional[str] = None

    client_secret: Optional[str] = None

    redirect_uri: Optional[str] = None
    """Custom redirect URI"""

    scopes: Optional[List[str]] = None


class ConnectorPipedriveDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: Optional[ConnectorPipedriveDiscriminatedConnectorConfigConfigOAuth] = None
    """Base oauth configuration for the connector"""


class ConnectorPipedriveDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorPipedriveDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorPipedriveDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorPipedriveDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorPipedriveDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorPipedriveDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorPipedriveDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorPipedriveDiscriminatedConnectorConfigConfig

    connector_name: Literal["pipedrive"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorPipedriveDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorPipedriveDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorQuickbooksDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: Optional[str] = None

    client_secret: Optional[str] = None

    redirect_uri: Optional[str] = None
    """Custom redirect URI"""

    scopes: Optional[List[str]] = None


class ConnectorQuickbooksDiscriminatedConnectorConfigConfig(BaseModel):
    env_name: Literal["sandbox", "production"] = FieldInfo(alias="envName")

    oauth: Optional[ConnectorQuickbooksDiscriminatedConnectorConfigConfigOAuth] = None
    """Base oauth configuration for the connector"""


class ConnectorQuickbooksDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorQuickbooksDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorQuickbooksDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorQuickbooksDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorQuickbooksDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorQuickbooksDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorQuickbooksDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorQuickbooksDiscriminatedConnectorConfigConfig

    connector_name: Literal["quickbooks"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorQuickbooksDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorQuickbooksDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorRedditDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: Optional[str] = None

    client_secret: Optional[str] = None

    redirect_uri: Optional[str] = None
    """Custom redirect URI"""

    scopes: Optional[List[str]] = None


class ConnectorRedditDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: Optional[ConnectorRedditDiscriminatedConnectorConfigConfigOAuth] = None
    """Base oauth configuration for the connector"""


class ConnectorRedditDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorRedditDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorRedditDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorRedditDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorRedditDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorRedditDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorRedditDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorRedditDiscriminatedConnectorConfigConfig

    connector_name: Literal["reddit"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorRedditDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorRedditDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorSalesloftDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: Optional[str] = None

    client_secret: Optional[str] = None

    redirect_uri: Optional[str] = None
    """Custom redirect URI"""

    scopes: Optional[List[str]] = None


class ConnectorSalesloftDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: Optional[ConnectorSalesloftDiscriminatedConnectorConfigConfigOAuth] = None
    """Base oauth configuration for the connector"""


class ConnectorSalesloftDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorSalesloftDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorSalesloftDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorSalesloftDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorSalesloftDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorSalesloftDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorSalesloftDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorSalesloftDiscriminatedConnectorConfigConfig

    connector_name: Literal["salesloft"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorSalesloftDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorSalesloftDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorSharepointDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: Optional[str] = None

    client_secret: Optional[str] = None

    redirect_uri: Optional[str] = None
    """Custom redirect URI"""

    scopes: Optional[List[str]] = None


class ConnectorSharepointDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: Optional[ConnectorSharepointDiscriminatedConnectorConfigConfigOAuth] = None
    """Base oauth configuration for the connector"""


class ConnectorSharepointDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorSharepointDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorSharepointDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorSharepointDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorSharepointDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorSharepointDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorSharepointDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorSharepointDiscriminatedConnectorConfigConfig

    connector_name: Literal["sharepoint"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorSharepointDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorSharepointDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorSlackDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: Optional[str] = None

    client_secret: Optional[str] = None

    redirect_uri: Optional[str] = None
    """Custom redirect URI"""

    scopes: Optional[List[str]] = None


class ConnectorSlackDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: Optional[ConnectorSlackDiscriminatedConnectorConfigConfigOAuth] = None
    """Base oauth configuration for the connector"""


class ConnectorSlackDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorSlackDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorSlackDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorSlackDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorSlackDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorSlackDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorSlackDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorSlackDiscriminatedConnectorConfigConfig

    connector_name: Literal["slack"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorSlackDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorSlackDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorTwitterDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: Optional[str] = None

    client_secret: Optional[str] = None

    redirect_uri: Optional[str] = None
    """Custom redirect URI"""

    scopes: Optional[List[str]] = None


class ConnectorTwitterDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: Optional[ConnectorTwitterDiscriminatedConnectorConfigConfigOAuth] = None
    """Base oauth configuration for the connector"""


class ConnectorTwitterDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorTwitterDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorTwitterDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorTwitterDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorTwitterDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorTwitterDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorTwitterDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorTwitterDiscriminatedConnectorConfigConfig

    connector_name: Literal["twitter"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorTwitterDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorTwitterDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorXeroDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: Optional[str] = None

    client_secret: Optional[str] = None

    redirect_uri: Optional[str] = None
    """Custom redirect URI"""

    scopes: Optional[List[str]] = None


class ConnectorXeroDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: Optional[ConnectorXeroDiscriminatedConnectorConfigConfigOAuth] = None
    """Base oauth configuration for the connector"""


class ConnectorXeroDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorXeroDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorXeroDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorXeroDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorXeroDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorXeroDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorXeroDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorXeroDiscriminatedConnectorConfigConfig

    connector_name: Literal["xero"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorXeroDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorXeroDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorZohoDeskDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: Optional[str] = None

    client_secret: Optional[str] = None

    redirect_uri: Optional[str] = None
    """Custom redirect URI"""

    scopes: Optional[List[str]] = None


class ConnectorZohoDeskDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: Optional[ConnectorZohoDeskDiscriminatedConnectorConfigConfigOAuth] = None
    """Base oauth configuration for the connector"""


class ConnectorZohoDeskDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorZohoDeskDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorZohoDeskDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorZohoDeskDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorZohoDeskDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorZohoDeskDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorZohoDeskDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorZohoDeskDiscriminatedConnectorConfigConfig

    connector_name: Literal["zoho-desk"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorZohoDeskDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorZohoDeskDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorAirtableDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorAirtableDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorAirtableDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorAirtableDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorAirtableDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorAirtableDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorAirtableDiscriminatedConnectorConfig(BaseModel):
    config: object

    connector_name: Literal["airtable"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorAirtableDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorAirtableDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorApolloDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorApolloDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorApolloDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorApolloDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorApolloDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorApolloDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorApolloDiscriminatedConnectorConfig(BaseModel):
    config: object

    connector_name: Literal["apollo"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorApolloDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorApolloDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorBrexDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: str = FieldInfo(alias="clientId")

    client_secret: str = FieldInfo(alias="clientSecret")


class ConnectorBrexDiscriminatedConnectorConfigConfig(BaseModel):
    apikey_auth: Optional[bool] = FieldInfo(alias="apikeyAuth", default=None)
    """API key auth support"""

    oauth: Optional[ConnectorBrexDiscriminatedConnectorConfigConfigOAuth] = None
    """Configure oauth"""


class ConnectorBrexDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorBrexDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorBrexDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorBrexDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorBrexDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorBrexDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorBrexDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorBrexDiscriminatedConnectorConfigConfig

    connector_name: Literal["brex"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorBrexDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorBrexDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorCodaDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorCodaDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorCodaDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorCodaDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorCodaDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorCodaDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorCodaDiscriminatedConnectorConfig(BaseModel):
    config: object

    connector_name: Literal["coda"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorCodaDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorCodaDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorFinchDiscriminatedConnectorConfigConfig(BaseModel):
    client_id: str

    client_secret: str

    products: List[
        Literal["company", "directory", "individual", "ssn", "employment", "payment", "pay_statement", "benefits"]
    ]
    """
    Finch products to access, @see
    https://developer.tryfinch.com/api-reference/development-guides/Permissions
    """

    api_version: Optional[str] = None
    """Finch API version"""


class ConnectorFinchDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorFinchDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorFinchDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorFinchDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorFinchDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorFinchDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorFinchDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorFinchDiscriminatedConnectorConfigConfig

    connector_name: Literal["finch"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorFinchDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorFinchDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorFirebaseDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorFirebaseDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorFirebaseDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorFirebaseDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorFirebaseDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorFirebaseDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorFirebaseDiscriminatedConnectorConfig(BaseModel):
    config: object

    connector_name: Literal["firebase"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorFirebaseDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorFirebaseDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorForeceiptDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorForeceiptDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorForeceiptDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorForeceiptDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorForeceiptDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorForeceiptDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorForeceiptDiscriminatedConnectorConfig(BaseModel):
    config: object

    connector_name: Literal["foreceipt"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorForeceiptDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorForeceiptDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorGreenhouseDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorGreenhouseDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorGreenhouseDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorGreenhouseDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorGreenhouseDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorGreenhouseDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorGreenhouseDiscriminatedConnectorConfig(BaseModel):
    config: object

    connector_name: Literal["greenhouse"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorGreenhouseDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorGreenhouseDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorHeronDiscriminatedConnectorConfigConfig(BaseModel):
    api_key: str = FieldInfo(alias="apiKey")


class ConnectorHeronDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorHeronDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorHeronDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorHeronDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorHeronDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorHeronDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorHeronDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorHeronDiscriminatedConnectorConfigConfig

    connector_name: Literal["heron"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorHeronDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorHeronDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorLunchmoneyDiscriminatedConnectorConfigConfig(BaseModel):
    access_token: str = FieldInfo(alias="accessToken")


class ConnectorLunchmoneyDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorLunchmoneyDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorLunchmoneyDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorLunchmoneyDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorLunchmoneyDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorLunchmoneyDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorLunchmoneyDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorLunchmoneyDiscriminatedConnectorConfigConfig

    connector_name: Literal["lunchmoney"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorLunchmoneyDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorLunchmoneyDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorMercuryDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: str = FieldInfo(alias="clientId")

    client_secret: str = FieldInfo(alias="clientSecret")


class ConnectorMercuryDiscriminatedConnectorConfigConfig(BaseModel):
    apikey_auth: Optional[bool] = FieldInfo(alias="apikeyAuth", default=None)
    """API key auth support"""

    oauth: Optional[ConnectorMercuryDiscriminatedConnectorConfigConfigOAuth] = None
    """Configure oauth"""


class ConnectorMercuryDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorMercuryDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorMercuryDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorMercuryDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorMercuryDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorMercuryDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorMercuryDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorMercuryDiscriminatedConnectorConfigConfig

    connector_name: Literal["mercury"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorMercuryDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorMercuryDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorMergeDiscriminatedConnectorConfigConfig(BaseModel):
    api_key: str = FieldInfo(alias="apiKey")


class ConnectorMergeDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorMergeDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorMergeDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorMergeDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorMergeDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorMergeDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorMergeDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorMergeDiscriminatedConnectorConfigConfig

    connector_name: Literal["merge"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorMergeDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorMergeDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorMootaDiscriminatedConnectorConfigConfig(BaseModel):
    token: str


class ConnectorMootaDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorMootaDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorMootaDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorMootaDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorMootaDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorMootaDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorMootaDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorMootaDiscriminatedConnectorConfigConfig

    connector_name: Literal["moota"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorMootaDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorMootaDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorOnebrickDiscriminatedConnectorConfigConfig(BaseModel):
    client_id: str = FieldInfo(alias="clientId")

    client_secret: str = FieldInfo(alias="clientSecret")

    env_name: Literal["sandbox", "production"] = FieldInfo(alias="envName")

    public_token: str = FieldInfo(alias="publicToken")

    access_token: Optional[str] = FieldInfo(alias="accessToken", default=None)

    redirect_url: Optional[str] = FieldInfo(alias="redirectUrl", default=None)


class ConnectorOnebrickDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorOnebrickDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorOnebrickDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorOnebrickDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorOnebrickDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorOnebrickDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorOnebrickDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorOnebrickDiscriminatedConnectorConfigConfig

    connector_name: Literal["onebrick"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorOnebrickDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorOnebrickDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorPlaidDiscriminatedConnectorConfigConfigCredentials(BaseModel):
    client_id: str = FieldInfo(alias="clientId")

    client_secret: str = FieldInfo(alias="clientSecret")


class ConnectorPlaidDiscriminatedConnectorConfigConfig(BaseModel):
    client_name: str = FieldInfo(alias="clientName")
    """
    The name of your application, as it should be displayed in Link. Maximum length
    of 30 characters. If a value longer than 30 characters is provided, Link will
    display "This Application" instead.
    """

    country_codes: List[
        Literal["US", "GB", "ES", "NL", "FR", "IE", "CA", "DE", "IT", "PL", "DK", "NO", "SE", "EE", "LT", "LV"]
    ] = FieldInfo(alias="countryCodes")

    env_name: Literal["sandbox", "development", "production"] = FieldInfo(alias="envName")

    language: Literal["en", "fr", "es", "nl", "de"]

    products: List[
        Literal[
            "assets",
            "auth",
            "balance",
            "identity",
            "investments",
            "liabilities",
            "payment_initiation",
            "identity_verification",
            "transactions",
            "credit_details",
            "income",
            "income_verification",
            "deposit_switch",
            "standing_orders",
            "transfer",
            "employment",
            "recurring_transactions",
        ]
    ]

    credentials: Optional[ConnectorPlaidDiscriminatedConnectorConfigConfigCredentials] = None


class ConnectorPlaidDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorPlaidDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorPlaidDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorPlaidDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorPlaidDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorPlaidDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorPlaidDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorPlaidDiscriminatedConnectorConfigConfig

    connector_name: Literal["plaid"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorPlaidDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorPlaidDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorPostgresDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorPostgresDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorPostgresDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorPostgresDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorPostgresDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorPostgresDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorPostgresDiscriminatedConnectorConfig(BaseModel):
    config: object

    connector_name: Literal["postgres"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorPostgresDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorPostgresDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorRampDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: str = FieldInfo(alias="clientId")

    client_secret: str = FieldInfo(alias="clientSecret")


class ConnectorRampDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: ConnectorRampDiscriminatedConnectorConfigConfigOAuth


class ConnectorRampDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorRampDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorRampDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorRampDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorRampDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorRampDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorRampDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorRampDiscriminatedConnectorConfigConfig

    connector_name: Literal["ramp"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorRampDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorRampDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorSaltedgeDiscriminatedConnectorConfigConfig(BaseModel):
    app_id: str = FieldInfo(alias="appId")

    secret: str

    url: Optional[str] = None


class ConnectorSaltedgeDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorSaltedgeDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorSaltedgeDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorSaltedgeDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorSaltedgeDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorSaltedgeDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorSaltedgeDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorSaltedgeDiscriminatedConnectorConfigConfig

    connector_name: Literal["saltedge"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorSaltedgeDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorSaltedgeDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorSplitwiseDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorSplitwiseDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorSplitwiseDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorSplitwiseDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorSplitwiseDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorSplitwiseDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorSplitwiseDiscriminatedConnectorConfig(BaseModel):
    config: object

    connector_name: Literal["splitwise"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorSplitwiseDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorSplitwiseDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorStripeDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: str = FieldInfo(alias="clientId")

    client_secret: str = FieldInfo(alias="clientSecret")


class ConnectorStripeDiscriminatedConnectorConfigConfig(BaseModel):
    apikey_auth: Optional[bool] = FieldInfo(alias="apikeyAuth", default=None)
    """API key auth support"""

    oauth: Optional[ConnectorStripeDiscriminatedConnectorConfigConfigOAuth] = None
    """Configure oauth"""


class ConnectorStripeDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorStripeDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorStripeDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorStripeDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorStripeDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorStripeDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorStripeDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorStripeDiscriminatedConnectorConfigConfig

    connector_name: Literal["stripe"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorStripeDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorStripeDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorTellerDiscriminatedConnectorConfigConfig(BaseModel):
    application_id: str = FieldInfo(alias="applicationId")

    token: Optional[str] = None


class ConnectorTellerDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorTellerDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorTellerDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorTellerDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorTellerDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorTellerDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorTellerDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorTellerDiscriminatedConnectorConfigConfig

    connector_name: Literal["teller"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorTellerDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorTellerDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorTogglDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorTogglDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorTogglDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorTogglDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorTogglDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorTogglDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorTogglDiscriminatedConnectorConfig(BaseModel):
    config: object

    connector_name: Literal["toggl"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorTogglDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorTogglDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorTwentyDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorTwentyDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorTwentyDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorTwentyDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorTwentyDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorTwentyDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorTwentyDiscriminatedConnectorConfig(BaseModel):
    config: object

    connector_name: Literal["twenty"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorTwentyDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorTwentyDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorVenmoDiscriminatedConnectorConfigConfigProxy(BaseModel):
    cert: str

    url: str


class ConnectorVenmoDiscriminatedConnectorConfigConfig(BaseModel):
    proxy: Optional[ConnectorVenmoDiscriminatedConnectorConfigConfigProxy] = None

    v1_base_url: Optional[str] = FieldInfo(alias="v1BaseURL", default=None)

    v5_base_url: Optional[str] = FieldInfo(alias="v5BaseURL", default=None)


class ConnectorVenmoDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorVenmoDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorVenmoDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorVenmoDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorVenmoDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorVenmoDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorVenmoDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorVenmoDiscriminatedConnectorConfigConfig

    connector_name: Literal["venmo"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorVenmoDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorVenmoDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorWiseDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorWiseDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorWiseDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorWiseDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorWiseDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorWiseDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorWiseDiscriminatedConnectorConfig(BaseModel):
    config: object

    connector_name: Literal["wise"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorWiseDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorWiseDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorYodleeDiscriminatedConnectorConfigConfigProxy(BaseModel):
    cert: str

    url: str


class ConnectorYodleeDiscriminatedConnectorConfigConfig(BaseModel):
    admin_login_name: str = FieldInfo(alias="adminLoginName")

    client_id: str = FieldInfo(alias="clientId")

    client_secret: str = FieldInfo(alias="clientSecret")

    env_name: Literal["sandbox", "development", "production"] = FieldInfo(alias="envName")

    proxy: Optional[ConnectorYodleeDiscriminatedConnectorConfigConfigProxy] = None

    sandbox_login_name: Optional[str] = FieldInfo(alias="sandboxLoginName", default=None)


class ConnectorYodleeDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorYodleeDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorYodleeDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorYodleeDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorYodleeDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorYodleeDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorYodleeDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorYodleeDiscriminatedConnectorConfigConfig

    connector_name: Literal["yodlee"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorYodleeDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorYodleeDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


ListConnectionConfigsResponse: TypeAlias = Union[
    ConnectorAcmeOauth2DiscriminatedConnectorConfig,
    ConnectorAircallDiscriminatedConnectorConfig,
    ConnectorConfluenceDiscriminatedConnectorConfig,
    ConnectorDiscordDiscriminatedConnectorConfig,
    ConnectorFacebookDiscriminatedConnectorConfig,
    ConnectorGitHubDiscriminatedConnectorConfig,
    ConnectorGongDiscriminatedConnectorConfig,
    ConnectorGoogleCalendarDiscriminatedConnectorConfig,
    ConnectorGoogleDocsDiscriminatedConnectorConfig,
    ConnectorGoogleDriveDiscriminatedConnectorConfig,
    ConnectorGoogleMailDiscriminatedConnectorConfig,
    ConnectorGoogleSheetDiscriminatedConnectorConfig,
    ConnectorHubspotDiscriminatedConnectorConfig,
    ConnectorInstagramDiscriminatedConnectorConfig,
    ConnectorIntercomDiscriminatedConnectorConfig,
    ConnectorJiraDiscriminatedConnectorConfig,
    ConnectorLeverDiscriminatedConnectorConfig,
    ConnectorLinearDiscriminatedConnectorConfig,
    ConnectorLinkedinDiscriminatedConnectorConfig,
    ConnectorNotionDiscriminatedConnectorConfig,
    ConnectorOutreachDiscriminatedConnectorConfig,
    ConnectorPipedriveDiscriminatedConnectorConfig,
    ConnectorQuickbooksDiscriminatedConnectorConfig,
    ConnectorRedditDiscriminatedConnectorConfig,
    ConnectorSalesloftDiscriminatedConnectorConfig,
    ConnectorSharepointDiscriminatedConnectorConfig,
    ConnectorSlackDiscriminatedConnectorConfig,
    ConnectorTwitterDiscriminatedConnectorConfig,
    ConnectorXeroDiscriminatedConnectorConfig,
    ConnectorZohoDeskDiscriminatedConnectorConfig,
    ConnectorAirtableDiscriminatedConnectorConfig,
    ConnectorApolloDiscriminatedConnectorConfig,
    ConnectorBrexDiscriminatedConnectorConfig,
    ConnectorCodaDiscriminatedConnectorConfig,
    ConnectorFinchDiscriminatedConnectorConfig,
    ConnectorFirebaseDiscriminatedConnectorConfig,
    ConnectorForeceiptDiscriminatedConnectorConfig,
    ConnectorGreenhouseDiscriminatedConnectorConfig,
    ConnectorHeronDiscriminatedConnectorConfig,
    ConnectorLunchmoneyDiscriminatedConnectorConfig,
    ConnectorMercuryDiscriminatedConnectorConfig,
    ConnectorMergeDiscriminatedConnectorConfig,
    ConnectorMootaDiscriminatedConnectorConfig,
    ConnectorOnebrickDiscriminatedConnectorConfig,
    ConnectorPlaidDiscriminatedConnectorConfig,
    ConnectorPostgresDiscriminatedConnectorConfig,
    ConnectorRampDiscriminatedConnectorConfig,
    ConnectorSaltedgeDiscriminatedConnectorConfig,
    ConnectorSplitwiseDiscriminatedConnectorConfig,
    ConnectorStripeDiscriminatedConnectorConfig,
    ConnectorTellerDiscriminatedConnectorConfig,
    ConnectorTogglDiscriminatedConnectorConfig,
    ConnectorTwentyDiscriminatedConnectorConfig,
    ConnectorVenmoDiscriminatedConnectorConfig,
    ConnectorWiseDiscriminatedConnectorConfig,
    ConnectorYodleeDiscriminatedConnectorConfig,
]
