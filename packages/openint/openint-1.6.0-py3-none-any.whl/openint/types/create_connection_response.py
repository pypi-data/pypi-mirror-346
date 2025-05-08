# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import TYPE_CHECKING, Dict, List, Union, Optional
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = [
    "CreateConnectionResponse",
    "ConnectorAcmeOauth2DiscriminatedConnectionSettings",
    "ConnectorAcmeOauth2DiscriminatedConnectionSettingsSettings",
    "ConnectorAcmeOauth2DiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorAcmeOauth2DiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorAircallDiscriminatedConnectionSettings",
    "ConnectorAircallDiscriminatedConnectionSettingsSettings",
    "ConnectorAircallDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorAircallDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorConfluenceDiscriminatedConnectionSettings",
    "ConnectorConfluenceDiscriminatedConnectionSettingsSettings",
    "ConnectorConfluenceDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorConfluenceDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorDiscordDiscriminatedConnectionSettings",
    "ConnectorDiscordDiscriminatedConnectionSettingsSettings",
    "ConnectorDiscordDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorDiscordDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorFacebookDiscriminatedConnectionSettings",
    "ConnectorFacebookDiscriminatedConnectionSettingsSettings",
    "ConnectorFacebookDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorFacebookDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorGitHubDiscriminatedConnectionSettings",
    "ConnectorGitHubDiscriminatedConnectionSettingsSettings",
    "ConnectorGitHubDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorGitHubDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorGongDiscriminatedConnectionSettings",
    "ConnectorGongDiscriminatedConnectionSettingsSettings",
    "ConnectorGongDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorGongDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorGoogleCalendarDiscriminatedConnectionSettings",
    "ConnectorGoogleCalendarDiscriminatedConnectionSettingsSettings",
    "ConnectorGoogleCalendarDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorGoogleCalendarDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorGoogleDocsDiscriminatedConnectionSettings",
    "ConnectorGoogleDocsDiscriminatedConnectionSettingsSettings",
    "ConnectorGoogleDocsDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorGoogleDocsDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorGoogleDriveDiscriminatedConnectionSettings",
    "ConnectorGoogleDriveDiscriminatedConnectionSettingsSettings",
    "ConnectorGoogleDriveDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorGoogleDriveDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorGoogleMailDiscriminatedConnectionSettings",
    "ConnectorGoogleMailDiscriminatedConnectionSettingsSettings",
    "ConnectorGoogleMailDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorGoogleMailDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorGoogleSheetDiscriminatedConnectionSettings",
    "ConnectorGoogleSheetDiscriminatedConnectionSettingsSettings",
    "ConnectorGoogleSheetDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorGoogleSheetDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorHubspotDiscriminatedConnectionSettings",
    "ConnectorHubspotDiscriminatedConnectionSettingsSettings",
    "ConnectorHubspotDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorHubspotDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorInstagramDiscriminatedConnectionSettings",
    "ConnectorInstagramDiscriminatedConnectionSettingsSettings",
    "ConnectorInstagramDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorInstagramDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorIntercomDiscriminatedConnectionSettings",
    "ConnectorIntercomDiscriminatedConnectionSettingsSettings",
    "ConnectorIntercomDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorIntercomDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorJiraDiscriminatedConnectionSettings",
    "ConnectorJiraDiscriminatedConnectionSettingsSettings",
    "ConnectorJiraDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorJiraDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorLeverDiscriminatedConnectionSettings",
    "ConnectorLeverDiscriminatedConnectionSettingsSettings",
    "ConnectorLeverDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorLeverDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorLinearDiscriminatedConnectionSettings",
    "ConnectorLinearDiscriminatedConnectionSettingsSettings",
    "ConnectorLinearDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorLinearDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorLinkedinDiscriminatedConnectionSettings",
    "ConnectorLinkedinDiscriminatedConnectionSettingsSettings",
    "ConnectorLinkedinDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorLinkedinDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorNotionDiscriminatedConnectionSettings",
    "ConnectorNotionDiscriminatedConnectionSettingsSettings",
    "ConnectorNotionDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorNotionDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorOutreachDiscriminatedConnectionSettings",
    "ConnectorOutreachDiscriminatedConnectionSettingsSettings",
    "ConnectorOutreachDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorOutreachDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorPipedriveDiscriminatedConnectionSettings",
    "ConnectorPipedriveDiscriminatedConnectionSettingsSettings",
    "ConnectorPipedriveDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorPipedriveDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorQuickbooksDiscriminatedConnectionSettings",
    "ConnectorQuickbooksDiscriminatedConnectionSettingsSettings",
    "ConnectorQuickbooksDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorQuickbooksDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorRedditDiscriminatedConnectionSettings",
    "ConnectorRedditDiscriminatedConnectionSettingsSettings",
    "ConnectorRedditDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorRedditDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorSalesloftDiscriminatedConnectionSettings",
    "ConnectorSalesloftDiscriminatedConnectionSettingsSettings",
    "ConnectorSalesloftDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorSalesloftDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorSharepointDiscriminatedConnectionSettings",
    "ConnectorSharepointDiscriminatedConnectionSettingsSettings",
    "ConnectorSharepointDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorSharepointDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorSlackDiscriminatedConnectionSettings",
    "ConnectorSlackDiscriminatedConnectionSettingsSettings",
    "ConnectorSlackDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorSlackDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorTwitterDiscriminatedConnectionSettings",
    "ConnectorTwitterDiscriminatedConnectionSettingsSettings",
    "ConnectorTwitterDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorTwitterDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorXeroDiscriminatedConnectionSettings",
    "ConnectorXeroDiscriminatedConnectionSettingsSettings",
    "ConnectorXeroDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorXeroDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorZohoDeskDiscriminatedConnectionSettings",
    "ConnectorZohoDeskDiscriminatedConnectionSettingsSettings",
    "ConnectorZohoDeskDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorZohoDeskDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorAirtableDiscriminatedConnectionSettings",
    "ConnectorAirtableDiscriminatedConnectionSettingsSettings",
    "ConnectorApolloDiscriminatedConnectionSettings",
    "ConnectorApolloDiscriminatedConnectionSettingsSettings",
    "ConnectorBrexDiscriminatedConnectionSettings",
    "ConnectorBrexDiscriminatedConnectionSettingsSettings",
    "ConnectorCodaDiscriminatedConnectionSettings",
    "ConnectorCodaDiscriminatedConnectionSettingsSettings",
    "ConnectorFinchDiscriminatedConnectionSettings",
    "ConnectorFinchDiscriminatedConnectionSettingsSettings",
    "ConnectorFirebaseDiscriminatedConnectionSettings",
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
    "ConnectorForeceiptDiscriminatedConnectionSettingsSettings",
    "ConnectorGreenhouseDiscriminatedConnectionSettings",
    "ConnectorGreenhouseDiscriminatedConnectionSettingsSettings",
    "ConnectorHeronDiscriminatedConnectionSettings",
    "ConnectorLunchmoneyDiscriminatedConnectionSettings",
    "ConnectorMercuryDiscriminatedConnectionSettings",
    "ConnectorMergeDiscriminatedConnectionSettings",
    "ConnectorMergeDiscriminatedConnectionSettingsSettings",
    "ConnectorMootaDiscriminatedConnectionSettings",
    "ConnectorOnebrickDiscriminatedConnectionSettings",
    "ConnectorOnebrickDiscriminatedConnectionSettingsSettings",
    "ConnectorPlaidDiscriminatedConnectionSettings",
    "ConnectorPlaidDiscriminatedConnectionSettingsSettings",
    "ConnectorPostgresDiscriminatedConnectionSettings",
    "ConnectorPostgresDiscriminatedConnectionSettingsSettings",
    "ConnectorRampDiscriminatedConnectionSettings",
    "ConnectorRampDiscriminatedConnectionSettingsSettings",
    "ConnectorSaltedgeDiscriminatedConnectionSettings",
    "ConnectorSplitwiseDiscriminatedConnectionSettings",
    "ConnectorSplitwiseDiscriminatedConnectionSettingsSettings",
    "ConnectorSplitwiseDiscriminatedConnectionSettingsSettingsCurrentUser",
    "ConnectorSplitwiseDiscriminatedConnectionSettingsSettingsCurrentUserNotifications",
    "ConnectorSplitwiseDiscriminatedConnectionSettingsSettingsCurrentUserPicture",
    "ConnectorStripeDiscriminatedConnectionSettings",
    "ConnectorStripeDiscriminatedConnectionSettingsSettings",
    "ConnectorTellerDiscriminatedConnectionSettings",
    "ConnectorTellerDiscriminatedConnectionSettingsSettings",
    "ConnectorTogglDiscriminatedConnectionSettings",
    "ConnectorTogglDiscriminatedConnectionSettingsSettings",
    "ConnectorTwentyDiscriminatedConnectionSettings",
    "ConnectorTwentyDiscriminatedConnectionSettingsSettings",
    "ConnectorVenmoDiscriminatedConnectionSettings",
    "ConnectorVenmoDiscriminatedConnectionSettingsSettings",
    "ConnectorWiseDiscriminatedConnectionSettings",
    "ConnectorWiseDiscriminatedConnectionSettingsSettings",
    "ConnectorYodleeDiscriminatedConnectionSettings",
    "ConnectorYodleeDiscriminatedConnectionSettingsSettings",
    "ConnectorYodleeDiscriminatedConnectionSettingsSettingsAccessToken",
    "ConnectorYodleeDiscriminatedConnectionSettingsSettingsProviderAccount",
]


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

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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


class ConnectorAirtableDiscriminatedConnectionSettingsSettings(BaseModel):
    airtable_base: str = FieldInfo(alias="airtableBase")

    api_key: str = FieldInfo(alias="apiKey")


class ConnectorAirtableDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["airtable"]

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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


class ConnectorApolloDiscriminatedConnectionSettingsSettings(BaseModel):
    api_key: str


class ConnectorApolloDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["apollo"]

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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


class ConnectorBrexDiscriminatedConnectionSettingsSettings(BaseModel):
    access_token: str = FieldInfo(alias="accessToken")


class ConnectorBrexDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["brex"]

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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


class ConnectorCodaDiscriminatedConnectionSettingsSettings(BaseModel):
    api_key: str = FieldInfo(alias="apiKey")


class ConnectorCodaDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["coda"]

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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


class ConnectorFinchDiscriminatedConnectionSettingsSettings(BaseModel):
    access_token: str


class ConnectorFinchDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["finch"]

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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


class ConnectorForeceiptDiscriminatedConnectionSettingsSettings(BaseModel):
    env_name: Literal["staging", "production"] = FieldInfo(alias="envName")

    api_id: Optional[object] = FieldInfo(alias="_id", default=None)

    credentials: Optional[object] = None


class ConnectorForeceiptDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["foreceipt"]

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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


class ConnectorGreenhouseDiscriminatedConnectionSettingsSettings(BaseModel):
    api_key: str = FieldInfo(alias="apiKey")


class ConnectorGreenhouseDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["greenhouse"]

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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


class ConnectorHeronDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["heron"]

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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


class ConnectorLunchmoneyDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["lunchmoney"]

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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


class ConnectorMercuryDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["mercury"]

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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


class ConnectorMergeDiscriminatedConnectionSettingsSettings(BaseModel):
    account_token: str = FieldInfo(alias="accountToken")

    account_details: Optional[object] = FieldInfo(alias="accountDetails", default=None)


class ConnectorMergeDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["merge"]

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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


class ConnectorMootaDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["moota"]

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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


class ConnectorOnebrickDiscriminatedConnectionSettingsSettings(BaseModel):
    access_token: str = FieldInfo(alias="accessToken")


class ConnectorOnebrickDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["onebrick"]

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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


class ConnectorPostgresDiscriminatedConnectionSettingsSettings(BaseModel):
    database_url: Optional[str] = FieldInfo(alias="databaseURL", default=None)


class ConnectorPostgresDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["postgres"]

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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


class ConnectorRampDiscriminatedConnectionSettingsSettings(BaseModel):
    access_token: Optional[str] = FieldInfo(alias="accessToken", default=None)

    start_after_transaction_id: Optional[str] = FieldInfo(alias="startAfterTransactionId", default=None)


class ConnectorRampDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["ramp"]

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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


class ConnectorSaltedgeDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["saltedge"]

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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


class ConnectorStripeDiscriminatedConnectionSettingsSettings(BaseModel):
    secret_key: str = FieldInfo(alias="secretKey")


class ConnectorStripeDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["stripe"]

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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


class ConnectorTellerDiscriminatedConnectionSettingsSettings(BaseModel):
    token: str


class ConnectorTellerDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["teller"]

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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


class ConnectorTogglDiscriminatedConnectionSettingsSettings(BaseModel):
    api_token: str = FieldInfo(alias="apiToken")

    email: Optional[str] = None

    password: Optional[str] = None


class ConnectorTogglDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["toggl"]

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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


class ConnectorTwentyDiscriminatedConnectionSettingsSettings(BaseModel):
    access_token: str


class ConnectorTwentyDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["twenty"]

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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


class ConnectorVenmoDiscriminatedConnectionSettingsSettings(BaseModel):
    credentials: Optional[object] = None

    me: Optional[object] = None


class ConnectorVenmoDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["venmo"]

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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


class ConnectorWiseDiscriminatedConnectionSettingsSettings(BaseModel):
    env_name: Literal["sandbox", "live"] = FieldInfo(alias="envName")

    api_token: Optional[str] = FieldInfo(alias="apiToken", default=None)


class ConnectorWiseDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["wise"]

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

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


CreateConnectionResponse: TypeAlias = Union[
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
