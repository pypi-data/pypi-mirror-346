# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import TYPE_CHECKING, Dict, List, Union, Optional
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = [
    "ListConnectionsResponse",
    "ConnectorAcmeOauth2DiscriminatedConnectionSettings",
    "ConnectorAcmeOauth2DiscriminatedConnectionSettingsConnector",
    "ConnectorAcmeOauth2DiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorAcmeOauth2DiscriminatedConnectionSettingsConnectorScope",
    "ConnectorAcmeOauth2DiscriminatedConnectionSettingsIntegration",
    "ConnectorAcmeOauth2DiscriminatedConnectionSettingsSettings",
    "ConnectorAcmeOauth2DiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorAcmeOauth2DiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorAircallDiscriminatedConnectionSettings",
    "ConnectorAircallDiscriminatedConnectionSettingsConnector",
    "ConnectorAircallDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorAircallDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorAircallDiscriminatedConnectionSettingsIntegration",
    "ConnectorAircallDiscriminatedConnectionSettingsSettings",
    "ConnectorAircallDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorAircallDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorConfluenceDiscriminatedConnectionSettings",
    "ConnectorConfluenceDiscriminatedConnectionSettingsConnector",
    "ConnectorConfluenceDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorConfluenceDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorConfluenceDiscriminatedConnectionSettingsIntegration",
    "ConnectorConfluenceDiscriminatedConnectionSettingsSettings",
    "ConnectorConfluenceDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorConfluenceDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorDiscordDiscriminatedConnectionSettings",
    "ConnectorDiscordDiscriminatedConnectionSettingsConnector",
    "ConnectorDiscordDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorDiscordDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorDiscordDiscriminatedConnectionSettingsIntegration",
    "ConnectorDiscordDiscriminatedConnectionSettingsSettings",
    "ConnectorDiscordDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorDiscordDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorFacebookDiscriminatedConnectionSettings",
    "ConnectorFacebookDiscriminatedConnectionSettingsConnector",
    "ConnectorFacebookDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorFacebookDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorFacebookDiscriminatedConnectionSettingsIntegration",
    "ConnectorFacebookDiscriminatedConnectionSettingsSettings",
    "ConnectorFacebookDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorFacebookDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorGitHubDiscriminatedConnectionSettings",
    "ConnectorGitHubDiscriminatedConnectionSettingsConnector",
    "ConnectorGitHubDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorGitHubDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorGitHubDiscriminatedConnectionSettingsIntegration",
    "ConnectorGitHubDiscriminatedConnectionSettingsSettings",
    "ConnectorGitHubDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorGitHubDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorGongDiscriminatedConnectionSettings",
    "ConnectorGongDiscriminatedConnectionSettingsConnector",
    "ConnectorGongDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorGongDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorGongDiscriminatedConnectionSettingsIntegration",
    "ConnectorGongDiscriminatedConnectionSettingsSettings",
    "ConnectorGongDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorGongDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorGoogleCalendarDiscriminatedConnectionSettings",
    "ConnectorGoogleCalendarDiscriminatedConnectionSettingsConnector",
    "ConnectorGoogleCalendarDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorGoogleCalendarDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorGoogleCalendarDiscriminatedConnectionSettingsIntegration",
    "ConnectorGoogleCalendarDiscriminatedConnectionSettingsSettings",
    "ConnectorGoogleCalendarDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorGoogleCalendarDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorGoogleDocsDiscriminatedConnectionSettings",
    "ConnectorGoogleDocsDiscriminatedConnectionSettingsConnector",
    "ConnectorGoogleDocsDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorGoogleDocsDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorGoogleDocsDiscriminatedConnectionSettingsIntegration",
    "ConnectorGoogleDocsDiscriminatedConnectionSettingsSettings",
    "ConnectorGoogleDocsDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorGoogleDocsDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorGoogleDriveDiscriminatedConnectionSettings",
    "ConnectorGoogleDriveDiscriminatedConnectionSettingsConnector",
    "ConnectorGoogleDriveDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorGoogleDriveDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorGoogleDriveDiscriminatedConnectionSettingsIntegration",
    "ConnectorGoogleDriveDiscriminatedConnectionSettingsSettings",
    "ConnectorGoogleDriveDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorGoogleDriveDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorGoogleMailDiscriminatedConnectionSettings",
    "ConnectorGoogleMailDiscriminatedConnectionSettingsConnector",
    "ConnectorGoogleMailDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorGoogleMailDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorGoogleMailDiscriminatedConnectionSettingsIntegration",
    "ConnectorGoogleMailDiscriminatedConnectionSettingsSettings",
    "ConnectorGoogleMailDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorGoogleMailDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorGoogleSheetDiscriminatedConnectionSettings",
    "ConnectorGoogleSheetDiscriminatedConnectionSettingsConnector",
    "ConnectorGoogleSheetDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorGoogleSheetDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorGoogleSheetDiscriminatedConnectionSettingsIntegration",
    "ConnectorGoogleSheetDiscriminatedConnectionSettingsSettings",
    "ConnectorGoogleSheetDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorGoogleSheetDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorHubspotDiscriminatedConnectionSettings",
    "ConnectorHubspotDiscriminatedConnectionSettingsConnector",
    "ConnectorHubspotDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorHubspotDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorHubspotDiscriminatedConnectionSettingsIntegration",
    "ConnectorHubspotDiscriminatedConnectionSettingsSettings",
    "ConnectorHubspotDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorHubspotDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorInstagramDiscriminatedConnectionSettings",
    "ConnectorInstagramDiscriminatedConnectionSettingsConnector",
    "ConnectorInstagramDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorInstagramDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorInstagramDiscriminatedConnectionSettingsIntegration",
    "ConnectorInstagramDiscriminatedConnectionSettingsSettings",
    "ConnectorInstagramDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorInstagramDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorIntercomDiscriminatedConnectionSettings",
    "ConnectorIntercomDiscriminatedConnectionSettingsConnector",
    "ConnectorIntercomDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorIntercomDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorIntercomDiscriminatedConnectionSettingsIntegration",
    "ConnectorIntercomDiscriminatedConnectionSettingsSettings",
    "ConnectorIntercomDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorIntercomDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorJiraDiscriminatedConnectionSettings",
    "ConnectorJiraDiscriminatedConnectionSettingsConnector",
    "ConnectorJiraDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorJiraDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorJiraDiscriminatedConnectionSettingsIntegration",
    "ConnectorJiraDiscriminatedConnectionSettingsSettings",
    "ConnectorJiraDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorJiraDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorLeverDiscriminatedConnectionSettings",
    "ConnectorLeverDiscriminatedConnectionSettingsConnector",
    "ConnectorLeverDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorLeverDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorLeverDiscriminatedConnectionSettingsIntegration",
    "ConnectorLeverDiscriminatedConnectionSettingsSettings",
    "ConnectorLeverDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorLeverDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorLinearDiscriminatedConnectionSettings",
    "ConnectorLinearDiscriminatedConnectionSettingsConnector",
    "ConnectorLinearDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorLinearDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorLinearDiscriminatedConnectionSettingsIntegration",
    "ConnectorLinearDiscriminatedConnectionSettingsSettings",
    "ConnectorLinearDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorLinearDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorLinkedinDiscriminatedConnectionSettings",
    "ConnectorLinkedinDiscriminatedConnectionSettingsConnector",
    "ConnectorLinkedinDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorLinkedinDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorLinkedinDiscriminatedConnectionSettingsIntegration",
    "ConnectorLinkedinDiscriminatedConnectionSettingsSettings",
    "ConnectorLinkedinDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorLinkedinDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorNotionDiscriminatedConnectionSettings",
    "ConnectorNotionDiscriminatedConnectionSettingsConnector",
    "ConnectorNotionDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorNotionDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorNotionDiscriminatedConnectionSettingsIntegration",
    "ConnectorNotionDiscriminatedConnectionSettingsSettings",
    "ConnectorNotionDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorNotionDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorOutreachDiscriminatedConnectionSettings",
    "ConnectorOutreachDiscriminatedConnectionSettingsConnector",
    "ConnectorOutreachDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorOutreachDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorOutreachDiscriminatedConnectionSettingsIntegration",
    "ConnectorOutreachDiscriminatedConnectionSettingsSettings",
    "ConnectorOutreachDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorOutreachDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorPipedriveDiscriminatedConnectionSettings",
    "ConnectorPipedriveDiscriminatedConnectionSettingsConnector",
    "ConnectorPipedriveDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorPipedriveDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorPipedriveDiscriminatedConnectionSettingsIntegration",
    "ConnectorPipedriveDiscriminatedConnectionSettingsSettings",
    "ConnectorPipedriveDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorPipedriveDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorQuickbooksDiscriminatedConnectionSettings",
    "ConnectorQuickbooksDiscriminatedConnectionSettingsConnector",
    "ConnectorQuickbooksDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorQuickbooksDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorQuickbooksDiscriminatedConnectionSettingsIntegration",
    "ConnectorQuickbooksDiscriminatedConnectionSettingsSettings",
    "ConnectorQuickbooksDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorQuickbooksDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorRedditDiscriminatedConnectionSettings",
    "ConnectorRedditDiscriminatedConnectionSettingsConnector",
    "ConnectorRedditDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorRedditDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorRedditDiscriminatedConnectionSettingsIntegration",
    "ConnectorRedditDiscriminatedConnectionSettingsSettings",
    "ConnectorRedditDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorRedditDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorSalesloftDiscriminatedConnectionSettings",
    "ConnectorSalesloftDiscriminatedConnectionSettingsConnector",
    "ConnectorSalesloftDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorSalesloftDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorSalesloftDiscriminatedConnectionSettingsIntegration",
    "ConnectorSalesloftDiscriminatedConnectionSettingsSettings",
    "ConnectorSalesloftDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorSalesloftDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorSharepointDiscriminatedConnectionSettings",
    "ConnectorSharepointDiscriminatedConnectionSettingsConnector",
    "ConnectorSharepointDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorSharepointDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorSharepointDiscriminatedConnectionSettingsIntegration",
    "ConnectorSharepointDiscriminatedConnectionSettingsSettings",
    "ConnectorSharepointDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorSharepointDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorSlackDiscriminatedConnectionSettings",
    "ConnectorSlackDiscriminatedConnectionSettingsConnector",
    "ConnectorSlackDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorSlackDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorSlackDiscriminatedConnectionSettingsIntegration",
    "ConnectorSlackDiscriminatedConnectionSettingsSettings",
    "ConnectorSlackDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorSlackDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorTwitterDiscriminatedConnectionSettings",
    "ConnectorTwitterDiscriminatedConnectionSettingsConnector",
    "ConnectorTwitterDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorTwitterDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorTwitterDiscriminatedConnectionSettingsIntegration",
    "ConnectorTwitterDiscriminatedConnectionSettingsSettings",
    "ConnectorTwitterDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorTwitterDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorXeroDiscriminatedConnectionSettings",
    "ConnectorXeroDiscriminatedConnectionSettingsConnector",
    "ConnectorXeroDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorXeroDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorXeroDiscriminatedConnectionSettingsIntegration",
    "ConnectorXeroDiscriminatedConnectionSettingsSettings",
    "ConnectorXeroDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorXeroDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorZohoDeskDiscriminatedConnectionSettings",
    "ConnectorZohoDeskDiscriminatedConnectionSettingsConnector",
    "ConnectorZohoDeskDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorZohoDeskDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorZohoDeskDiscriminatedConnectionSettingsIntegration",
    "ConnectorZohoDeskDiscriminatedConnectionSettingsSettings",
    "ConnectorZohoDeskDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorZohoDeskDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorAirtableDiscriminatedConnectionSettings",
    "ConnectorAirtableDiscriminatedConnectionSettingsConnector",
    "ConnectorAirtableDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorAirtableDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorAirtableDiscriminatedConnectionSettingsIntegration",
    "ConnectorAirtableDiscriminatedConnectionSettingsSettings",
    "ConnectorApolloDiscriminatedConnectionSettings",
    "ConnectorApolloDiscriminatedConnectionSettingsConnector",
    "ConnectorApolloDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorApolloDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorApolloDiscriminatedConnectionSettingsIntegration",
    "ConnectorApolloDiscriminatedConnectionSettingsSettings",
    "ConnectorBrexDiscriminatedConnectionSettings",
    "ConnectorBrexDiscriminatedConnectionSettingsConnector",
    "ConnectorBrexDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorBrexDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorBrexDiscriminatedConnectionSettingsIntegration",
    "ConnectorBrexDiscriminatedConnectionSettingsSettings",
    "ConnectorCodaDiscriminatedConnectionSettings",
    "ConnectorCodaDiscriminatedConnectionSettingsConnector",
    "ConnectorCodaDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorCodaDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorCodaDiscriminatedConnectionSettingsIntegration",
    "ConnectorCodaDiscriminatedConnectionSettingsSettings",
    "ConnectorFinchDiscriminatedConnectionSettings",
    "ConnectorFinchDiscriminatedConnectionSettingsConnector",
    "ConnectorFinchDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorFinchDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorFinchDiscriminatedConnectionSettingsIntegration",
    "ConnectorFinchDiscriminatedConnectionSettingsSettings",
    "ConnectorFirebaseDiscriminatedConnectionSettings",
    "ConnectorFirebaseDiscriminatedConnectionSettingsConnector",
    "ConnectorFirebaseDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorFirebaseDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorFirebaseDiscriminatedConnectionSettingsIntegration",
    "ConnectorFirebaseDiscriminatedConnectionSettingsSettings",
    "ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember0",
    "ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember0ServiceAccount",
    "ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1",
    "ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthData",
    "ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember0",
    "ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember0UserJson",
    "ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember1",
    "ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember2",
    "ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1FirebaseConfig",
    "ConnectorForeceiptDiscriminatedConnectionSettings",
    "ConnectorForeceiptDiscriminatedConnectionSettingsConnector",
    "ConnectorForeceiptDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorForeceiptDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorForeceiptDiscriminatedConnectionSettingsIntegration",
    "ConnectorForeceiptDiscriminatedConnectionSettingsSettings",
    "ConnectorGreenhouseDiscriminatedConnectionSettings",
    "ConnectorGreenhouseDiscriminatedConnectionSettingsConnector",
    "ConnectorGreenhouseDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorGreenhouseDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorGreenhouseDiscriminatedConnectionSettingsIntegration",
    "ConnectorGreenhouseDiscriminatedConnectionSettingsSettings",
    "ConnectorHeronDiscriminatedConnectionSettings",
    "ConnectorHeronDiscriminatedConnectionSettingsConnector",
    "ConnectorHeronDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorHeronDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorHeronDiscriminatedConnectionSettingsIntegration",
    "ConnectorLunchmoneyDiscriminatedConnectionSettings",
    "ConnectorLunchmoneyDiscriminatedConnectionSettingsConnector",
    "ConnectorLunchmoneyDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorLunchmoneyDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorLunchmoneyDiscriminatedConnectionSettingsIntegration",
    "ConnectorMercuryDiscriminatedConnectionSettings",
    "ConnectorMercuryDiscriminatedConnectionSettingsConnector",
    "ConnectorMercuryDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorMercuryDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorMercuryDiscriminatedConnectionSettingsIntegration",
    "ConnectorMergeDiscriminatedConnectionSettings",
    "ConnectorMergeDiscriminatedConnectionSettingsConnector",
    "ConnectorMergeDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorMergeDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorMergeDiscriminatedConnectionSettingsIntegration",
    "ConnectorMergeDiscriminatedConnectionSettingsSettings",
    "ConnectorMootaDiscriminatedConnectionSettings",
    "ConnectorMootaDiscriminatedConnectionSettingsConnector",
    "ConnectorMootaDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorMootaDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorMootaDiscriminatedConnectionSettingsIntegration",
    "ConnectorOnebrickDiscriminatedConnectionSettings",
    "ConnectorOnebrickDiscriminatedConnectionSettingsConnector",
    "ConnectorOnebrickDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorOnebrickDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorOnebrickDiscriminatedConnectionSettingsIntegration",
    "ConnectorOnebrickDiscriminatedConnectionSettingsSettings",
    "ConnectorPlaidDiscriminatedConnectionSettings",
    "ConnectorPlaidDiscriminatedConnectionSettingsConnector",
    "ConnectorPlaidDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorPlaidDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorPlaidDiscriminatedConnectionSettingsIntegration",
    "ConnectorPlaidDiscriminatedConnectionSettingsSettings",
    "ConnectorPostgresDiscriminatedConnectionSettings",
    "ConnectorPostgresDiscriminatedConnectionSettingsConnector",
    "ConnectorPostgresDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorPostgresDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorPostgresDiscriminatedConnectionSettingsIntegration",
    "ConnectorPostgresDiscriminatedConnectionSettingsSettings",
    "ConnectorRampDiscriminatedConnectionSettings",
    "ConnectorRampDiscriminatedConnectionSettingsConnector",
    "ConnectorRampDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorRampDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorRampDiscriminatedConnectionSettingsIntegration",
    "ConnectorRampDiscriminatedConnectionSettingsSettings",
    "ConnectorSaltedgeDiscriminatedConnectionSettings",
    "ConnectorSaltedgeDiscriminatedConnectionSettingsConnector",
    "ConnectorSaltedgeDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorSaltedgeDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorSaltedgeDiscriminatedConnectionSettingsIntegration",
    "ConnectorSplitwiseDiscriminatedConnectionSettings",
    "ConnectorSplitwiseDiscriminatedConnectionSettingsConnector",
    "ConnectorSplitwiseDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorSplitwiseDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorSplitwiseDiscriminatedConnectionSettingsIntegration",
    "ConnectorSplitwiseDiscriminatedConnectionSettingsSettings",
    "ConnectorSplitwiseDiscriminatedConnectionSettingsSettingsCurrentUser",
    "ConnectorSplitwiseDiscriminatedConnectionSettingsSettingsCurrentUserNotifications",
    "ConnectorSplitwiseDiscriminatedConnectionSettingsSettingsCurrentUserPicture",
    "ConnectorStripeDiscriminatedConnectionSettings",
    "ConnectorStripeDiscriminatedConnectionSettingsConnector",
    "ConnectorStripeDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorStripeDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorStripeDiscriminatedConnectionSettingsIntegration",
    "ConnectorStripeDiscriminatedConnectionSettingsSettings",
    "ConnectorTellerDiscriminatedConnectionSettings",
    "ConnectorTellerDiscriminatedConnectionSettingsConnector",
    "ConnectorTellerDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorTellerDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorTellerDiscriminatedConnectionSettingsIntegration",
    "ConnectorTellerDiscriminatedConnectionSettingsSettings",
    "ConnectorTogglDiscriminatedConnectionSettings",
    "ConnectorTogglDiscriminatedConnectionSettingsConnector",
    "ConnectorTogglDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorTogglDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorTogglDiscriminatedConnectionSettingsIntegration",
    "ConnectorTogglDiscriminatedConnectionSettingsSettings",
    "ConnectorTwentyDiscriminatedConnectionSettings",
    "ConnectorTwentyDiscriminatedConnectionSettingsConnector",
    "ConnectorTwentyDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorTwentyDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorTwentyDiscriminatedConnectionSettingsIntegration",
    "ConnectorTwentyDiscriminatedConnectionSettingsSettings",
    "ConnectorVenmoDiscriminatedConnectionSettings",
    "ConnectorVenmoDiscriminatedConnectionSettingsConnector",
    "ConnectorVenmoDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorVenmoDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorVenmoDiscriminatedConnectionSettingsIntegration",
    "ConnectorVenmoDiscriminatedConnectionSettingsSettings",
    "ConnectorWiseDiscriminatedConnectionSettings",
    "ConnectorWiseDiscriminatedConnectionSettingsConnector",
    "ConnectorWiseDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorWiseDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorWiseDiscriminatedConnectionSettingsIntegration",
    "ConnectorWiseDiscriminatedConnectionSettingsSettings",
    "ConnectorYodleeDiscriminatedConnectionSettings",
    "ConnectorYodleeDiscriminatedConnectionSettingsConnector",
    "ConnectorYodleeDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorYodleeDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorYodleeDiscriminatedConnectionSettingsIntegration",
    "ConnectorYodleeDiscriminatedConnectionSettingsSettings",
    "ConnectorYodleeDiscriminatedConnectionSettingsSettingsAccessToken",
    "ConnectorYodleeDiscriminatedConnectionSettingsSettingsProviderAccount",
]


class ConnectorAcmeOauth2DiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorAcmeOauth2DiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorAcmeOauth2DiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorAcmeOauth2DiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorAcmeOauth2DiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorAcmeOauth2DiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorAcmeOauth2DiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    access_token: str

    client_id: Optional[str] = None
    """Client ID used for the connection"""

    expires_at: Optional[str] = None

    expires_in: Optional[float] = None

    raw: Optional[Dict[str, object]] = None

    refresh_token: Optional[str] = None

    scope: Optional[str] = None

    token_type: Optional[str] = None


class ConnectorAcmeOauth2DiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    created_at: Optional[str] = None

    credentials: Optional[ConnectorAcmeOauth2DiscriminatedConnectionSettingsSettingsOAuthCredentials] = None
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[str] = None


class ConnectorAcmeOauth2DiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorAcmeOauth2DiscriminatedConnectionSettingsSettingsOAuth


class ConnectorAcmeOauth2DiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["acme-oauth2"]

    id: Optional[str] = None

    connector: Optional[ConnectorAcmeOauth2DiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorAcmeOauth2DiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorAcmeOauth2DiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorAircallDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorAircallDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorAircallDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorAircallDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorAircallDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorAircallDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorAircallDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    access_token: str

    client_id: Optional[str] = None
    """Client ID used for the connection"""

    expires_at: Optional[str] = None

    expires_in: Optional[float] = None

    raw: Optional[Dict[str, object]] = None

    refresh_token: Optional[str] = None

    scope: Optional[str] = None

    token_type: Optional[str] = None


class ConnectorAircallDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    created_at: Optional[str] = None

    credentials: Optional[ConnectorAircallDiscriminatedConnectionSettingsSettingsOAuthCredentials] = None
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[str] = None


class ConnectorAircallDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorAircallDiscriminatedConnectionSettingsSettingsOAuth


class ConnectorAircallDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["aircall"]

    id: Optional[str] = None

    connector: Optional[ConnectorAircallDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorAircallDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorAircallDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorConfluenceDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorConfluenceDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorConfluenceDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorConfluenceDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorConfluenceDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorConfluenceDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorConfluenceDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    access_token: str

    client_id: Optional[str] = None
    """Client ID used for the connection"""

    expires_at: Optional[str] = None

    expires_in: Optional[float] = None

    raw: Optional[Dict[str, object]] = None

    refresh_token: Optional[str] = None

    scope: Optional[str] = None

    token_type: Optional[str] = None


class ConnectorConfluenceDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    created_at: Optional[str] = None

    credentials: Optional[ConnectorConfluenceDiscriminatedConnectionSettingsSettingsOAuthCredentials] = None
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[str] = None


class ConnectorConfluenceDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorConfluenceDiscriminatedConnectionSettingsSettingsOAuth


class ConnectorConfluenceDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["confluence"]

    id: Optional[str] = None

    connector: Optional[ConnectorConfluenceDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorConfluenceDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorConfluenceDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorDiscordDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorDiscordDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorDiscordDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorDiscordDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorDiscordDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorDiscordDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorDiscordDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    access_token: str

    client_id: Optional[str] = None
    """Client ID used for the connection"""

    expires_at: Optional[str] = None

    expires_in: Optional[float] = None

    raw: Optional[Dict[str, object]] = None

    refresh_token: Optional[str] = None

    scope: Optional[str] = None

    token_type: Optional[str] = None


class ConnectorDiscordDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    created_at: Optional[str] = None

    credentials: Optional[ConnectorDiscordDiscriminatedConnectionSettingsSettingsOAuthCredentials] = None
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[str] = None


class ConnectorDiscordDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorDiscordDiscriminatedConnectionSettingsSettingsOAuth


class ConnectorDiscordDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["discord"]

    id: Optional[str] = None

    connector: Optional[ConnectorDiscordDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorDiscordDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorDiscordDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorFacebookDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorFacebookDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorFacebookDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorFacebookDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorFacebookDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorFacebookDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorFacebookDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    access_token: str

    client_id: Optional[str] = None
    """Client ID used for the connection"""

    expires_at: Optional[str] = None

    expires_in: Optional[float] = None

    raw: Optional[Dict[str, object]] = None

    refresh_token: Optional[str] = None

    scope: Optional[str] = None

    token_type: Optional[str] = None


class ConnectorFacebookDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    created_at: Optional[str] = None

    credentials: Optional[ConnectorFacebookDiscriminatedConnectionSettingsSettingsOAuthCredentials] = None
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[str] = None


class ConnectorFacebookDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorFacebookDiscriminatedConnectionSettingsSettingsOAuth


class ConnectorFacebookDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["facebook"]

    id: Optional[str] = None

    connector: Optional[ConnectorFacebookDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorFacebookDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorFacebookDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorGitHubDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorGitHubDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorGitHubDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorGitHubDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorGitHubDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorGitHubDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorGitHubDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    access_token: str

    client_id: Optional[str] = None
    """Client ID used for the connection"""

    expires_at: Optional[str] = None

    expires_in: Optional[float] = None

    raw: Optional[Dict[str, object]] = None

    refresh_token: Optional[str] = None

    scope: Optional[str] = None

    token_type: Optional[str] = None


class ConnectorGitHubDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    created_at: Optional[str] = None

    credentials: Optional[ConnectorGitHubDiscriminatedConnectionSettingsSettingsOAuthCredentials] = None
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[str] = None


class ConnectorGitHubDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorGitHubDiscriminatedConnectionSettingsSettingsOAuth


class ConnectorGitHubDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["github"]

    id: Optional[str] = None

    connector: Optional[ConnectorGitHubDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorGitHubDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorGitHubDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorGongDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorGongDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorGongDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorGongDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorGongDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorGongDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorGongDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    access_token: str

    client_id: Optional[str] = None
    """Client ID used for the connection"""

    expires_at: Optional[str] = None

    expires_in: Optional[float] = None

    raw: Optional[Dict[str, object]] = None

    refresh_token: Optional[str] = None

    scope: Optional[str] = None

    token_type: Optional[str] = None


class ConnectorGongDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    created_at: Optional[str] = None

    credentials: Optional[ConnectorGongDiscriminatedConnectionSettingsSettingsOAuthCredentials] = None
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[str] = None


class ConnectorGongDiscriminatedConnectionSettingsSettings(BaseModel):
    api_base_url_for_customer: str
    """The base URL of your Gong account (e.g., example)"""

    oauth: ConnectorGongDiscriminatedConnectionSettingsSettingsOAuth


class ConnectorGongDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["gong"]

    id: Optional[str] = None

    connector: Optional[ConnectorGongDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorGongDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorGongDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorGoogleCalendarDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorGoogleCalendarDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorGoogleCalendarDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorGoogleCalendarDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorGoogleCalendarDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorGoogleCalendarDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorGoogleCalendarDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    access_token: str

    client_id: Optional[str] = None
    """Client ID used for the connection"""

    expires_at: Optional[str] = None

    expires_in: Optional[float] = None

    raw: Optional[Dict[str, object]] = None

    refresh_token: Optional[str] = None

    scope: Optional[str] = None

    token_type: Optional[str] = None


class ConnectorGoogleCalendarDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    created_at: Optional[str] = None

    credentials: Optional[ConnectorGoogleCalendarDiscriminatedConnectionSettingsSettingsOAuthCredentials] = None
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[str] = None


class ConnectorGoogleCalendarDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorGoogleCalendarDiscriminatedConnectionSettingsSettingsOAuth


class ConnectorGoogleCalendarDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["google-calendar"]

    id: Optional[str] = None

    connector: Optional[ConnectorGoogleCalendarDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorGoogleCalendarDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorGoogleCalendarDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorGoogleDocsDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorGoogleDocsDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorGoogleDocsDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorGoogleDocsDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorGoogleDocsDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorGoogleDocsDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorGoogleDocsDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    access_token: str

    client_id: Optional[str] = None
    """Client ID used for the connection"""

    expires_at: Optional[str] = None

    expires_in: Optional[float] = None

    raw: Optional[Dict[str, object]] = None

    refresh_token: Optional[str] = None

    scope: Optional[str] = None

    token_type: Optional[str] = None


class ConnectorGoogleDocsDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    created_at: Optional[str] = None

    credentials: Optional[ConnectorGoogleDocsDiscriminatedConnectionSettingsSettingsOAuthCredentials] = None
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[str] = None


class ConnectorGoogleDocsDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorGoogleDocsDiscriminatedConnectionSettingsSettingsOAuth


class ConnectorGoogleDocsDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["google-docs"]

    id: Optional[str] = None

    connector: Optional[ConnectorGoogleDocsDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorGoogleDocsDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorGoogleDocsDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorGoogleDriveDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorGoogleDriveDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorGoogleDriveDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorGoogleDriveDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorGoogleDriveDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorGoogleDriveDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorGoogleDriveDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    access_token: str

    client_id: Optional[str] = None
    """Client ID used for the connection"""

    expires_at: Optional[str] = None

    expires_in: Optional[float] = None

    raw: Optional[Dict[str, object]] = None

    refresh_token: Optional[str] = None

    scope: Optional[str] = None

    token_type: Optional[str] = None


class ConnectorGoogleDriveDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    created_at: Optional[str] = None

    credentials: Optional[ConnectorGoogleDriveDiscriminatedConnectionSettingsSettingsOAuthCredentials] = None
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[str] = None


class ConnectorGoogleDriveDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorGoogleDriveDiscriminatedConnectionSettingsSettingsOAuth


class ConnectorGoogleDriveDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["google-drive"]

    id: Optional[str] = None

    connector: Optional[ConnectorGoogleDriveDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorGoogleDriveDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorGoogleDriveDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorGoogleMailDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorGoogleMailDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorGoogleMailDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorGoogleMailDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorGoogleMailDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorGoogleMailDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorGoogleMailDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    access_token: str

    client_id: Optional[str] = None
    """Client ID used for the connection"""

    expires_at: Optional[str] = None

    expires_in: Optional[float] = None

    raw: Optional[Dict[str, object]] = None

    refresh_token: Optional[str] = None

    scope: Optional[str] = None

    token_type: Optional[str] = None


class ConnectorGoogleMailDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    created_at: Optional[str] = None

    credentials: Optional[ConnectorGoogleMailDiscriminatedConnectionSettingsSettingsOAuthCredentials] = None
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[str] = None


class ConnectorGoogleMailDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorGoogleMailDiscriminatedConnectionSettingsSettingsOAuth


class ConnectorGoogleMailDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["google-mail"]

    id: Optional[str] = None

    connector: Optional[ConnectorGoogleMailDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorGoogleMailDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorGoogleMailDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorGoogleSheetDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorGoogleSheetDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorGoogleSheetDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorGoogleSheetDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorGoogleSheetDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorGoogleSheetDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorGoogleSheetDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    access_token: str

    client_id: Optional[str] = None
    """Client ID used for the connection"""

    expires_at: Optional[str] = None

    expires_in: Optional[float] = None

    raw: Optional[Dict[str, object]] = None

    refresh_token: Optional[str] = None

    scope: Optional[str] = None

    token_type: Optional[str] = None


class ConnectorGoogleSheetDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    created_at: Optional[str] = None

    credentials: Optional[ConnectorGoogleSheetDiscriminatedConnectionSettingsSettingsOAuthCredentials] = None
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[str] = None


class ConnectorGoogleSheetDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorGoogleSheetDiscriminatedConnectionSettingsSettingsOAuth


class ConnectorGoogleSheetDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["google-sheet"]

    id: Optional[str] = None

    connector: Optional[ConnectorGoogleSheetDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorGoogleSheetDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorGoogleSheetDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorHubspotDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorHubspotDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorHubspotDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorHubspotDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorHubspotDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorHubspotDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorHubspotDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    access_token: str

    client_id: Optional[str] = None
    """Client ID used for the connection"""

    expires_at: Optional[str] = None

    expires_in: Optional[float] = None

    raw: Optional[Dict[str, object]] = None

    refresh_token: Optional[str] = None

    scope: Optional[str] = None

    token_type: Optional[str] = None


class ConnectorHubspotDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    created_at: Optional[str] = None

    credentials: Optional[ConnectorHubspotDiscriminatedConnectionSettingsSettingsOAuthCredentials] = None
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[str] = None


class ConnectorHubspotDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorHubspotDiscriminatedConnectionSettingsSettingsOAuth


class ConnectorHubspotDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["hubspot"]

    id: Optional[str] = None

    connector: Optional[ConnectorHubspotDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorHubspotDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorHubspotDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorInstagramDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorInstagramDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorInstagramDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorInstagramDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorInstagramDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorInstagramDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorInstagramDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    access_token: str

    client_id: Optional[str] = None
    """Client ID used for the connection"""

    expires_at: Optional[str] = None

    expires_in: Optional[float] = None

    raw: Optional[Dict[str, object]] = None

    refresh_token: Optional[str] = None

    scope: Optional[str] = None

    token_type: Optional[str] = None


class ConnectorInstagramDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    created_at: Optional[str] = None

    credentials: Optional[ConnectorInstagramDiscriminatedConnectionSettingsSettingsOAuthCredentials] = None
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[str] = None


class ConnectorInstagramDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorInstagramDiscriminatedConnectionSettingsSettingsOAuth


class ConnectorInstagramDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["instagram"]

    id: Optional[str] = None

    connector: Optional[ConnectorInstagramDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorInstagramDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorInstagramDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorIntercomDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorIntercomDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorIntercomDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorIntercomDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorIntercomDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorIntercomDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorIntercomDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    access_token: str

    client_id: Optional[str] = None
    """Client ID used for the connection"""

    expires_at: Optional[str] = None

    expires_in: Optional[float] = None

    raw: Optional[Dict[str, object]] = None

    refresh_token: Optional[str] = None

    scope: Optional[str] = None

    token_type: Optional[str] = None


class ConnectorIntercomDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    created_at: Optional[str] = None

    credentials: Optional[ConnectorIntercomDiscriminatedConnectionSettingsSettingsOAuthCredentials] = None
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[str] = None


class ConnectorIntercomDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorIntercomDiscriminatedConnectionSettingsSettingsOAuth


class ConnectorIntercomDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["intercom"]

    id: Optional[str] = None

    connector: Optional[ConnectorIntercomDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorIntercomDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorIntercomDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorJiraDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorJiraDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorJiraDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorJiraDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorJiraDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorJiraDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorJiraDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    access_token: str

    client_id: Optional[str] = None
    """Client ID used for the connection"""

    expires_at: Optional[str] = None

    expires_in: Optional[float] = None

    raw: Optional[Dict[str, object]] = None

    refresh_token: Optional[str] = None

    scope: Optional[str] = None

    token_type: Optional[str] = None


class ConnectorJiraDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    created_at: Optional[str] = None

    credentials: Optional[ConnectorJiraDiscriminatedConnectionSettingsSettingsOAuthCredentials] = None
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[str] = None


class ConnectorJiraDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorJiraDiscriminatedConnectionSettingsSettingsOAuth


class ConnectorJiraDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["jira"]

    id: Optional[str] = None

    connector: Optional[ConnectorJiraDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorJiraDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorJiraDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorLeverDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorLeverDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorLeverDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorLeverDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorLeverDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorLeverDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorLeverDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    access_token: str

    client_id: Optional[str] = None
    """Client ID used for the connection"""

    expires_at: Optional[str] = None

    expires_in: Optional[float] = None

    raw: Optional[Dict[str, object]] = None

    refresh_token: Optional[str] = None

    scope: Optional[str] = None

    token_type: Optional[str] = None


class ConnectorLeverDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    created_at: Optional[str] = None

    credentials: Optional[ConnectorLeverDiscriminatedConnectionSettingsSettingsOAuthCredentials] = None
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[str] = None


class ConnectorLeverDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorLeverDiscriminatedConnectionSettingsSettingsOAuth


class ConnectorLeverDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["lever"]

    id: Optional[str] = None

    connector: Optional[ConnectorLeverDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorLeverDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorLeverDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorLinearDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorLinearDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorLinearDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorLinearDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorLinearDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorLinearDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorLinearDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    access_token: str

    client_id: Optional[str] = None
    """Client ID used for the connection"""

    expires_at: Optional[str] = None

    expires_in: Optional[float] = None

    raw: Optional[Dict[str, object]] = None

    refresh_token: Optional[str] = None

    scope: Optional[str] = None

    token_type: Optional[str] = None


class ConnectorLinearDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    created_at: Optional[str] = None

    credentials: Optional[ConnectorLinearDiscriminatedConnectionSettingsSettingsOAuthCredentials] = None
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[str] = None


class ConnectorLinearDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorLinearDiscriminatedConnectionSettingsSettingsOAuth


class ConnectorLinearDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["linear"]

    id: Optional[str] = None

    connector: Optional[ConnectorLinearDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorLinearDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorLinearDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorLinkedinDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorLinkedinDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorLinkedinDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorLinkedinDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorLinkedinDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorLinkedinDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorLinkedinDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    access_token: str

    client_id: Optional[str] = None
    """Client ID used for the connection"""

    expires_at: Optional[str] = None

    expires_in: Optional[float] = None

    raw: Optional[Dict[str, object]] = None

    refresh_token: Optional[str] = None

    scope: Optional[str] = None

    token_type: Optional[str] = None


class ConnectorLinkedinDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    created_at: Optional[str] = None

    credentials: Optional[ConnectorLinkedinDiscriminatedConnectionSettingsSettingsOAuthCredentials] = None
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[str] = None


class ConnectorLinkedinDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorLinkedinDiscriminatedConnectionSettingsSettingsOAuth


class ConnectorLinkedinDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["linkedin"]

    id: Optional[str] = None

    connector: Optional[ConnectorLinkedinDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorLinkedinDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorLinkedinDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorNotionDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorNotionDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorNotionDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorNotionDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorNotionDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorNotionDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorNotionDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    access_token: str

    client_id: Optional[str] = None
    """Client ID used for the connection"""

    expires_at: Optional[str] = None

    expires_in: Optional[float] = None

    raw: Optional[Dict[str, object]] = None

    refresh_token: Optional[str] = None

    scope: Optional[str] = None

    token_type: Optional[str] = None


class ConnectorNotionDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    created_at: Optional[str] = None

    credentials: Optional[ConnectorNotionDiscriminatedConnectionSettingsSettingsOAuthCredentials] = None
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[str] = None


class ConnectorNotionDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorNotionDiscriminatedConnectionSettingsSettingsOAuth


class ConnectorNotionDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["notion"]

    id: Optional[str] = None

    connector: Optional[ConnectorNotionDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorNotionDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorNotionDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorOutreachDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorOutreachDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorOutreachDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorOutreachDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorOutreachDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorOutreachDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorOutreachDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    access_token: str

    client_id: Optional[str] = None
    """Client ID used for the connection"""

    expires_at: Optional[str] = None

    expires_in: Optional[float] = None

    raw: Optional[Dict[str, object]] = None

    refresh_token: Optional[str] = None

    scope: Optional[str] = None

    token_type: Optional[str] = None


class ConnectorOutreachDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    created_at: Optional[str] = None

    credentials: Optional[ConnectorOutreachDiscriminatedConnectionSettingsSettingsOAuthCredentials] = None
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[str] = None


class ConnectorOutreachDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorOutreachDiscriminatedConnectionSettingsSettingsOAuth


class ConnectorOutreachDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["outreach"]

    id: Optional[str] = None

    connector: Optional[ConnectorOutreachDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorOutreachDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorOutreachDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorPipedriveDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorPipedriveDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorPipedriveDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorPipedriveDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorPipedriveDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorPipedriveDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorPipedriveDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    access_token: str

    client_id: Optional[str] = None
    """Client ID used for the connection"""

    expires_at: Optional[str] = None

    expires_in: Optional[float] = None

    raw: Optional[Dict[str, object]] = None

    refresh_token: Optional[str] = None

    scope: Optional[str] = None

    token_type: Optional[str] = None


class ConnectorPipedriveDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    created_at: Optional[str] = None

    credentials: Optional[ConnectorPipedriveDiscriminatedConnectionSettingsSettingsOAuthCredentials] = None
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[str] = None


class ConnectorPipedriveDiscriminatedConnectionSettingsSettings(BaseModel):
    api_domain: str
    """The API URL of your Pipedrive account (e.g., example)"""

    oauth: ConnectorPipedriveDiscriminatedConnectionSettingsSettingsOAuth


class ConnectorPipedriveDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["pipedrive"]

    id: Optional[str] = None

    connector: Optional[ConnectorPipedriveDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorPipedriveDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorPipedriveDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorQuickbooksDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorQuickbooksDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorQuickbooksDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorQuickbooksDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorQuickbooksDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorQuickbooksDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorQuickbooksDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    access_token: str

    client_id: Optional[str] = None
    """Client ID used for the connection"""

    expires_at: Optional[str] = None

    expires_in: Optional[float] = None

    raw: Optional[Dict[str, object]] = None

    refresh_token: Optional[str] = None

    scope: Optional[str] = None

    token_type: Optional[str] = None


class ConnectorQuickbooksDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    created_at: Optional[str] = None

    credentials: Optional[ConnectorQuickbooksDiscriminatedConnectionSettingsSettingsOAuthCredentials] = None
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[str] = None


class ConnectorQuickbooksDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorQuickbooksDiscriminatedConnectionSettingsSettingsOAuth

    realm_id: str = FieldInfo(alias="realmId")
    """The realmId of your quickbooks company (e.g., 9341453474484455)"""


class ConnectorQuickbooksDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["quickbooks"]

    id: Optional[str] = None

    connector: Optional[ConnectorQuickbooksDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorQuickbooksDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorQuickbooksDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorRedditDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorRedditDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorRedditDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorRedditDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorRedditDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorRedditDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorRedditDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    access_token: str

    client_id: Optional[str] = None
    """Client ID used for the connection"""

    expires_at: Optional[str] = None

    expires_in: Optional[float] = None

    raw: Optional[Dict[str, object]] = None

    refresh_token: Optional[str] = None

    scope: Optional[str] = None

    token_type: Optional[str] = None


class ConnectorRedditDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    created_at: Optional[str] = None

    credentials: Optional[ConnectorRedditDiscriminatedConnectionSettingsSettingsOAuthCredentials] = None
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[str] = None


class ConnectorRedditDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorRedditDiscriminatedConnectionSettingsSettingsOAuth


class ConnectorRedditDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["reddit"]

    id: Optional[str] = None

    connector: Optional[ConnectorRedditDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorRedditDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorRedditDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorSalesloftDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorSalesloftDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorSalesloftDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorSalesloftDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorSalesloftDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorSalesloftDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorSalesloftDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    access_token: str

    client_id: Optional[str] = None
    """Client ID used for the connection"""

    expires_at: Optional[str] = None

    expires_in: Optional[float] = None

    raw: Optional[Dict[str, object]] = None

    refresh_token: Optional[str] = None

    scope: Optional[str] = None

    token_type: Optional[str] = None


class ConnectorSalesloftDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    created_at: Optional[str] = None

    credentials: Optional[ConnectorSalesloftDiscriminatedConnectionSettingsSettingsOAuthCredentials] = None
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[str] = None


class ConnectorSalesloftDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorSalesloftDiscriminatedConnectionSettingsSettingsOAuth


class ConnectorSalesloftDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["salesloft"]

    id: Optional[str] = None

    connector: Optional[ConnectorSalesloftDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorSalesloftDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorSalesloftDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorSharepointDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorSharepointDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorSharepointDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorSharepointDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorSharepointDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorSharepointDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorSharepointDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    access_token: str

    client_id: Optional[str] = None
    """Client ID used for the connection"""

    expires_at: Optional[str] = None

    expires_in: Optional[float] = None

    raw: Optional[Dict[str, object]] = None

    refresh_token: Optional[str] = None

    scope: Optional[str] = None

    token_type: Optional[str] = None


class ConnectorSharepointDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    created_at: Optional[str] = None

    credentials: Optional[ConnectorSharepointDiscriminatedConnectionSettingsSettingsOAuthCredentials] = None
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[str] = None


class ConnectorSharepointDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorSharepointDiscriminatedConnectionSettingsSettingsOAuth


class ConnectorSharepointDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["sharepoint"]

    id: Optional[str] = None

    connector: Optional[ConnectorSharepointDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorSharepointDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorSharepointDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorSlackDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorSlackDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorSlackDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorSlackDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorSlackDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorSlackDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorSlackDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    access_token: str

    client_id: Optional[str] = None
    """Client ID used for the connection"""

    expires_at: Optional[str] = None

    expires_in: Optional[float] = None

    raw: Optional[Dict[str, object]] = None

    refresh_token: Optional[str] = None

    scope: Optional[str] = None

    token_type: Optional[str] = None


class ConnectorSlackDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    created_at: Optional[str] = None

    credentials: Optional[ConnectorSlackDiscriminatedConnectionSettingsSettingsOAuthCredentials] = None
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[str] = None


class ConnectorSlackDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorSlackDiscriminatedConnectionSettingsSettingsOAuth


class ConnectorSlackDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["slack"]

    id: Optional[str] = None

    connector: Optional[ConnectorSlackDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorSlackDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorSlackDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorTwitterDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorTwitterDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorTwitterDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorTwitterDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorTwitterDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorTwitterDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorTwitterDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    access_token: str

    client_id: Optional[str] = None
    """Client ID used for the connection"""

    expires_at: Optional[str] = None

    expires_in: Optional[float] = None

    raw: Optional[Dict[str, object]] = None

    refresh_token: Optional[str] = None

    scope: Optional[str] = None

    token_type: Optional[str] = None


class ConnectorTwitterDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    created_at: Optional[str] = None

    credentials: Optional[ConnectorTwitterDiscriminatedConnectionSettingsSettingsOAuthCredentials] = None
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[str] = None


class ConnectorTwitterDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorTwitterDiscriminatedConnectionSettingsSettingsOAuth


class ConnectorTwitterDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["twitter"]

    id: Optional[str] = None

    connector: Optional[ConnectorTwitterDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorTwitterDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorTwitterDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorXeroDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorXeroDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorXeroDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorXeroDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorXeroDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorXeroDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorXeroDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    access_token: str

    client_id: Optional[str] = None
    """Client ID used for the connection"""

    expires_at: Optional[str] = None

    expires_in: Optional[float] = None

    raw: Optional[Dict[str, object]] = None

    refresh_token: Optional[str] = None

    scope: Optional[str] = None

    token_type: Optional[str] = None


class ConnectorXeroDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    created_at: Optional[str] = None

    credentials: Optional[ConnectorXeroDiscriminatedConnectionSettingsSettingsOAuthCredentials] = None
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[str] = None


class ConnectorXeroDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorXeroDiscriminatedConnectionSettingsSettingsOAuth


class ConnectorXeroDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["xero"]

    id: Optional[str] = None

    connector: Optional[ConnectorXeroDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorXeroDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorXeroDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorZohoDeskDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorZohoDeskDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorZohoDeskDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorZohoDeskDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorZohoDeskDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorZohoDeskDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorZohoDeskDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    access_token: str

    client_id: Optional[str] = None
    """Client ID used for the connection"""

    expires_at: Optional[str] = None

    expires_in: Optional[float] = None

    raw: Optional[Dict[str, object]] = None

    refresh_token: Optional[str] = None

    scope: Optional[str] = None

    token_type: Optional[str] = None


class ConnectorZohoDeskDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    created_at: Optional[str] = None

    credentials: Optional[ConnectorZohoDeskDiscriminatedConnectionSettingsSettingsOAuthCredentials] = None
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[str] = None


class ConnectorZohoDeskDiscriminatedConnectionSettingsSettings(BaseModel):
    extension: str
    """The domain extension of your Zoho account (e.g., https://accounts.zoho.com/)"""

    oauth: ConnectorZohoDeskDiscriminatedConnectionSettingsSettingsOAuth


class ConnectorZohoDeskDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["zoho-desk"]

    id: Optional[str] = None

    connector: Optional[ConnectorZohoDeskDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorZohoDeskDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorZohoDeskDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorAirtableDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorAirtableDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorAirtableDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorAirtableDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorAirtableDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorAirtableDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorAirtableDiscriminatedConnectionSettingsSettings(BaseModel):
    airtable_base: str = FieldInfo(alias="airtableBase")

    api_key: str = FieldInfo(alias="apiKey")


class ConnectorAirtableDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["airtable"]

    id: Optional[str] = None

    connector: Optional[ConnectorAirtableDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorAirtableDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorAirtableDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorApolloDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorApolloDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorApolloDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorApolloDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorApolloDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorApolloDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorApolloDiscriminatedConnectionSettingsSettings(BaseModel):
    api_key: str


class ConnectorApolloDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["apollo"]

    id: Optional[str] = None

    connector: Optional[ConnectorApolloDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorApolloDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorApolloDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorBrexDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorBrexDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorBrexDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorBrexDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorBrexDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorBrexDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorBrexDiscriminatedConnectionSettingsSettings(BaseModel):
    access_token: str = FieldInfo(alias="accessToken")


class ConnectorBrexDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["brex"]

    id: Optional[str] = None

    connector: Optional[ConnectorBrexDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorBrexDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorBrexDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorCodaDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorCodaDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorCodaDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorCodaDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorCodaDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorCodaDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorCodaDiscriminatedConnectionSettingsSettings(BaseModel):
    api_key: str = FieldInfo(alias="apiKey")


class ConnectorCodaDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["coda"]

    id: Optional[str] = None

    connector: Optional[ConnectorCodaDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorCodaDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorCodaDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorFinchDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorFinchDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorFinchDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorFinchDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorFinchDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorFinchDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorFinchDiscriminatedConnectionSettingsSettings(BaseModel):
    access_token: str


class ConnectorFinchDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["finch"]

    id: Optional[str] = None

    connector: Optional[ConnectorFinchDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorFinchDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorFinchDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorFirebaseDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorFirebaseDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorFirebaseDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorFirebaseDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorFirebaseDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorFirebaseDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember0ServiceAccount(BaseModel):
    project_id: str

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...


class ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember0(BaseModel):
    role: Literal["admin"]

    service_account: ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember0ServiceAccount = FieldInfo(
        alias="serviceAccount"
    )


class ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember0UserJson(BaseModel):
    app_name: str = FieldInfo(alias="appName")

    sts_token_manager: Dict[str, object] = FieldInfo(alias="stsTokenManager")

    uid: str

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...


class ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember0(BaseModel):
    method: Literal["userJson"]

    user_json: ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember0UserJson = (
        FieldInfo(alias="userJson")
    )


class ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember1(BaseModel):
    custom_token: str = FieldInfo(alias="customToken")

    method: Literal["customToken"]


class ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember2(BaseModel):
    email: str

    method: Literal["emailPassword"]

    password: str


ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthData: TypeAlias = Union[
    ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember0,
    ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember1,
    ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember2,
]


class ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1FirebaseConfig(BaseModel):
    api_key: str = FieldInfo(alias="apiKey")

    app_id: str = FieldInfo(alias="appId")

    auth_domain: str = FieldInfo(alias="authDomain")

    database_url: str = FieldInfo(alias="databaseURL")

    project_id: str = FieldInfo(alias="projectId")

    measurement_id: Optional[str] = FieldInfo(alias="measurementId", default=None)

    messaging_sender_id: Optional[str] = FieldInfo(alias="messagingSenderId", default=None)

    storage_bucket: Optional[str] = FieldInfo(alias="storageBucket", default=None)


class ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1(BaseModel):
    auth_data: ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthData = FieldInfo(
        alias="authData"
    )

    firebase_config: ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1FirebaseConfig = FieldInfo(
        alias="firebaseConfig"
    )

    role: Literal["user"]


ConnectorFirebaseDiscriminatedConnectionSettingsSettings: TypeAlias = Union[
    ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember0,
    ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1,
]


class ConnectorFirebaseDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["firebase"]

    id: Optional[str] = None

    connector: Optional[ConnectorFirebaseDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorFirebaseDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorFirebaseDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorForeceiptDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorForeceiptDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorForeceiptDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorForeceiptDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorForeceiptDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorForeceiptDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorForeceiptDiscriminatedConnectionSettingsSettings(BaseModel):
    env_name: Literal["staging", "production"] = FieldInfo(alias="envName")

    api_id: Optional[object] = FieldInfo(alias="_id", default=None)

    credentials: Optional[object] = None


class ConnectorForeceiptDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["foreceipt"]

    id: Optional[str] = None

    connector: Optional[ConnectorForeceiptDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorForeceiptDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorForeceiptDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorGreenhouseDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorGreenhouseDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorGreenhouseDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorGreenhouseDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorGreenhouseDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorGreenhouseDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorGreenhouseDiscriminatedConnectionSettingsSettings(BaseModel):
    api_key: str = FieldInfo(alias="apiKey")


class ConnectorGreenhouseDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["greenhouse"]

    id: Optional[str] = None

    connector: Optional[ConnectorGreenhouseDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorGreenhouseDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorGreenhouseDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorHeronDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorHeronDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorHeronDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorHeronDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorHeronDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorHeronDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorHeronDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["heron"]

    id: Optional[str] = None

    connector: Optional[ConnectorHeronDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorHeronDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[object] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorLunchmoneyDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorLunchmoneyDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorLunchmoneyDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorLunchmoneyDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorLunchmoneyDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorLunchmoneyDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorLunchmoneyDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["lunchmoney"]

    id: Optional[str] = None

    connector: Optional[ConnectorLunchmoneyDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorLunchmoneyDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[object] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorMercuryDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorMercuryDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorMercuryDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorMercuryDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorMercuryDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorMercuryDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorMercuryDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["mercury"]

    id: Optional[str] = None

    connector: Optional[ConnectorMercuryDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorMercuryDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[object] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorMergeDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorMergeDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorMergeDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorMergeDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorMergeDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorMergeDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorMergeDiscriminatedConnectionSettingsSettings(BaseModel):
    account_token: str = FieldInfo(alias="accountToken")

    account_details: Optional[object] = FieldInfo(alias="accountDetails", default=None)


class ConnectorMergeDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["merge"]

    id: Optional[str] = None

    connector: Optional[ConnectorMergeDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorMergeDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorMergeDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorMootaDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorMootaDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorMootaDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorMootaDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorMootaDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorMootaDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorMootaDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["moota"]

    id: Optional[str] = None

    connector: Optional[ConnectorMootaDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorMootaDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[object] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorOnebrickDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorOnebrickDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorOnebrickDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorOnebrickDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorOnebrickDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorOnebrickDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorOnebrickDiscriminatedConnectionSettingsSettings(BaseModel):
    access_token: str = FieldInfo(alias="accessToken")


class ConnectorOnebrickDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["onebrick"]

    id: Optional[str] = None

    connector: Optional[ConnectorOnebrickDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorOnebrickDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorOnebrickDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorPlaidDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorPlaidDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorPlaidDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorPlaidDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorPlaidDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorPlaidDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorPlaidDiscriminatedConnectionSettingsSettings(BaseModel):
    access_token: str = FieldInfo(alias="accessToken")

    institution: Optional[object] = None

    item: Optional[object] = None

    item_id: Optional[str] = FieldInfo(alias="itemId", default=None)

    status: Optional[object] = None

    webhook_item_error: None = FieldInfo(alias="webhookItemError", default=None)


class ConnectorPlaidDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["plaid"]

    id: Optional[str] = None

    connector: Optional[ConnectorPlaidDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorPlaidDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorPlaidDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorPostgresDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorPostgresDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorPostgresDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorPostgresDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorPostgresDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorPostgresDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorPostgresDiscriminatedConnectionSettingsSettings(BaseModel):
    database_url: Optional[str] = FieldInfo(alias="databaseURL", default=None)


class ConnectorPostgresDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["postgres"]

    id: Optional[str] = None

    connector: Optional[ConnectorPostgresDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorPostgresDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorPostgresDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorRampDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorRampDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorRampDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorRampDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorRampDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorRampDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorRampDiscriminatedConnectionSettingsSettings(BaseModel):
    access_token: Optional[str] = FieldInfo(alias="accessToken", default=None)

    start_after_transaction_id: Optional[str] = FieldInfo(alias="startAfterTransactionId", default=None)


class ConnectorRampDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["ramp"]

    id: Optional[str] = None

    connector: Optional[ConnectorRampDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorRampDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorRampDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorSaltedgeDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorSaltedgeDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorSaltedgeDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorSaltedgeDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorSaltedgeDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorSaltedgeDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorSaltedgeDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["saltedge"]

    id: Optional[str] = None

    connector: Optional[ConnectorSaltedgeDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorSaltedgeDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[object] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorSplitwiseDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorSplitwiseDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorSplitwiseDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorSplitwiseDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorSplitwiseDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorSplitwiseDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorSplitwiseDiscriminatedConnectionSettingsSettingsCurrentUserNotifications(BaseModel):
    added_as_friend: bool

    added_to_group: bool

    announcements: bool

    bills: bool

    expense_added: bool

    expense_updated: bool

    monthly_summary: bool

    payments: bool


class ConnectorSplitwiseDiscriminatedConnectionSettingsSettingsCurrentUserPicture(BaseModel):
    large: Optional[str] = None

    medium: Optional[str] = None

    original: Optional[str] = None

    small: Optional[str] = None

    xlarge: Optional[str] = None

    xxlarge: Optional[str] = None


class ConnectorSplitwiseDiscriminatedConnectionSettingsSettingsCurrentUser(BaseModel):
    id: float

    country_code: str

    custom_picture: bool

    date_format: str

    default_currency: str

    default_group_id: float

    email: str

    first_name: str

    force_refresh_at: str

    last_name: str

    locale: str

    notifications: ConnectorSplitwiseDiscriminatedConnectionSettingsSettingsCurrentUserNotifications

    notifications_count: float

    notifications_read: str

    picture: ConnectorSplitwiseDiscriminatedConnectionSettingsSettingsCurrentUserPicture

    registration_status: str


class ConnectorSplitwiseDiscriminatedConnectionSettingsSettings(BaseModel):
    access_token: str = FieldInfo(alias="accessToken")

    current_user: Optional[ConnectorSplitwiseDiscriminatedConnectionSettingsSettingsCurrentUser] = FieldInfo(
        alias="currentUser", default=None
    )


class ConnectorSplitwiseDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["splitwise"]

    id: Optional[str] = None

    connector: Optional[ConnectorSplitwiseDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorSplitwiseDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorSplitwiseDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorStripeDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorStripeDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorStripeDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorStripeDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorStripeDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorStripeDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorStripeDiscriminatedConnectionSettingsSettings(BaseModel):
    secret_key: str = FieldInfo(alias="secretKey")


class ConnectorStripeDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["stripe"]

    id: Optional[str] = None

    connector: Optional[ConnectorStripeDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorStripeDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorStripeDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorTellerDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorTellerDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorTellerDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorTellerDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorTellerDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorTellerDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorTellerDiscriminatedConnectionSettingsSettings(BaseModel):
    token: str


class ConnectorTellerDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["teller"]

    id: Optional[str] = None

    connector: Optional[ConnectorTellerDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorTellerDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorTellerDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorTogglDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorTogglDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorTogglDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorTogglDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorTogglDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorTogglDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorTogglDiscriminatedConnectionSettingsSettings(BaseModel):
    api_token: str = FieldInfo(alias="apiToken")

    email: Optional[str] = None

    password: Optional[str] = None


class ConnectorTogglDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["toggl"]

    id: Optional[str] = None

    connector: Optional[ConnectorTogglDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorTogglDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorTogglDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorTwentyDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorTwentyDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorTwentyDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorTwentyDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorTwentyDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorTwentyDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorTwentyDiscriminatedConnectionSettingsSettings(BaseModel):
    access_token: str


class ConnectorTwentyDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["twenty"]

    id: Optional[str] = None

    connector: Optional[ConnectorTwentyDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorTwentyDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorTwentyDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorVenmoDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorVenmoDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorVenmoDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorVenmoDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorVenmoDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorVenmoDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorVenmoDiscriminatedConnectionSettingsSettings(BaseModel):
    credentials: Optional[object] = None

    me: Optional[object] = None


class ConnectorVenmoDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["venmo"]

    id: Optional[str] = None

    connector: Optional[ConnectorVenmoDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorVenmoDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorVenmoDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorWiseDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorWiseDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorWiseDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorWiseDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorWiseDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorWiseDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorWiseDiscriminatedConnectionSettingsSettings(BaseModel):
    env_name: Literal["sandbox", "live"] = FieldInfo(alias="envName")

    api_token: Optional[str] = FieldInfo(alias="apiToken", default=None)


class ConnectorWiseDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["wise"]

    id: Optional[str] = None

    connector: Optional[ConnectorWiseDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorWiseDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorWiseDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorYodleeDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorYodleeDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorYodleeDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorYodleeDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorYodleeDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorYodleeDiscriminatedConnectionSettingsIntegration(BaseModel):
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


class ConnectorYodleeDiscriminatedConnectionSettingsSettingsAccessToken(BaseModel):
    access_token: str = FieldInfo(alias="accessToken")

    expires_in: float = FieldInfo(alias="expiresIn")

    issued_at: str = FieldInfo(alias="issuedAt")


class ConnectorYodleeDiscriminatedConnectionSettingsSettingsProviderAccount(BaseModel):
    id: float

    aggregation_source: str = FieldInfo(alias="aggregationSource")

    created_date: str = FieldInfo(alias="createdDate")

    dataset: List[object]

    is_manual: bool = FieldInfo(alias="isManual")

    provider_id: float = FieldInfo(alias="providerId")

    status: Literal["LOGIN_IN_PROGRESS", "USER_INPUT_REQUIRED", "IN_PROGRESS", "PARTIAL_SUCCESS", "SUCCESS", "FAILED"]

    is_deleted: Optional[bool] = FieldInfo(alias="isDeleted", default=None)


class ConnectorYodleeDiscriminatedConnectionSettingsSettings(BaseModel):
    login_name: str = FieldInfo(alias="loginName")

    provider_account_id: Union[float, str] = FieldInfo(alias="providerAccountId")

    access_token: Optional[ConnectorYodleeDiscriminatedConnectionSettingsSettingsAccessToken] = FieldInfo(
        alias="accessToken", default=None
    )

    provider: None = None

    provider_account: Optional[ConnectorYodleeDiscriminatedConnectionSettingsSettingsProviderAccount] = FieldInfo(
        alias="providerAccount", default=None
    )

    user: None = None


class ConnectorYodleeDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["yodlee"]

    id: Optional[str] = None

    connector: Optional[ConnectorYodleeDiscriminatedConnectionSettingsConnector] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration: Optional[ConnectorYodleeDiscriminatedConnectionSettingsIntegration] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[ConnectorYodleeDiscriminatedConnectionSettingsSettings] = None

    status: Optional[Literal["healthy", "disconnected", "error", "manual", "unknown"]] = None

    status_message: Optional[str] = None

    updated_at: Optional[str] = None


ListConnectionsResponse: TypeAlias = Union[
    ConnectorAcmeOauth2DiscriminatedConnectionSettings,
    ConnectorAircallDiscriminatedConnectionSettings,
    ConnectorConfluenceDiscriminatedConnectionSettings,
    ConnectorDiscordDiscriminatedConnectionSettings,
    ConnectorFacebookDiscriminatedConnectionSettings,
    ConnectorGitHubDiscriminatedConnectionSettings,
    ConnectorGongDiscriminatedConnectionSettings,
    ConnectorGoogleCalendarDiscriminatedConnectionSettings,
    ConnectorGoogleDocsDiscriminatedConnectionSettings,
    ConnectorGoogleDriveDiscriminatedConnectionSettings,
    ConnectorGoogleMailDiscriminatedConnectionSettings,
    ConnectorGoogleSheetDiscriminatedConnectionSettings,
    ConnectorHubspotDiscriminatedConnectionSettings,
    ConnectorInstagramDiscriminatedConnectionSettings,
    ConnectorIntercomDiscriminatedConnectionSettings,
    ConnectorJiraDiscriminatedConnectionSettings,
    ConnectorLeverDiscriminatedConnectionSettings,
    ConnectorLinearDiscriminatedConnectionSettings,
    ConnectorLinkedinDiscriminatedConnectionSettings,
    ConnectorNotionDiscriminatedConnectionSettings,
    ConnectorOutreachDiscriminatedConnectionSettings,
    ConnectorPipedriveDiscriminatedConnectionSettings,
    ConnectorQuickbooksDiscriminatedConnectionSettings,
    ConnectorRedditDiscriminatedConnectionSettings,
    ConnectorSalesloftDiscriminatedConnectionSettings,
    ConnectorSharepointDiscriminatedConnectionSettings,
    ConnectorSlackDiscriminatedConnectionSettings,
    ConnectorTwitterDiscriminatedConnectionSettings,
    ConnectorXeroDiscriminatedConnectionSettings,
    ConnectorZohoDeskDiscriminatedConnectionSettings,
    ConnectorAirtableDiscriminatedConnectionSettings,
    ConnectorApolloDiscriminatedConnectionSettings,
    ConnectorBrexDiscriminatedConnectionSettings,
    ConnectorCodaDiscriminatedConnectionSettings,
    ConnectorFinchDiscriminatedConnectionSettings,
    ConnectorFirebaseDiscriminatedConnectionSettings,
    ConnectorForeceiptDiscriminatedConnectionSettings,
    ConnectorGreenhouseDiscriminatedConnectionSettings,
    ConnectorHeronDiscriminatedConnectionSettings,
    ConnectorLunchmoneyDiscriminatedConnectionSettings,
    ConnectorMercuryDiscriminatedConnectionSettings,
    ConnectorMergeDiscriminatedConnectionSettings,
    ConnectorMootaDiscriminatedConnectionSettings,
    ConnectorOnebrickDiscriminatedConnectionSettings,
    ConnectorPlaidDiscriminatedConnectionSettings,
    ConnectorPostgresDiscriminatedConnectionSettings,
    ConnectorRampDiscriminatedConnectionSettings,
    ConnectorSaltedgeDiscriminatedConnectionSettings,
    ConnectorSplitwiseDiscriminatedConnectionSettings,
    ConnectorStripeDiscriminatedConnectionSettings,
    ConnectorTellerDiscriminatedConnectionSettings,
    ConnectorTogglDiscriminatedConnectionSettings,
    ConnectorTwentyDiscriminatedConnectionSettings,
    ConnectorVenmoDiscriminatedConnectionSettings,
    ConnectorWiseDiscriminatedConnectionSettings,
    ConnectorYodleeDiscriminatedConnectionSettings,
]
