# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable, Optional
from typing_extensions import Literal, Required, Annotated, TypeAlias, TypedDict

from .._utils import PropertyInfo

__all__ = [
    "ClientCreateConnectionParams",
    "Data",
    "DataConnectorAcmeOauth2DiscriminatedConnectionSettings",
    "DataConnectorAcmeOauth2DiscriminatedConnectionSettingsSettings",
    "DataConnectorAcmeOauth2DiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorAcmeOauth2DiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorAircallDiscriminatedConnectionSettings",
    "DataConnectorAircallDiscriminatedConnectionSettingsSettings",
    "DataConnectorAircallDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorAircallDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorConfluenceDiscriminatedConnectionSettings",
    "DataConnectorConfluenceDiscriminatedConnectionSettingsSettings",
    "DataConnectorConfluenceDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorConfluenceDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorDiscordDiscriminatedConnectionSettings",
    "DataConnectorDiscordDiscriminatedConnectionSettingsSettings",
    "DataConnectorDiscordDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorDiscordDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorFacebookDiscriminatedConnectionSettings",
    "DataConnectorFacebookDiscriminatedConnectionSettingsSettings",
    "DataConnectorFacebookDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorFacebookDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorGitHubDiscriminatedConnectionSettings",
    "DataConnectorGitHubDiscriminatedConnectionSettingsSettings",
    "DataConnectorGitHubDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorGitHubDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorGongDiscriminatedConnectionSettings",
    "DataConnectorGongDiscriminatedConnectionSettingsSettings",
    "DataConnectorGongDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorGongDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorGoogleCalendarDiscriminatedConnectionSettings",
    "DataConnectorGoogleCalendarDiscriminatedConnectionSettingsSettings",
    "DataConnectorGoogleCalendarDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorGoogleCalendarDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorGoogleDocsDiscriminatedConnectionSettings",
    "DataConnectorGoogleDocsDiscriminatedConnectionSettingsSettings",
    "DataConnectorGoogleDocsDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorGoogleDocsDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorGoogleDriveDiscriminatedConnectionSettings",
    "DataConnectorGoogleDriveDiscriminatedConnectionSettingsSettings",
    "DataConnectorGoogleDriveDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorGoogleDriveDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorGoogleMailDiscriminatedConnectionSettings",
    "DataConnectorGoogleMailDiscriminatedConnectionSettingsSettings",
    "DataConnectorGoogleMailDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorGoogleMailDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorGoogleSheetDiscriminatedConnectionSettings",
    "DataConnectorGoogleSheetDiscriminatedConnectionSettingsSettings",
    "DataConnectorGoogleSheetDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorGoogleSheetDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorHubspotDiscriminatedConnectionSettings",
    "DataConnectorHubspotDiscriminatedConnectionSettingsSettings",
    "DataConnectorHubspotDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorHubspotDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorInstagramDiscriminatedConnectionSettings",
    "DataConnectorInstagramDiscriminatedConnectionSettingsSettings",
    "DataConnectorInstagramDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorInstagramDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorIntercomDiscriminatedConnectionSettings",
    "DataConnectorIntercomDiscriminatedConnectionSettingsSettings",
    "DataConnectorIntercomDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorIntercomDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorJiraDiscriminatedConnectionSettings",
    "DataConnectorJiraDiscriminatedConnectionSettingsSettings",
    "DataConnectorJiraDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorJiraDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorLeverDiscriminatedConnectionSettings",
    "DataConnectorLeverDiscriminatedConnectionSettingsSettings",
    "DataConnectorLeverDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorLeverDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorLinearDiscriminatedConnectionSettings",
    "DataConnectorLinearDiscriminatedConnectionSettingsSettings",
    "DataConnectorLinearDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorLinearDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorLinkedinDiscriminatedConnectionSettings",
    "DataConnectorLinkedinDiscriminatedConnectionSettingsSettings",
    "DataConnectorLinkedinDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorLinkedinDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorNotionDiscriminatedConnectionSettings",
    "DataConnectorNotionDiscriminatedConnectionSettingsSettings",
    "DataConnectorNotionDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorNotionDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorOutreachDiscriminatedConnectionSettings",
    "DataConnectorOutreachDiscriminatedConnectionSettingsSettings",
    "DataConnectorOutreachDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorOutreachDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorPipedriveDiscriminatedConnectionSettings",
    "DataConnectorPipedriveDiscriminatedConnectionSettingsSettings",
    "DataConnectorPipedriveDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorPipedriveDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorQuickbooksDiscriminatedConnectionSettings",
    "DataConnectorQuickbooksDiscriminatedConnectionSettingsSettings",
    "DataConnectorQuickbooksDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorQuickbooksDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorRedditDiscriminatedConnectionSettings",
    "DataConnectorRedditDiscriminatedConnectionSettingsSettings",
    "DataConnectorRedditDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorRedditDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorSalesloftDiscriminatedConnectionSettings",
    "DataConnectorSalesloftDiscriminatedConnectionSettingsSettings",
    "DataConnectorSalesloftDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorSalesloftDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorSharepointDiscriminatedConnectionSettings",
    "DataConnectorSharepointDiscriminatedConnectionSettingsSettings",
    "DataConnectorSharepointDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorSharepointDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorSlackDiscriminatedConnectionSettings",
    "DataConnectorSlackDiscriminatedConnectionSettingsSettings",
    "DataConnectorSlackDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorSlackDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorTwitterDiscriminatedConnectionSettings",
    "DataConnectorTwitterDiscriminatedConnectionSettingsSettings",
    "DataConnectorTwitterDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorTwitterDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorXeroDiscriminatedConnectionSettings",
    "DataConnectorXeroDiscriminatedConnectionSettingsSettings",
    "DataConnectorXeroDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorXeroDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorZohoDeskDiscriminatedConnectionSettings",
    "DataConnectorZohoDeskDiscriminatedConnectionSettingsSettings",
    "DataConnectorZohoDeskDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorZohoDeskDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorAirtableDiscriminatedConnectionSettings",
    "DataConnectorAirtableDiscriminatedConnectionSettingsSettings",
    "DataConnectorApolloDiscriminatedConnectionSettings",
    "DataConnectorApolloDiscriminatedConnectionSettingsSettings",
    "DataConnectorBrexDiscriminatedConnectionSettings",
    "DataConnectorBrexDiscriminatedConnectionSettingsSettings",
    "DataConnectorCodaDiscriminatedConnectionSettings",
    "DataConnectorCodaDiscriminatedConnectionSettingsSettings",
    "DataConnectorFinchDiscriminatedConnectionSettings",
    "DataConnectorFinchDiscriminatedConnectionSettingsSettings",
    "DataConnectorFirebaseDiscriminatedConnectionSettings",
    "DataConnectorFirebaseDiscriminatedConnectionSettingsSettings",
    "DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember0",
    "DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember0ServiceAccount",
    "DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1",
    "DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthData",
    "DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember0",
    "DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember0UserJson",
    "DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember1",
    "DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember2",
    "DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1FirebaseConfig",
    "DataConnectorForeceiptDiscriminatedConnectionSettings",
    "DataConnectorForeceiptDiscriminatedConnectionSettingsSettings",
    "DataConnectorGreenhouseDiscriminatedConnectionSettings",
    "DataConnectorGreenhouseDiscriminatedConnectionSettingsSettings",
    "DataConnectorHeronDiscriminatedConnectionSettings",
    "DataConnectorLunchmoneyDiscriminatedConnectionSettings",
    "DataConnectorMercuryDiscriminatedConnectionSettings",
    "DataConnectorMergeDiscriminatedConnectionSettings",
    "DataConnectorMergeDiscriminatedConnectionSettingsSettings",
    "DataConnectorMootaDiscriminatedConnectionSettings",
    "DataConnectorOnebrickDiscriminatedConnectionSettings",
    "DataConnectorOnebrickDiscriminatedConnectionSettingsSettings",
    "DataConnectorPlaidDiscriminatedConnectionSettings",
    "DataConnectorPlaidDiscriminatedConnectionSettingsSettings",
    "DataConnectorPostgresDiscriminatedConnectionSettings",
    "DataConnectorPostgresDiscriminatedConnectionSettingsSettings",
    "DataConnectorRampDiscriminatedConnectionSettings",
    "DataConnectorRampDiscriminatedConnectionSettingsSettings",
    "DataConnectorSaltedgeDiscriminatedConnectionSettings",
    "DataConnectorSplitwiseDiscriminatedConnectionSettings",
    "DataConnectorSplitwiseDiscriminatedConnectionSettingsSettings",
    "DataConnectorSplitwiseDiscriminatedConnectionSettingsSettingsCurrentUser",
    "DataConnectorSplitwiseDiscriminatedConnectionSettingsSettingsCurrentUserNotifications",
    "DataConnectorSplitwiseDiscriminatedConnectionSettingsSettingsCurrentUserPicture",
    "DataConnectorStripeDiscriminatedConnectionSettings",
    "DataConnectorStripeDiscriminatedConnectionSettingsSettings",
    "DataConnectorTellerDiscriminatedConnectionSettings",
    "DataConnectorTellerDiscriminatedConnectionSettingsSettings",
    "DataConnectorTogglDiscriminatedConnectionSettings",
    "DataConnectorTogglDiscriminatedConnectionSettingsSettings",
    "DataConnectorTwentyDiscriminatedConnectionSettings",
    "DataConnectorTwentyDiscriminatedConnectionSettingsSettings",
    "DataConnectorVenmoDiscriminatedConnectionSettings",
    "DataConnectorVenmoDiscriminatedConnectionSettingsSettings",
    "DataConnectorWiseDiscriminatedConnectionSettings",
    "DataConnectorWiseDiscriminatedConnectionSettingsSettings",
    "DataConnectorYodleeDiscriminatedConnectionSettings",
    "DataConnectorYodleeDiscriminatedConnectionSettingsSettings",
    "DataConnectorYodleeDiscriminatedConnectionSettingsSettingsAccessToken",
    "DataConnectorYodleeDiscriminatedConnectionSettingsSettingsProviderAccount",
]


class ClientCreateConnectionParams(TypedDict, total=False):
    connector_config_id: Required[str]
    """The id of the connector config, starts with `ccfg_`"""

    customer_id: Required[str]
    """The id of the customer in your application.

    Ensure it is unique for that customer.
    """

    data: Required[Data]
    """Connector specific data"""

    check_connection: bool
    """Perform a synchronous connection check before creating it."""

    metadata: Dict[str, object]


class DataConnectorAcmeOauth2DiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    access_token: Required[str]

    client_id: str
    """Client ID used for the connection"""

    expires_at: str

    expires_in: float

    raw: Dict[str, object]

    refresh_token: str

    scope: str

    token_type: str


class DataConnectorAcmeOauth2DiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    created_at: str

    credentials: DataConnectorAcmeOauth2DiscriminatedConnectionSettingsSettingsOAuthCredentials
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: str

    metadata: Optional[Dict[str, object]]

    updated_at: str


class DataConnectorAcmeOauth2DiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorAcmeOauth2DiscriminatedConnectionSettingsSettingsOAuth]


class DataConnectorAcmeOauth2DiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["acme-oauth2"]]

    settings: DataConnectorAcmeOauth2DiscriminatedConnectionSettingsSettings


class DataConnectorAircallDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    access_token: Required[str]

    client_id: str
    """Client ID used for the connection"""

    expires_at: str

    expires_in: float

    raw: Dict[str, object]

    refresh_token: str

    scope: str

    token_type: str


class DataConnectorAircallDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    created_at: str

    credentials: DataConnectorAircallDiscriminatedConnectionSettingsSettingsOAuthCredentials
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: str

    metadata: Optional[Dict[str, object]]

    updated_at: str


class DataConnectorAircallDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorAircallDiscriminatedConnectionSettingsSettingsOAuth]


class DataConnectorAircallDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["aircall"]]

    settings: DataConnectorAircallDiscriminatedConnectionSettingsSettings


class DataConnectorConfluenceDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    access_token: Required[str]

    client_id: str
    """Client ID used for the connection"""

    expires_at: str

    expires_in: float

    raw: Dict[str, object]

    refresh_token: str

    scope: str

    token_type: str


class DataConnectorConfluenceDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    created_at: str

    credentials: DataConnectorConfluenceDiscriminatedConnectionSettingsSettingsOAuthCredentials
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: str

    metadata: Optional[Dict[str, object]]

    updated_at: str


class DataConnectorConfluenceDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorConfluenceDiscriminatedConnectionSettingsSettingsOAuth]


class DataConnectorConfluenceDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["confluence"]]

    settings: DataConnectorConfluenceDiscriminatedConnectionSettingsSettings


class DataConnectorDiscordDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    access_token: Required[str]

    client_id: str
    """Client ID used for the connection"""

    expires_at: str

    expires_in: float

    raw: Dict[str, object]

    refresh_token: str

    scope: str

    token_type: str


class DataConnectorDiscordDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    created_at: str

    credentials: DataConnectorDiscordDiscriminatedConnectionSettingsSettingsOAuthCredentials
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: str

    metadata: Optional[Dict[str, object]]

    updated_at: str


class DataConnectorDiscordDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorDiscordDiscriminatedConnectionSettingsSettingsOAuth]


class DataConnectorDiscordDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["discord"]]

    settings: DataConnectorDiscordDiscriminatedConnectionSettingsSettings


class DataConnectorFacebookDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    access_token: Required[str]

    client_id: str
    """Client ID used for the connection"""

    expires_at: str

    expires_in: float

    raw: Dict[str, object]

    refresh_token: str

    scope: str

    token_type: str


class DataConnectorFacebookDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    created_at: str

    credentials: DataConnectorFacebookDiscriminatedConnectionSettingsSettingsOAuthCredentials
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: str

    metadata: Optional[Dict[str, object]]

    updated_at: str


class DataConnectorFacebookDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorFacebookDiscriminatedConnectionSettingsSettingsOAuth]


class DataConnectorFacebookDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["facebook"]]

    settings: DataConnectorFacebookDiscriminatedConnectionSettingsSettings


class DataConnectorGitHubDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    access_token: Required[str]

    client_id: str
    """Client ID used for the connection"""

    expires_at: str

    expires_in: float

    raw: Dict[str, object]

    refresh_token: str

    scope: str

    token_type: str


class DataConnectorGitHubDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    created_at: str

    credentials: DataConnectorGitHubDiscriminatedConnectionSettingsSettingsOAuthCredentials
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: str

    metadata: Optional[Dict[str, object]]

    updated_at: str


class DataConnectorGitHubDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorGitHubDiscriminatedConnectionSettingsSettingsOAuth]


class DataConnectorGitHubDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["github"]]

    settings: DataConnectorGitHubDiscriminatedConnectionSettingsSettings


class DataConnectorGongDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    access_token: Required[str]

    client_id: str
    """Client ID used for the connection"""

    expires_at: str

    expires_in: float

    raw: Dict[str, object]

    refresh_token: str

    scope: str

    token_type: str


class DataConnectorGongDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    created_at: str

    credentials: DataConnectorGongDiscriminatedConnectionSettingsSettingsOAuthCredentials
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: str

    metadata: Optional[Dict[str, object]]

    updated_at: str


class DataConnectorGongDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    api_base_url_for_customer: Required[str]
    """The base URL of your Gong account (e.g., example)"""

    oauth: Required[DataConnectorGongDiscriminatedConnectionSettingsSettingsOAuth]


class DataConnectorGongDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["gong"]]

    settings: DataConnectorGongDiscriminatedConnectionSettingsSettings


class DataConnectorGoogleCalendarDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    access_token: Required[str]

    client_id: str
    """Client ID used for the connection"""

    expires_at: str

    expires_in: float

    raw: Dict[str, object]

    refresh_token: str

    scope: str

    token_type: str


class DataConnectorGoogleCalendarDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    created_at: str

    credentials: DataConnectorGoogleCalendarDiscriminatedConnectionSettingsSettingsOAuthCredentials
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: str

    metadata: Optional[Dict[str, object]]

    updated_at: str


class DataConnectorGoogleCalendarDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorGoogleCalendarDiscriminatedConnectionSettingsSettingsOAuth]


class DataConnectorGoogleCalendarDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["google-calendar"]]

    settings: DataConnectorGoogleCalendarDiscriminatedConnectionSettingsSettings


class DataConnectorGoogleDocsDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    access_token: Required[str]

    client_id: str
    """Client ID used for the connection"""

    expires_at: str

    expires_in: float

    raw: Dict[str, object]

    refresh_token: str

    scope: str

    token_type: str


class DataConnectorGoogleDocsDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    created_at: str

    credentials: DataConnectorGoogleDocsDiscriminatedConnectionSettingsSettingsOAuthCredentials
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: str

    metadata: Optional[Dict[str, object]]

    updated_at: str


class DataConnectorGoogleDocsDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorGoogleDocsDiscriminatedConnectionSettingsSettingsOAuth]


class DataConnectorGoogleDocsDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["google-docs"]]

    settings: DataConnectorGoogleDocsDiscriminatedConnectionSettingsSettings


class DataConnectorGoogleDriveDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    access_token: Required[str]

    client_id: str
    """Client ID used for the connection"""

    expires_at: str

    expires_in: float

    raw: Dict[str, object]

    refresh_token: str

    scope: str

    token_type: str


class DataConnectorGoogleDriveDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    created_at: str

    credentials: DataConnectorGoogleDriveDiscriminatedConnectionSettingsSettingsOAuthCredentials
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: str

    metadata: Optional[Dict[str, object]]

    updated_at: str


class DataConnectorGoogleDriveDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorGoogleDriveDiscriminatedConnectionSettingsSettingsOAuth]


class DataConnectorGoogleDriveDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["google-drive"]]

    settings: DataConnectorGoogleDriveDiscriminatedConnectionSettingsSettings


class DataConnectorGoogleMailDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    access_token: Required[str]

    client_id: str
    """Client ID used for the connection"""

    expires_at: str

    expires_in: float

    raw: Dict[str, object]

    refresh_token: str

    scope: str

    token_type: str


class DataConnectorGoogleMailDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    created_at: str

    credentials: DataConnectorGoogleMailDiscriminatedConnectionSettingsSettingsOAuthCredentials
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: str

    metadata: Optional[Dict[str, object]]

    updated_at: str


class DataConnectorGoogleMailDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorGoogleMailDiscriminatedConnectionSettingsSettingsOAuth]


class DataConnectorGoogleMailDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["google-mail"]]

    settings: DataConnectorGoogleMailDiscriminatedConnectionSettingsSettings


class DataConnectorGoogleSheetDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    access_token: Required[str]

    client_id: str
    """Client ID used for the connection"""

    expires_at: str

    expires_in: float

    raw: Dict[str, object]

    refresh_token: str

    scope: str

    token_type: str


class DataConnectorGoogleSheetDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    created_at: str

    credentials: DataConnectorGoogleSheetDiscriminatedConnectionSettingsSettingsOAuthCredentials
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: str

    metadata: Optional[Dict[str, object]]

    updated_at: str


class DataConnectorGoogleSheetDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorGoogleSheetDiscriminatedConnectionSettingsSettingsOAuth]


class DataConnectorGoogleSheetDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["google-sheet"]]

    settings: DataConnectorGoogleSheetDiscriminatedConnectionSettingsSettings


class DataConnectorHubspotDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    access_token: Required[str]

    client_id: str
    """Client ID used for the connection"""

    expires_at: str

    expires_in: float

    raw: Dict[str, object]

    refresh_token: str

    scope: str

    token_type: str


class DataConnectorHubspotDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    created_at: str

    credentials: DataConnectorHubspotDiscriminatedConnectionSettingsSettingsOAuthCredentials
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: str

    metadata: Optional[Dict[str, object]]

    updated_at: str


class DataConnectorHubspotDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorHubspotDiscriminatedConnectionSettingsSettingsOAuth]


class DataConnectorHubspotDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["hubspot"]]

    settings: DataConnectorHubspotDiscriminatedConnectionSettingsSettings


class DataConnectorInstagramDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    access_token: Required[str]

    client_id: str
    """Client ID used for the connection"""

    expires_at: str

    expires_in: float

    raw: Dict[str, object]

    refresh_token: str

    scope: str

    token_type: str


class DataConnectorInstagramDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    created_at: str

    credentials: DataConnectorInstagramDiscriminatedConnectionSettingsSettingsOAuthCredentials
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: str

    metadata: Optional[Dict[str, object]]

    updated_at: str


class DataConnectorInstagramDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorInstagramDiscriminatedConnectionSettingsSettingsOAuth]


class DataConnectorInstagramDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["instagram"]]

    settings: DataConnectorInstagramDiscriminatedConnectionSettingsSettings


class DataConnectorIntercomDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    access_token: Required[str]

    client_id: str
    """Client ID used for the connection"""

    expires_at: str

    expires_in: float

    raw: Dict[str, object]

    refresh_token: str

    scope: str

    token_type: str


class DataConnectorIntercomDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    created_at: str

    credentials: DataConnectorIntercomDiscriminatedConnectionSettingsSettingsOAuthCredentials
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: str

    metadata: Optional[Dict[str, object]]

    updated_at: str


class DataConnectorIntercomDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorIntercomDiscriminatedConnectionSettingsSettingsOAuth]


class DataConnectorIntercomDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["intercom"]]

    settings: DataConnectorIntercomDiscriminatedConnectionSettingsSettings


class DataConnectorJiraDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    access_token: Required[str]

    client_id: str
    """Client ID used for the connection"""

    expires_at: str

    expires_in: float

    raw: Dict[str, object]

    refresh_token: str

    scope: str

    token_type: str


class DataConnectorJiraDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    created_at: str

    credentials: DataConnectorJiraDiscriminatedConnectionSettingsSettingsOAuthCredentials
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: str

    metadata: Optional[Dict[str, object]]

    updated_at: str


class DataConnectorJiraDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorJiraDiscriminatedConnectionSettingsSettingsOAuth]


class DataConnectorJiraDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["jira"]]

    settings: DataConnectorJiraDiscriminatedConnectionSettingsSettings


class DataConnectorLeverDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    access_token: Required[str]

    client_id: str
    """Client ID used for the connection"""

    expires_at: str

    expires_in: float

    raw: Dict[str, object]

    refresh_token: str

    scope: str

    token_type: str


class DataConnectorLeverDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    created_at: str

    credentials: DataConnectorLeverDiscriminatedConnectionSettingsSettingsOAuthCredentials
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: str

    metadata: Optional[Dict[str, object]]

    updated_at: str


class DataConnectorLeverDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorLeverDiscriminatedConnectionSettingsSettingsOAuth]


class DataConnectorLeverDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["lever"]]

    settings: DataConnectorLeverDiscriminatedConnectionSettingsSettings


class DataConnectorLinearDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    access_token: Required[str]

    client_id: str
    """Client ID used for the connection"""

    expires_at: str

    expires_in: float

    raw: Dict[str, object]

    refresh_token: str

    scope: str

    token_type: str


class DataConnectorLinearDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    created_at: str

    credentials: DataConnectorLinearDiscriminatedConnectionSettingsSettingsOAuthCredentials
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: str

    metadata: Optional[Dict[str, object]]

    updated_at: str


class DataConnectorLinearDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorLinearDiscriminatedConnectionSettingsSettingsOAuth]


class DataConnectorLinearDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["linear"]]

    settings: DataConnectorLinearDiscriminatedConnectionSettingsSettings


class DataConnectorLinkedinDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    access_token: Required[str]

    client_id: str
    """Client ID used for the connection"""

    expires_at: str

    expires_in: float

    raw: Dict[str, object]

    refresh_token: str

    scope: str

    token_type: str


class DataConnectorLinkedinDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    created_at: str

    credentials: DataConnectorLinkedinDiscriminatedConnectionSettingsSettingsOAuthCredentials
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: str

    metadata: Optional[Dict[str, object]]

    updated_at: str


class DataConnectorLinkedinDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorLinkedinDiscriminatedConnectionSettingsSettingsOAuth]


class DataConnectorLinkedinDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["linkedin"]]

    settings: DataConnectorLinkedinDiscriminatedConnectionSettingsSettings


class DataConnectorNotionDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    access_token: Required[str]

    client_id: str
    """Client ID used for the connection"""

    expires_at: str

    expires_in: float

    raw: Dict[str, object]

    refresh_token: str

    scope: str

    token_type: str


class DataConnectorNotionDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    created_at: str

    credentials: DataConnectorNotionDiscriminatedConnectionSettingsSettingsOAuthCredentials
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: str

    metadata: Optional[Dict[str, object]]

    updated_at: str


class DataConnectorNotionDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorNotionDiscriminatedConnectionSettingsSettingsOAuth]


class DataConnectorNotionDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["notion"]]

    settings: DataConnectorNotionDiscriminatedConnectionSettingsSettings


class DataConnectorOutreachDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    access_token: Required[str]

    client_id: str
    """Client ID used for the connection"""

    expires_at: str

    expires_in: float

    raw: Dict[str, object]

    refresh_token: str

    scope: str

    token_type: str


class DataConnectorOutreachDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    created_at: str

    credentials: DataConnectorOutreachDiscriminatedConnectionSettingsSettingsOAuthCredentials
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: str

    metadata: Optional[Dict[str, object]]

    updated_at: str


class DataConnectorOutreachDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorOutreachDiscriminatedConnectionSettingsSettingsOAuth]


class DataConnectorOutreachDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["outreach"]]

    settings: DataConnectorOutreachDiscriminatedConnectionSettingsSettings


class DataConnectorPipedriveDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    access_token: Required[str]

    client_id: str
    """Client ID used for the connection"""

    expires_at: str

    expires_in: float

    raw: Dict[str, object]

    refresh_token: str

    scope: str

    token_type: str


class DataConnectorPipedriveDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    created_at: str

    credentials: DataConnectorPipedriveDiscriminatedConnectionSettingsSettingsOAuthCredentials
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: str

    metadata: Optional[Dict[str, object]]

    updated_at: str


class DataConnectorPipedriveDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    api_domain: Required[str]
    """The API URL of your Pipedrive account (e.g., example)"""

    oauth: Required[DataConnectorPipedriveDiscriminatedConnectionSettingsSettingsOAuth]


class DataConnectorPipedriveDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["pipedrive"]]

    settings: DataConnectorPipedriveDiscriminatedConnectionSettingsSettings


class DataConnectorQuickbooksDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    access_token: Required[str]

    client_id: str
    """Client ID used for the connection"""

    expires_at: str

    expires_in: float

    raw: Dict[str, object]

    refresh_token: str

    scope: str

    token_type: str


class DataConnectorQuickbooksDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    created_at: str

    credentials: DataConnectorQuickbooksDiscriminatedConnectionSettingsSettingsOAuthCredentials
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: str

    metadata: Optional[Dict[str, object]]

    updated_at: str


class DataConnectorQuickbooksDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorQuickbooksDiscriminatedConnectionSettingsSettingsOAuth]

    realm_id: Required[Annotated[str, PropertyInfo(alias="realmId")]]
    """The realmId of your quickbooks company (e.g., 9341453474484455)"""


class DataConnectorQuickbooksDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["quickbooks"]]

    settings: DataConnectorQuickbooksDiscriminatedConnectionSettingsSettings


class DataConnectorRedditDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    access_token: Required[str]

    client_id: str
    """Client ID used for the connection"""

    expires_at: str

    expires_in: float

    raw: Dict[str, object]

    refresh_token: str

    scope: str

    token_type: str


class DataConnectorRedditDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    created_at: str

    credentials: DataConnectorRedditDiscriminatedConnectionSettingsSettingsOAuthCredentials
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: str

    metadata: Optional[Dict[str, object]]

    updated_at: str


class DataConnectorRedditDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorRedditDiscriminatedConnectionSettingsSettingsOAuth]


class DataConnectorRedditDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["reddit"]]

    settings: DataConnectorRedditDiscriminatedConnectionSettingsSettings


class DataConnectorSalesloftDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    access_token: Required[str]

    client_id: str
    """Client ID used for the connection"""

    expires_at: str

    expires_in: float

    raw: Dict[str, object]

    refresh_token: str

    scope: str

    token_type: str


class DataConnectorSalesloftDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    created_at: str

    credentials: DataConnectorSalesloftDiscriminatedConnectionSettingsSettingsOAuthCredentials
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: str

    metadata: Optional[Dict[str, object]]

    updated_at: str


class DataConnectorSalesloftDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorSalesloftDiscriminatedConnectionSettingsSettingsOAuth]


class DataConnectorSalesloftDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["salesloft"]]

    settings: DataConnectorSalesloftDiscriminatedConnectionSettingsSettings


class DataConnectorSharepointDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    access_token: Required[str]

    client_id: str
    """Client ID used for the connection"""

    expires_at: str

    expires_in: float

    raw: Dict[str, object]

    refresh_token: str

    scope: str

    token_type: str


class DataConnectorSharepointDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    created_at: str

    credentials: DataConnectorSharepointDiscriminatedConnectionSettingsSettingsOAuthCredentials
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: str

    metadata: Optional[Dict[str, object]]

    updated_at: str


class DataConnectorSharepointDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorSharepointDiscriminatedConnectionSettingsSettingsOAuth]


class DataConnectorSharepointDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["sharepoint"]]

    settings: DataConnectorSharepointDiscriminatedConnectionSettingsSettings


class DataConnectorSlackDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    access_token: Required[str]

    client_id: str
    """Client ID used for the connection"""

    expires_at: str

    expires_in: float

    raw: Dict[str, object]

    refresh_token: str

    scope: str

    token_type: str


class DataConnectorSlackDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    created_at: str

    credentials: DataConnectorSlackDiscriminatedConnectionSettingsSettingsOAuthCredentials
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: str

    metadata: Optional[Dict[str, object]]

    updated_at: str


class DataConnectorSlackDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorSlackDiscriminatedConnectionSettingsSettingsOAuth]


class DataConnectorSlackDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["slack"]]

    settings: DataConnectorSlackDiscriminatedConnectionSettingsSettings


class DataConnectorTwitterDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    access_token: Required[str]

    client_id: str
    """Client ID used for the connection"""

    expires_at: str

    expires_in: float

    raw: Dict[str, object]

    refresh_token: str

    scope: str

    token_type: str


class DataConnectorTwitterDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    created_at: str

    credentials: DataConnectorTwitterDiscriminatedConnectionSettingsSettingsOAuthCredentials
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: str

    metadata: Optional[Dict[str, object]]

    updated_at: str


class DataConnectorTwitterDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorTwitterDiscriminatedConnectionSettingsSettingsOAuth]


class DataConnectorTwitterDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["twitter"]]

    settings: DataConnectorTwitterDiscriminatedConnectionSettingsSettings


class DataConnectorXeroDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    access_token: Required[str]

    client_id: str
    """Client ID used for the connection"""

    expires_at: str

    expires_in: float

    raw: Dict[str, object]

    refresh_token: str

    scope: str

    token_type: str


class DataConnectorXeroDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    created_at: str

    credentials: DataConnectorXeroDiscriminatedConnectionSettingsSettingsOAuthCredentials
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: str

    metadata: Optional[Dict[str, object]]

    updated_at: str


class DataConnectorXeroDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorXeroDiscriminatedConnectionSettingsSettingsOAuth]


class DataConnectorXeroDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["xero"]]

    settings: DataConnectorXeroDiscriminatedConnectionSettingsSettings


class DataConnectorZohoDeskDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    access_token: Required[str]

    client_id: str
    """Client ID used for the connection"""

    expires_at: str

    expires_in: float

    raw: Dict[str, object]

    refresh_token: str

    scope: str

    token_type: str


class DataConnectorZohoDeskDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    created_at: str

    credentials: DataConnectorZohoDeskDiscriminatedConnectionSettingsSettingsOAuthCredentials
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: str

    metadata: Optional[Dict[str, object]]

    updated_at: str


class DataConnectorZohoDeskDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    extension: Required[str]
    """The domain extension of your Zoho account (e.g., https://accounts.zoho.com/)"""

    oauth: Required[DataConnectorZohoDeskDiscriminatedConnectionSettingsSettingsOAuth]


class DataConnectorZohoDeskDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["zoho-desk"]]

    settings: DataConnectorZohoDeskDiscriminatedConnectionSettingsSettings


class DataConnectorAirtableDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    airtable_base: Required[Annotated[str, PropertyInfo(alias="airtableBase")]]

    api_key: Required[Annotated[str, PropertyInfo(alias="apiKey")]]


class DataConnectorAirtableDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["airtable"]]

    settings: DataConnectorAirtableDiscriminatedConnectionSettingsSettings


class DataConnectorApolloDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    api_key: Required[str]


class DataConnectorApolloDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["apollo"]]

    settings: DataConnectorApolloDiscriminatedConnectionSettingsSettings


class DataConnectorBrexDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    access_token: Required[Annotated[str, PropertyInfo(alias="accessToken")]]


class DataConnectorBrexDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["brex"]]

    settings: DataConnectorBrexDiscriminatedConnectionSettingsSettings


class DataConnectorCodaDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    api_key: Required[Annotated[str, PropertyInfo(alias="apiKey")]]


class DataConnectorCodaDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["coda"]]

    settings: DataConnectorCodaDiscriminatedConnectionSettingsSettings


class DataConnectorFinchDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    access_token: Required[str]


class DataConnectorFinchDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["finch"]]

    settings: DataConnectorFinchDiscriminatedConnectionSettingsSettings


class DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember0ServiceAccountTyped(
    TypedDict, total=False
):
    project_id: Required[str]


DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember0ServiceAccount: TypeAlias = Union[
    DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember0ServiceAccountTyped, Dict[str, object]
]


class DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember0(TypedDict, total=False):
    role: Required[Literal["admin"]]

    service_account: Required[
        Annotated[
            DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember0ServiceAccount,
            PropertyInfo(alias="serviceAccount"),
        ]
    ]


class DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember0UserJsonTyped(
    TypedDict, total=False
):
    app_name: Required[Annotated[str, PropertyInfo(alias="appName")]]

    sts_token_manager: Required[Annotated[Dict[str, object], PropertyInfo(alias="stsTokenManager")]]

    uid: Required[str]


DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember0UserJson: TypeAlias = Union[
    DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember0UserJsonTyped,
    Dict[str, object],
]


class DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember0(
    TypedDict, total=False
):
    method: Required[Literal["userJson"]]

    user_json: Required[
        Annotated[
            DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember0UserJson,
            PropertyInfo(alias="userJson"),
        ]
    ]


class DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember1(
    TypedDict, total=False
):
    custom_token: Required[Annotated[str, PropertyInfo(alias="customToken")]]

    method: Required[Literal["customToken"]]


class DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember2(
    TypedDict, total=False
):
    email: Required[str]

    method: Required[Literal["emailPassword"]]

    password: Required[str]


DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthData: TypeAlias = Union[
    DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember0,
    DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember1,
    DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember2,
]


class DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1FirebaseConfig(TypedDict, total=False):
    api_key: Required[Annotated[str, PropertyInfo(alias="apiKey")]]

    app_id: Required[Annotated[str, PropertyInfo(alias="appId")]]

    auth_domain: Required[Annotated[str, PropertyInfo(alias="authDomain")]]

    database_url: Required[Annotated[str, PropertyInfo(alias="databaseURL")]]

    project_id: Required[Annotated[str, PropertyInfo(alias="projectId")]]

    measurement_id: Annotated[str, PropertyInfo(alias="measurementId")]

    messaging_sender_id: Annotated[str, PropertyInfo(alias="messagingSenderId")]

    storage_bucket: Annotated[str, PropertyInfo(alias="storageBucket")]


class DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1(TypedDict, total=False):
    auth_data: Required[
        Annotated[
            DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthData,
            PropertyInfo(alias="authData"),
        ]
    ]

    firebase_config: Required[
        Annotated[
            DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1FirebaseConfig,
            PropertyInfo(alias="firebaseConfig"),
        ]
    ]

    role: Required[Literal["user"]]


DataConnectorFirebaseDiscriminatedConnectionSettingsSettings: TypeAlias = Union[
    DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember0,
    DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1,
]


class DataConnectorFirebaseDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["firebase"]]

    settings: DataConnectorFirebaseDiscriminatedConnectionSettingsSettings


class DataConnectorForeceiptDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    env_name: Required[Annotated[Literal["staging", "production"], PropertyInfo(alias="envName")]]

    _id: object

    credentials: object


class DataConnectorForeceiptDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["foreceipt"]]

    settings: DataConnectorForeceiptDiscriminatedConnectionSettingsSettings


class DataConnectorGreenhouseDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    api_key: Required[Annotated[str, PropertyInfo(alias="apiKey")]]


class DataConnectorGreenhouseDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["greenhouse"]]

    settings: DataConnectorGreenhouseDiscriminatedConnectionSettingsSettings


class DataConnectorHeronDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["heron"]]

    settings: object


class DataConnectorLunchmoneyDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["lunchmoney"]]

    settings: object


class DataConnectorMercuryDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["mercury"]]

    settings: object


class DataConnectorMergeDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    account_token: Required[Annotated[str, PropertyInfo(alias="accountToken")]]

    account_details: Annotated[object, PropertyInfo(alias="accountDetails")]


class DataConnectorMergeDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["merge"]]

    settings: DataConnectorMergeDiscriminatedConnectionSettingsSettings


class DataConnectorMootaDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["moota"]]

    settings: object


class DataConnectorOnebrickDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    access_token: Required[Annotated[str, PropertyInfo(alias="accessToken")]]


class DataConnectorOnebrickDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["onebrick"]]

    settings: DataConnectorOnebrickDiscriminatedConnectionSettingsSettings


class DataConnectorPlaidDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    access_token: Required[Annotated[str, PropertyInfo(alias="accessToken")]]

    institution: object

    item: object

    item_id: Annotated[Optional[str], PropertyInfo(alias="itemId")]

    status: object

    webhook_item_error: Annotated[None, PropertyInfo(alias="webhookItemError")]


class DataConnectorPlaidDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["plaid"]]

    settings: DataConnectorPlaidDiscriminatedConnectionSettingsSettings


class DataConnectorPostgresDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    database_url: Annotated[str, PropertyInfo(alias="databaseURL")]


class DataConnectorPostgresDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["postgres"]]

    settings: DataConnectorPostgresDiscriminatedConnectionSettingsSettings


class DataConnectorRampDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    access_token: Annotated[Optional[str], PropertyInfo(alias="accessToken")]

    start_after_transaction_id: Annotated[Optional[str], PropertyInfo(alias="startAfterTransactionId")]


class DataConnectorRampDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["ramp"]]

    settings: DataConnectorRampDiscriminatedConnectionSettingsSettings


class DataConnectorSaltedgeDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["saltedge"]]

    settings: object


class DataConnectorSplitwiseDiscriminatedConnectionSettingsSettingsCurrentUserNotifications(TypedDict, total=False):
    added_as_friend: Required[bool]

    added_to_group: Required[bool]

    announcements: Required[bool]

    bills: Required[bool]

    expense_added: Required[bool]

    expense_updated: Required[bool]

    monthly_summary: Required[bool]

    payments: Required[bool]


class DataConnectorSplitwiseDiscriminatedConnectionSettingsSettingsCurrentUserPicture(TypedDict, total=False):
    large: Optional[str]

    medium: Optional[str]

    original: Optional[str]

    small: Optional[str]

    xlarge: Optional[str]

    xxlarge: Optional[str]


class DataConnectorSplitwiseDiscriminatedConnectionSettingsSettingsCurrentUser(TypedDict, total=False):
    id: Required[float]

    country_code: Required[str]

    custom_picture: Required[bool]

    date_format: Required[str]

    default_currency: Required[str]

    default_group_id: Required[float]

    email: Required[str]

    first_name: Required[str]

    force_refresh_at: Required[str]

    last_name: Required[str]

    locale: Required[str]

    notifications: Required[DataConnectorSplitwiseDiscriminatedConnectionSettingsSettingsCurrentUserNotifications]

    notifications_count: Required[float]

    notifications_read: Required[str]

    picture: Required[DataConnectorSplitwiseDiscriminatedConnectionSettingsSettingsCurrentUserPicture]

    registration_status: Required[str]


class DataConnectorSplitwiseDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    access_token: Required[Annotated[str, PropertyInfo(alias="accessToken")]]

    current_user: Annotated[
        Optional[DataConnectorSplitwiseDiscriminatedConnectionSettingsSettingsCurrentUser],
        PropertyInfo(alias="currentUser"),
    ]


class DataConnectorSplitwiseDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["splitwise"]]

    settings: DataConnectorSplitwiseDiscriminatedConnectionSettingsSettings


class DataConnectorStripeDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    secret_key: Required[Annotated[str, PropertyInfo(alias="secretKey")]]


class DataConnectorStripeDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["stripe"]]

    settings: DataConnectorStripeDiscriminatedConnectionSettingsSettings


class DataConnectorTellerDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    token: Required[str]


class DataConnectorTellerDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["teller"]]

    settings: DataConnectorTellerDiscriminatedConnectionSettingsSettings


class DataConnectorTogglDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    api_token: Required[Annotated[str, PropertyInfo(alias="apiToken")]]

    email: Optional[str]

    password: Optional[str]


class DataConnectorTogglDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["toggl"]]

    settings: DataConnectorTogglDiscriminatedConnectionSettingsSettings


class DataConnectorTwentyDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    access_token: Required[str]


class DataConnectorTwentyDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["twenty"]]

    settings: DataConnectorTwentyDiscriminatedConnectionSettingsSettings


class DataConnectorVenmoDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    credentials: object

    me: object


class DataConnectorVenmoDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["venmo"]]

    settings: DataConnectorVenmoDiscriminatedConnectionSettingsSettings


class DataConnectorWiseDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    env_name: Required[Annotated[Literal["sandbox", "live"], PropertyInfo(alias="envName")]]

    api_token: Annotated[Optional[str], PropertyInfo(alias="apiToken")]


class DataConnectorWiseDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["wise"]]

    settings: DataConnectorWiseDiscriminatedConnectionSettingsSettings


class DataConnectorYodleeDiscriminatedConnectionSettingsSettingsAccessToken(TypedDict, total=False):
    access_token: Required[Annotated[str, PropertyInfo(alias="accessToken")]]

    expires_in: Required[Annotated[float, PropertyInfo(alias="expiresIn")]]

    issued_at: Required[Annotated[str, PropertyInfo(alias="issuedAt")]]


class DataConnectorYodleeDiscriminatedConnectionSettingsSettingsProviderAccount(TypedDict, total=False):
    id: Required[float]

    aggregation_source: Required[Annotated[str, PropertyInfo(alias="aggregationSource")]]

    created_date: Required[Annotated[str, PropertyInfo(alias="createdDate")]]

    dataset: Required[Iterable[object]]

    is_manual: Required[Annotated[bool, PropertyInfo(alias="isManual")]]

    provider_id: Required[Annotated[float, PropertyInfo(alias="providerId")]]

    status: Required[
        Literal["LOGIN_IN_PROGRESS", "USER_INPUT_REQUIRED", "IN_PROGRESS", "PARTIAL_SUCCESS", "SUCCESS", "FAILED"]
    ]

    is_deleted: Annotated[Optional[bool], PropertyInfo(alias="isDeleted")]


class DataConnectorYodleeDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    login_name: Required[Annotated[str, PropertyInfo(alias="loginName")]]

    provider_account_id: Required[Annotated[Union[float, str], PropertyInfo(alias="providerAccountId")]]

    access_token: Annotated[
        Optional[DataConnectorYodleeDiscriminatedConnectionSettingsSettingsAccessToken],
        PropertyInfo(alias="accessToken"),
    ]

    provider: None

    provider_account: Annotated[
        Optional[DataConnectorYodleeDiscriminatedConnectionSettingsSettingsProviderAccount],
        PropertyInfo(alias="providerAccount"),
    ]

    user: None


class DataConnectorYodleeDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["yodlee"]]

    settings: DataConnectorYodleeDiscriminatedConnectionSettingsSettings


Data: TypeAlias = Union[
    DataConnectorAcmeOauth2DiscriminatedConnectionSettings,
    DataConnectorAircallDiscriminatedConnectionSettings,
    DataConnectorConfluenceDiscriminatedConnectionSettings,
    DataConnectorDiscordDiscriminatedConnectionSettings,
    DataConnectorFacebookDiscriminatedConnectionSettings,
    DataConnectorGitHubDiscriminatedConnectionSettings,
    DataConnectorGongDiscriminatedConnectionSettings,
    DataConnectorGoogleCalendarDiscriminatedConnectionSettings,
    DataConnectorGoogleDocsDiscriminatedConnectionSettings,
    DataConnectorGoogleDriveDiscriminatedConnectionSettings,
    DataConnectorGoogleMailDiscriminatedConnectionSettings,
    DataConnectorGoogleSheetDiscriminatedConnectionSettings,
    DataConnectorHubspotDiscriminatedConnectionSettings,
    DataConnectorInstagramDiscriminatedConnectionSettings,
    DataConnectorIntercomDiscriminatedConnectionSettings,
    DataConnectorJiraDiscriminatedConnectionSettings,
    DataConnectorLeverDiscriminatedConnectionSettings,
    DataConnectorLinearDiscriminatedConnectionSettings,
    DataConnectorLinkedinDiscriminatedConnectionSettings,
    DataConnectorNotionDiscriminatedConnectionSettings,
    DataConnectorOutreachDiscriminatedConnectionSettings,
    DataConnectorPipedriveDiscriminatedConnectionSettings,
    DataConnectorQuickbooksDiscriminatedConnectionSettings,
    DataConnectorRedditDiscriminatedConnectionSettings,
    DataConnectorSalesloftDiscriminatedConnectionSettings,
    DataConnectorSharepointDiscriminatedConnectionSettings,
    DataConnectorSlackDiscriminatedConnectionSettings,
    DataConnectorTwitterDiscriminatedConnectionSettings,
    DataConnectorXeroDiscriminatedConnectionSettings,
    DataConnectorZohoDeskDiscriminatedConnectionSettings,
    DataConnectorAirtableDiscriminatedConnectionSettings,
    DataConnectorApolloDiscriminatedConnectionSettings,
    DataConnectorBrexDiscriminatedConnectionSettings,
    DataConnectorCodaDiscriminatedConnectionSettings,
    DataConnectorFinchDiscriminatedConnectionSettings,
    DataConnectorFirebaseDiscriminatedConnectionSettings,
    DataConnectorForeceiptDiscriminatedConnectionSettings,
    DataConnectorGreenhouseDiscriminatedConnectionSettings,
    DataConnectorHeronDiscriminatedConnectionSettings,
    DataConnectorLunchmoneyDiscriminatedConnectionSettings,
    DataConnectorMercuryDiscriminatedConnectionSettings,
    DataConnectorMergeDiscriminatedConnectionSettings,
    DataConnectorMootaDiscriminatedConnectionSettings,
    DataConnectorOnebrickDiscriminatedConnectionSettings,
    DataConnectorPlaidDiscriminatedConnectionSettings,
    DataConnectorPostgresDiscriminatedConnectionSettings,
    DataConnectorRampDiscriminatedConnectionSettings,
    DataConnectorSaltedgeDiscriminatedConnectionSettings,
    DataConnectorSplitwiseDiscriminatedConnectionSettings,
    DataConnectorStripeDiscriminatedConnectionSettings,
    DataConnectorTellerDiscriminatedConnectionSettings,
    DataConnectorTogglDiscriminatedConnectionSettings,
    DataConnectorTwentyDiscriminatedConnectionSettings,
    DataConnectorVenmoDiscriminatedConnectionSettings,
    DataConnectorWiseDiscriminatedConnectionSettings,
    DataConnectorYodleeDiscriminatedConnectionSettings,
]
