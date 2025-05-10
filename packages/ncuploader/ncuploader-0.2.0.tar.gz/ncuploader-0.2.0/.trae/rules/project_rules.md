# Development Guidelines 

Remember this tech stack we use in our development, and don't repeat the common mistakes (in parentheses):

## Environment
- We develop on MacOS (remember add `.DS_Store` files to `.gitignore`)
- We use modern Python 3.12
- Use virtual environments with uv

## Core Libraries
- Pydantic 2.11 (
  - Don't add `@classmethod` to function already decorated with `@field_validator`
  - Don't use `Union`, use `|` for type unions
  - Use `model_dump()` not `.dict()`
  - Use `model_validate()` not `parse_obj()`
  - Remember to use `exclude_none=True` when needed in `model_dump()`
)
- We use loguru for logging (not Python's built-in logging)
- We use rich for good looking terminal output
- We use typer for CLI (not argparse)
- We use dotenv to load .env secrets
- We use nextcloud_client for Nextcloud API interactions

## Project Structure
- Use a modular approach with separate modules for different responsibilities
- Separate CLI logic from core functionality
- Export public API in `__init__.py`
- Keep configuration handling separate from business logic

## Coding Standards
- Use Path objects from pathlib, not string paths or os.path
- Always use type hints with proper return types, including None where applicable
- Use dataclasses or Pydantic models for structured data
- Make code importable as a module (don't rely on global state)
- Follow PEP 8 naming conventions (snake_case for variables and functions)
- Make code testable and easy to understand 

## Project specifi
# We use nc_py_api: from nc_py_api import NextcloudApp
Here is main file from nc_py_api (nc_py_api/nextcloud.py):
"""Nextcloud class providing access to all API endpoints."""

import contextlib
import typing
from abc import ABC

from httpx import Headers

from ._exceptions import NextcloudExceptionNotFound
from ._misc import check_capabilities, require_capabilities
from ._preferences import AsyncPreferencesAPI, PreferencesAPI
from ._preferences_ex import (
    AppConfigExAPI,
    AsyncAppConfigExAPI,
    AsyncPreferencesExAPI,
    PreferencesExAPI,
)
from ._session import (
    AppConfig,
    AsyncNcSession,
    AsyncNcSessionApp,
    AsyncNcSessionBasic,
    NcSession,
    NcSessionApp,
    NcSessionBasic,
    ServerVersion,
)
from ._talk_api import _AsyncTalkAPI, _TalkAPI
from ._theming import ThemingInfo, get_parsed_theme
from .activity import _ActivityAPI, _AsyncActivityAPI
from .apps import _AppsAPI, _AsyncAppsAPI
from .calendar_api import _CalendarAPI
from .ex_app.defs import LogLvl
from .ex_app.occ_commands import AsyncOccCommandsAPI, OccCommandsAPI
from .ex_app.providers.providers import AsyncProvidersApi, ProvidersApi
from .ex_app.ui.ui import AsyncUiApi, UiApi
from .files.files import FilesAPI
from .files.files_async import AsyncFilesAPI
from .loginflow_v2 import _AsyncLoginFlowV2API, _LoginFlowV2API
from .notes import _AsyncNotesAPI, _NotesAPI
from .notifications import _AsyncNotificationsAPI, _NotificationsAPI
from .user_status import _AsyncUserStatusAPI, _UserStatusAPI
from .users import _AsyncUsersAPI, _UsersAPI
from .users_groups import _AsyncUsersGroupsAPI, _UsersGroupsAPI
from .weather_status import _AsyncWeatherStatusAPI, _WeatherStatusAPI
from .webhooks import _AsyncWebhooksAPI, _WebhooksAPI


class _NextcloudBasic(ABC):  # pylint: disable=too-many-instance-attributes
    apps: _AppsAPI
    """Nextcloud API for App management"""
    activity: _ActivityAPI
    """Activity Application API"""
    cal: _CalendarAPI
    """Nextcloud Calendar API"""
    files: FilesAPI
    """Nextcloud API for File System and Files Sharing"""
    preferences: PreferencesAPI
    """Nextcloud User Preferences API"""
    notes: _NotesAPI
    """Nextcloud Notes API"""
    notifications: _NotificationsAPI
    """Nextcloud API for managing user notifications"""
    talk: _TalkAPI
    """Nextcloud Talk API"""
    users: _UsersAPI
    """Nextcloud API for managing users."""
    users_groups: _UsersGroupsAPI
    """Nextcloud API for managing user groups."""
    user_status: _UserStatusAPI
    """Nextcloud API for managing users statuses"""
    weather_status: _WeatherStatusAPI
    """Nextcloud API for managing user weather statuses"""
    webhooks: _WebhooksAPI
    """Nextcloud API for managing webhooks"""
    _session: NcSessionBasic

    def __init__(self, session: NcSessionBasic):
        self.apps = _AppsAPI(session)
        self.activity = _ActivityAPI(session)
        self.cal = _CalendarAPI(session)
        self.files = FilesAPI(session)
        self.preferences = PreferencesAPI(session)
        self.notes = _NotesAPI(session)
        self.notifications = _NotificationsAPI(session)
        self.talk = _TalkAPI(session)
        self.users = _UsersAPI(session)
        self.users_groups = _UsersGroupsAPI(session)
        self.user_status = _UserStatusAPI(session)
        self.weather_status = _WeatherStatusAPI(session)
        self.webhooks = _WebhooksAPI(session)

    @property
    def capabilities(self) -> dict:
        """Returns the capabilities of the Nextcloud instance."""
        return self._session.capabilities

    @property
    def srv_version(self) -> ServerVersion:
        """Returns dictionary with the server version."""
        return self._session.nc_version

    def check_capabilities(self, capabilities: str | list[str]) -> list[str]:
        """Returns the list with missing capabilities if any."""
        return check_capabilities(capabilities, self.capabilities)

    def update_server_info(self) -> None:
        """Updates the capabilities and the Nextcloud version.

        *In normal cases, it is called automatically and there is no need to call it manually.*
        """
        self._session.update_server_info()

    @property
    def response_headers(self) -> Headers:
        """Returns the `HTTPX headers <https://www.python-httpx.org/api/#headers>`_ from the last response."""
        return self._session.response_headers

    @property
    def theme(self) -> ThemingInfo | None:
        """Returns Theme information."""
        return get_parsed_theme(self.capabilities["theming"]) if "theming" in self.capabilities else None

    def perform_login(self) -> bool:
        """Performs login into Nextcloud if not already logged in; manual invocation of this method is unnecessary."""
        try:
            self.update_server_info()
        except Exception:  # noqa pylint: disable=broad-exception-caught
            return False
        return True

    def ocs(
        self,
        method: str,
        path: str,
        *,
        content: bytes | str | typing.Iterable[bytes] | typing.AsyncIterable[bytes] | None = None,
        json: dict | list | None = None,
        response_type: str | None = None,
        params: dict | None = None,
        **kwargs,
    ):
        """Performs OCS call and returns OCS response payload data."""
        return self._session.ocs(
            method, path, content=content, json=json, response_type=response_type, params=params, **kwargs
        )

    def download_log(self, fp) -> None:
        """Downloads Nextcloud log file. Requires Admin privileges."""
        self._session.download2stream("/index.php/settings/admin/log/download", fp)


class _AsyncNextcloudBasic(ABC):  # pylint: disable=too-many-instance-attributes
    apps: _AsyncAppsAPI
    """Nextcloud API for App management"""
    activity: _AsyncActivityAPI
    """Activity Application API"""
    # cal: _CalendarAPI
    # """Nextcloud Calendar API"""
    files: AsyncFilesAPI
    """Nextcloud API for File System and Files Sharing"""
    preferences: AsyncPreferencesAPI
    """Nextcloud User Preferences API"""
    notes: _AsyncNotesAPI
    """Nextcloud Notes API"""
    notifications: _AsyncNotificationsAPI
    """Nextcloud API for managing user notifications"""
    talk: _AsyncTalkAPI
    """Nextcloud Talk API"""
    users: _AsyncUsersAPI
    """Nextcloud API for managing users."""
    users_groups: _AsyncUsersGroupsAPI
    """Nextcloud API for managing user groups."""
    user_status: _AsyncUserStatusAPI
    """Nextcloud API for managing users statuses"""
    weather_status: _AsyncWeatherStatusAPI
    """Nextcloud API for managing user weather statuses"""
    webhooks: _AsyncWebhooksAPI
    """Nextcloud API for managing webhooks"""
    _session: AsyncNcSessionBasic

    def __init__(self, session: AsyncNcSessionBasic):
        self.apps = _AsyncAppsAPI(session)
        self.activity = _AsyncActivityAPI(session)
        # self.cal = _CalendarAPI(session)
        self.files = AsyncFilesAPI(session)
        self.preferences = AsyncPreferencesAPI(session)
        self.notes = _AsyncNotesAPI(session)
        self.notifications = _AsyncNotificationsAPI(session)
        self.talk = _AsyncTalkAPI(session)
        self.users = _AsyncUsersAPI(session)
        self.users_groups = _AsyncUsersGroupsAPI(session)
        self.user_status = _AsyncUserStatusAPI(session)
        self.weather_status = _AsyncWeatherStatusAPI(session)
        self.webhooks = _AsyncWebhooksAPI(session)

    @property
    async def capabilities(self) -> dict:
        """Returns the capabilities of the Nextcloud instance."""
        return await self._session.capabilities

    @property
    async def srv_version(self) -> ServerVersion:
        """Returns dictionary with the server version."""
        return await self._session.nc_version

    async def check_capabilities(self, capabilities: str | list[str]) -> list[str]:
        """Returns the list with missing capabilities if any."""
        return check_capabilities(capabilities, await self.capabilities)

    async def update_server_info(self) -> None:
        """Updates the capabilities and the Nextcloud version.

        *In normal cases, it is called automatically and there is no need to call it manually.*
        """
        await self._session.update_server_info()

    @property
    def response_headers(self) -> Headers:
        """Returns the `HTTPX headers <https://www.python-httpx.org/api/#headers>`_ from the last response."""
        return self._session.response_headers

    @property
    async def theme(self) -> ThemingInfo | None:
        """Returns Theme information."""
        return get_parsed_theme((await self.capabilities)["theming"]) if "theming" in await self.capabilities else None

    async def perform_login(self) -> bool:
        """Performs login into Nextcloud if not already logged in; manual invocation of this method is unnecessary."""
        try:
            await self.update_server_info()
        except Exception:  # noqa pylint: disable=broad-exception-caught
            return False
        return True

    async def ocs(
        self,
        method: str,
        path: str,
        *,
        content: bytes | str | typing.Iterable[bytes] | typing.AsyncIterable[bytes] | None = None,
        json: dict | list | None = None,
        response_type: str | None = None,
        params: dict | None = None,
        **kwargs,
    ):
        """Performs OCS call and returns OCS response payload data."""
        return await self._session.ocs(
            method, path, content=content, json=json, response_type=response_type, params=params, **kwargs
        )

    async def download_log(self, fp) -> None:
        """Downloads Nextcloud log file. Requires Admin privileges."""
        await self._session.download2stream("/index.php/settings/admin/log/download", fp)


class Nextcloud(_NextcloudBasic):
    """Nextcloud client class.

    Allows you to connect to Nextcloud and perform operations on files, shares, users, and everything else.
    """

    _session: NcSession
    loginflow_v2: _LoginFlowV2API
    """Nextcloud Login flow v2."""

    def __init__(self, **kwargs):
        """If the parameters are not specified, they will be taken from the environment.

        :param nextcloud_url: url of the nextcloud instance.
        :param nc_auth_user: login username. Optional.
        :param nc_auth_pass: password or app-password for the username. Optional.
        """
        self._session = NcSession(**kwargs)
        self.loginflow_v2 = _LoginFlowV2API(self._session)
        super().__init__(self._session)

    @property
    def user(self) -> str:
        """Returns current user ID."""
        return self._session.user


class AsyncNextcloud(_AsyncNextcloudBasic):
    """Async Nextcloud client class.

    Allows you to connect to Nextcloud and perform operations on files, shares, users, and everything else.
    """

    _session: AsyncNcSession
    loginflow_v2: _AsyncLoginFlowV2API
    """Nextcloud Login flow v2."""

    def __init__(self, **kwargs):
        """If the parameters are not specified, they will be taken from the environment.

        :param nextcloud_url: url of the nextcloud instance.
        :param nc_auth_user: login username. Optional.
        :param nc_auth_pass: password or app-password for the username. Optional.
        """
        self._session = AsyncNcSession(**kwargs)
        self.loginflow_v2 = _AsyncLoginFlowV2API(self._session)
        super().__init__(self._session)

    @property
    async def user(self) -> str:
        """Returns current user ID."""
        return await self._session.user


class NextcloudApp(_NextcloudBasic):
    """Class for communication with Nextcloud in Nextcloud applications.

    Provides additional API required for applications such as user impersonation,
    endpoint registration, new authentication method, etc.

    .. note:: Instance of this class should not be created directly in ``normal`` applications,
        it will be provided for each app endpoint call.
    """

    _session: NcSessionApp
    appconfig_ex: AppConfigExAPI
    """Nextcloud App Preferences API for ExApps"""
    preferences_ex: PreferencesExAPI
    """Nextcloud User Preferences API for ExApps"""
    ui: UiApi
    """Nextcloud UI API for ExApps"""
    providers: ProvidersApi
    """API for registering Events listeners for ExApps"""
    occ_commands: OccCommandsAPI
    """API for registering OCC command for ExApps"""

    def __init__(self, **kwargs):
        """The parameters will be taken from the environment.

        They can be overridden by specifying them in **kwargs**, but this behavior is highly discouraged.
        """
        self._session = NcSessionApp(**kwargs)
        super().__init__(self._session)
        self.appconfig_ex = AppConfigExAPI(self._session)
        self.preferences_ex = PreferencesExAPI(self._session)
        self.ui = UiApi(self._session)
        self.providers = ProvidersApi(self._session)
        self.occ_commands = OccCommandsAPI(self._session)

    @property
    def enabled_state(self) -> bool:
        """Returns ``True`` if ExApp is enabled, ``False`` otherwise."""
        with contextlib.suppress(Exception):
            return bool(self._session.ocs("GET", "/ocs/v1.php/apps/app_api/ex-app/state"))
        return False

    def log(self, log_lvl: LogLvl, content: str, fast_send: bool = False) -> None:
        """Writes log to the Nextcloud log file."""
        int_log_lvl = int(log_lvl)
        if int_log_lvl < 0 or int_log_lvl > 4:
            raise ValueError("Invalid `log_lvl` value")
        if not fast_send:
            if self.check_capabilities("app_api"):
                return
            if int_log_lvl < self.capabilities["app_api"].get("loglevel", 0):
                return
        with contextlib.suppress(Exception):
            self._session.ocs("POST", f"{self._session.ae_url}/log", json={"level": int_log_lvl, "message": content})

    def users_list(self) -> list[str]:
        """Returns list of users on the Nextcloud instance."""
        return self._session.ocs("GET", f"{self._session.ae_url}/users")

    @property
    def user(self) -> str:
        """Property containing the current user ID.

        **ExApps** can change user ID they impersonate with **set_user** method.
        """
        return self._session.user

    def set_user(self, user_id: str):
        """Changes current User ID."""
        if self._session.user != user_id:
            self._session.set_user(user_id)
            self.talk.config_sha = ""
            self.talk.modified_since = 0
            self.activity.last_given = 0
            self.notes.last_etag = ""
            self._session.update_server_info()

    @property
    def app_cfg(self) -> AppConfig:
        """Returns deploy config, with AppAPI version, Application version and name."""
        return self._session.cfg

    def register_talk_bot(self, callback_url: str, display_name: str, description: str = "") -> tuple[str, str]:
        """Registers Talk BOT.

        .. note:: AppAPI will add a record in a case of successful registration to the ``appconfig_ex`` table.

        :param callback_url: URL suffix for fetching new messages. MUST be ``UNIQ`` for each bot the app provides.
        :param display_name: The name under which the messages will be posted.
        :param description: Optional description shown in the admin settings.
        :return: Tuple with ID and the secret used for signing requests.
        """
        require_capabilities("app_api", self._session.capabilities)
        require_capabilities("spreed.features.bots-v1", self._session.capabilities)
        params = {
            "name": display_name,
            "route": callback_url,
            "description": description,
        }
        result = self._session.ocs("POST", f"{self._session.ae_url}/talk_bot", json=params)
        return result["id"], result["secret"]

    def unregister_talk_bot(self, callback_url: str) -> bool:
        """Unregisters Talk BOT."""
        require_capabilities("app_api", self._session.capabilities)
        require_capabilities("spreed.features.bots-v1", self._session.capabilities)
        params = {
            "route": callback_url,
        }
        try:
            self._session.ocs("DELETE", f"{self._session.ae_url}/talk_bot", json=params)
        except NextcloudExceptionNotFound:
            return False
        return True

    def set_init_status(self, progress: int, error: str = "") -> None:
        """Sets state of the app initialization.

        :param progress: a number from ``0`` to ``100`` indicating the percentage of application readiness for work.
            After sending ``100`` AppAPI will enable the application.
        :param error: if non-empty, signals to AppAPI that the application cannot be initialized successfully.
        """
        self._session.ocs(
            "PUT",
            f"/ocs/v1.php/apps/app_api/apps/status/{self._session.cfg.app_name}",
            json={
                "progress": progress,
                "error": error,
            },
        )


class AsyncNextcloudApp(_AsyncNextcloudBasic):
    """Class for communication with Nextcloud in Async Nextcloud applications.

    Provides additional API required for applications such as user impersonation,
    endpoint registration, new authentication method, etc.

    .. note:: Instance of this class should not be created directly in ``normal`` applications,
        it will be provided for each app endpoint call.
    """

    _session: AsyncNcSessionApp
    appconfig_ex: AsyncAppConfigExAPI
    """Nextcloud App Preferences API for ExApps"""
    preferences_ex: AsyncPreferencesExAPI
    """Nextcloud User Preferences API for ExApps"""
    ui: AsyncUiApi
    """Nextcloud UI API for ExApps"""
    providers: AsyncProvidersApi
    """API for registering Events listeners for ExApps"""
    occ_commands: AsyncOccCommandsAPI
    """API for registering OCC command for ExApps"""

    def __init__(self, **kwargs):
        """The parameters will be taken from the environment.

        They can be overridden by specifying them in **kwargs**, but this behavior is highly discouraged.
        """
        self._session = AsyncNcSessionApp(**kwargs)
        super().__init__(self._session)
        self.appconfig_ex = AsyncAppConfigExAPI(self._session)
        self.preferences_ex = AsyncPreferencesExAPI(self._session)
        self.ui = AsyncUiApi(self._session)
        self.providers = AsyncProvidersApi(self._session)
        self.occ_commands = AsyncOccCommandsAPI(self._session)

    @property
    async def enabled_state(self) -> bool:
        """Returns ``True`` if ExApp is enabled, ``False`` otherwise."""
        with contextlib.suppress(Exception):
            return bool(await self._session.ocs("GET", "/ocs/v1.php/apps/app_api/ex-app/state"))
        return False

    async def log(self, log_lvl: LogLvl, content: str, fast_send: bool = False) -> None:
        """Writes log to the Nextcloud log file."""
        int_log_lvl = int(log_lvl)
        if int_log_lvl < 0 or int_log_lvl > 4:
            raise ValueError("Invalid `log_lvl` value")
        if not fast_send:
            if await self.check_capabilities("app_api"):
                return
            if int_log_lvl < (await self.capabilities)["app_api"].get("loglevel", 0):
                return
        with contextlib.suppress(Exception):
            await self._session.ocs(
                "POST", f"{self._session.ae_url}/log", json={"level": int_log_lvl, "message": content}
            )

    async def users_list(self) -> list[str]:
        """Returns list of users on the Nextcloud instance."""
        return await self._session.ocs("GET", f"{self._session.ae_url}/users")

    @property
    async def user(self) -> str:
        """Property containing the current user ID.

        **ExApps** can change user ID they impersonate with **set_user** method.
        """
        return await self._session.user

    async def set_user(self, user_id: str):
        """Changes current User ID."""
        if await self._session.user != user_id:
            self._session.set_user(user_id)
            self.talk.config_sha = ""
            self.talk.modified_since = 0
            self.activity.last_given = 0
            self.notes.last_etag = ""
            await self._session.update_server_info()

    @property
    def app_cfg(self) -> AppConfig:
        """Returns deploy config, with AppAPI version, Application version and name."""
        return self._session.cfg

    async def register_talk_bot(self, callback_url: str, display_name: str, description: str = "") -> tuple[str, str]:
        """Registers Talk BOT.

        .. note:: AppAPI will add a record in a case of successful registration to the ``appconfig_ex`` table.

        :param callback_url: URL suffix for fetching new messages. MUST be ``UNIQ`` for each bot the app provides.
        :param display_name: The name under which the messages will be posted.
        :param description: Optional description shown in the admin settings.
        :return: Tuple with ID and the secret used for signing requests.
        """
        require_capabilities("app_api", await self._session.capabilities)
        require_capabilities("spreed.features.bots-v1", await self._session.capabilities)
        params = {
            "name": display_name,
            "route": callback_url,
            "description": description,
        }
        result = await self._session.ocs("POST", f"{self._session.ae_url}/talk_bot", json=params)
        return result["id"], result["secret"]

    async def unregister_talk_bot(self, callback_url: str) -> bool:
        """Unregisters Talk BOT."""
        require_capabilities("app_api", await self._session.capabilities)
        require_capabilities("spreed.features.bots-v1", await self._session.capabilities)
        params = {
            "route": callback_url,
        }
        try:
            await self._session.ocs("DELETE", f"{self._session.ae_url}/talk_bot", json=params)
        except NextcloudExceptionNotFound:
            return False
        return True

    async def set_init_status(self, progress: int, error: str = "") -> None:
        """Sets state of the app initialization.

        :param progress: a number from ``0`` to ``100`` indicating the percentage of application readiness for work.
            After sending ``100`` AppAPI will enable the application.
        :param error: if non-empty, signals to AppAPI that the application cannot be initialized successfully.
        """
        await self._session.ocs(
            "PUT",
            f"/ocs/v1.php/apps/app_api/apps/status/{self._session.cfg.app_name}",
            json={
                "progress": progress,
                "error": error,
            },
        )

And files.py: """Nextcloud API for working with the file system."""

import builtins
import os
from pathlib import Path
from urllib.parse import quote

from httpx import Headers

from .._exceptions import NextcloudException, NextcloudExceptionNotFound, check_error
from .._misc import random_string, require_capabilities
from .._session import NcSessionBasic
from . import FsNode, LockType, SystemTag
from ._files import (
    PROPFIND_PROPERTIES,
    PropFindType,
    build_find_request,
    build_list_by_criteria_req,
    build_list_tag_req,
    build_list_tags_response,
    build_listdir_req,
    build_listdir_response,
    build_setfav_req,
    build_tags_ids_for_object,
    build_update_tag_req,
    dav_get_obj_path,
    element_tree_as_str,
    etag_fileid_from_response,
    get_propfind_properties,
    lf_parse_webdav_response,
)
from .sharing import _FilesSharingAPI


class FilesAPI:
    """Class that encapsulates file system and file sharing API, avalaible as **nc.files.<method>**."""

    sharing: _FilesSharingAPI
    """API for managing Files Shares"""

    def __init__(self, session: NcSessionBasic):
        self._session = session
        self.sharing = _FilesSharingAPI(session)

    def listdir(self, path: str | FsNode = "", depth: int = 1, exclude_self=True) -> list[FsNode]:
        """Returns a list of all entries in the specified directory.

        :param path: path to the directory to get the list.
        :param depth: how many directory levels should be included in output. Default = **1** (only specified directory)
        :param exclude_self: boolean value indicating whether the `path` itself should be excluded from the list or not.
            Default = **True**.
        """
        if exclude_self and not depth:
            raise ValueError("Wrong input parameters, query will return nothing.")
        properties = get_propfind_properties(self._session.capabilities)
        path = path.user_path if isinstance(path, FsNode) else path
        return self._listdir(self._session.user, path, properties=properties, depth=depth, exclude_self=exclude_self)

    def by_id(self, file_id: int | str | FsNode) -> FsNode | None:
        """Returns :py:class:`~nc_py_api.files.FsNode` by file_id if any.

        :param file_id: can be full file ID with Nextcloud instance ID or only clear file ID.
        """
        file_id = file_id.file_id if isinstance(file_id, FsNode) else file_id
        result = self.find(req=["eq", "fileid", file_id])
        return result[0] if result else None

    def by_path(self, path: str | FsNode) -> FsNode | None:
        """Returns :py:class:`~nc_py_api.files.FsNode` by exact path if any."""
        path = path.user_path if isinstance(path, FsNode) else path
        result = self.listdir(path, depth=0, exclude_self=False)
        return result[0] if result else None

    def find(self, req: list, path: str | FsNode = "") -> list[FsNode]:
        """Searches a directory for a file or subdirectory with a name.

        :param req: list of conditions to search for. Detailed description here...
        :param path: path where to search from. Default = **""**.
        """
        # `req` possible keys: "name", "mime", "last_modified", "size", "favorite", "fileid"
        root = build_find_request(req, path, self._session.user, self._session.capabilities)
        webdav_response = self._session.adapter_dav.request(
            "SEARCH", "", content=element_tree_as_str(root), headers={"Content-Type": "text/xml"}
        )
        request_info = f"find: {self._session.user}, {req}, {path}"
        return lf_parse_webdav_response(self._session.cfg.dav_url_suffix, webdav_response, request_info)

    def download(self, path: str | FsNode) -> bytes:
        """Downloads and returns the content of a file."""
        path = path.user_path if isinstance(path, FsNode) else path
        response = self._session.adapter_dav.get(quote(dav_get_obj_path(self._session.user, path)))
        check_error(response, f"download: user={self._session.user}, path={path}")
        return response.content

    def download2stream(self, path: str | FsNode, fp, **kwargs) -> None:
        """Downloads file to the given `fp` object.

        :param path: path to download file.
        :param fp: filename (string), pathlib.Path object or a file object.
            The object must implement the ``file.write`` method and be able to write binary data.
        :param kwargs: **chunk_size** an int value specifying chunk size to write. Default = **5Mb**
        """
        path = quote(dav_get_obj_path(self._session.user, path.user_path if isinstance(path, FsNode) else path))
        self._session.download2stream(path, fp, dav=True, **kwargs)

    def download_directory_as_zip(self, path: str | FsNode, local_path: str | Path | None = None, **kwargs) -> Path:
        """Downloads a remote directory as zip archive.

        :param path: path to directory to download.
        :param local_path: relative or absolute file path to save zip file.
        :returns: Path to the saved zip archive.

        .. note:: This works only for directories, you should not use this to download a file.
        """
        path = path.user_path if isinstance(path, FsNode) else path
        result_path = local_path if local_path else os.path.basename(path)
        with open(result_path, "wb") as fp:
            if self._session.nc_version["major"] >= 31:
                full_path = dav_get_obj_path(self._session.user, path)
                accept_header = f"application/{kwargs.get('format', 'zip')}"
                self._session.download2fp(quote(full_path), fp, dav=True, headers={"Accept": accept_header})
            else:
                self._session.download2fp(
                    "/index.php/apps/files/ajax/download.php", fp, dav=False, params={"dir": path}, **kwargs
                )
        return Path(result_path)

    def upload(self, path: str | FsNode, content: bytes | str) -> FsNode:
        """Creates a file with the specified content at the specified path.

        :param path: file's upload path.
        :param content: content to create the file. If it is a string, it will be encoded into bytes using UTF-8.
        """
        path = path.user_path if isinstance(path, FsNode) else path
        full_path = dav_get_obj_path(self._session.user, path)
        response = self._session.adapter_dav.put(quote(full_path), content=content)
        check_error(response, f"upload: user={self._session.user}, path={path}, size={len(content)}")
        return FsNode(full_path.strip("/"), **etag_fileid_from_response(response))

    def upload_stream(self, path: str | FsNode, fp, **kwargs) -> FsNode:
        """Creates a file with content provided by `fp` object at the specified path.

        :param path: file's upload path.
        :param fp: filename (string), pathlib.Path object or a file object.
            The object must implement the ``file.read`` method providing data with str or bytes type.
        :param kwargs: **chunk_size** an int value specifying chunk size to read. Default = **5Mb**
        """
        path = path.user_path if isinstance(path, FsNode) else path
        chunk_size = kwargs.get("chunk_size", 5 * 1024 * 1024)
        if isinstance(fp, str | Path):
            with builtins.open(fp, "rb") as f:
                return self.__upload_stream(path, f, chunk_size)
        elif hasattr(fp, "read"):
            return self.__upload_stream(path, fp, chunk_size)
        else:
            raise TypeError("`fp` must be a path to file or an object with `read` method.")

    def mkdir(self, path: str | FsNode) -> FsNode:
        """Creates a new directory.

        :param path: path of the directory to be created.
        """
        path = path.user_path if isinstance(path, FsNode) else path
        full_path = dav_get_obj_path(self._session.user, path)
        response = self._session.adapter_dav.request("MKCOL", quote(full_path))
        check_error(response)
        full_path += "/" if not full_path.endswith("/") else ""
        return FsNode(full_path.lstrip("/"), **etag_fileid_from_response(response))

    def makedirs(self, path: str | FsNode, exist_ok=False) -> FsNode | None:
        """Creates a new directory and subdirectories.

        :param path: path of the directories to be created.
        :param exist_ok: ignore error if any of pathname components already exists.
        :returns: `FsNode` if directory was created or ``None`` if it was already created.
        """
        _path = ""
        path = path.user_path if isinstance(path, FsNode) else path
        path = path.lstrip("/")
        result = None
        for i in Path(path).parts:
            _path = f"{_path}/{i}"
            if not exist_ok:
                result = self.mkdir(_path)
            else:
                try:
                    result = self.mkdir(_path)
                except NextcloudException as e:
                    if e.status_code != 405:
                        raise e from None
        return result

    def delete(self, path: str | FsNode, not_fail=False) -> None:
        """Deletes a file/directory (moves to trash if trash is enabled).

        :param path: path to delete.
        :param not_fail: if set to ``True`` and the object is not found, it does not raise an exception.
        """
        path = path.user_path if isinstance(path, FsNode) else path
        response = self._session.adapter_dav.delete(quote(dav_get_obj_path(self._session.user, path)))
        if response.status_code == 404 and not_fail:
            return
        check_error(response)

    def move(self, path_src: str | FsNode, path_dest: str | FsNode, overwrite=False) -> FsNode:
        """Moves an existing file or a directory.

        :param path_src: path of an existing file/directory.
        :param path_dest: name of the new one.
        :param overwrite: if ``True`` and the destination object already exists, it gets overwritten.
            Default = **False**.
        """
        path_src = path_src.user_path if isinstance(path_src, FsNode) else path_src
        full_dest_path = dav_get_obj_path(
            self._session.user, path_dest.user_path if isinstance(path_dest, FsNode) else path_dest
        )
        dest = self._session.cfg.dav_endpoint + quote(full_dest_path)
        headers = Headers({"Destination": dest, "Overwrite": "T" if overwrite else "F"}, encoding="utf-8")
        response = self._session.adapter_dav.request(
            "MOVE",
            quote(dav_get_obj_path(self._session.user, path_src)),
            headers=headers,
        )
        check_error(response, f"move: user={self._session.user}, src={path_src}, dest={dest}, {overwrite}")
        return self.find(req=["eq", "fileid", response.headers["OC-FileId"]])[0]

    def copy(self, path_src: str | FsNode, path_dest: str | FsNode, overwrite=False) -> FsNode:
        """Copies an existing file/directory.

        :param path_src: path of an existing file/directory.
        :param path_dest: name of the new one.
        :param overwrite: if ``True`` and the destination object already exists, it gets overwritten.
            Default = **False**.
        """
        path_src = path_src.user_path if isinstance(path_src, FsNode) else path_src
        full_dest_path = dav_get_obj_path(
            self._session.user, path_dest.user_path if isinstance(path_dest, FsNode) else path_dest
        )
        dest = self._session.cfg.dav_endpoint + quote(full_dest_path)
        headers = Headers({"Destination": dest, "Overwrite": "T" if overwrite else "F"}, encoding="utf-8")
        response = self._session.adapter_dav.request(
            "COPY",
            quote(dav_get_obj_path(self._session.user, path_src)),
            headers=headers,
        )
        check_error(response, f"copy: user={self._session.user}, src={path_src}, dest={dest}, {overwrite}")
        return self.find(req=["eq", "fileid", response.headers["OC-FileId"]])[0]

    def list_by_criteria(
        self, properties: list[str] | None = None, tags: list[int | SystemTag] | None = None
    ) -> list[FsNode]:
        """Returns a list of all files/directories for the current user filtered by the specified values.

        :param properties: List of ``properties`` that should have been set for the file.
            Supported values: **favorite**
        :param tags: List of ``tags ids`` or ``SystemTag`` that should have been set for the file.
        """
        root = build_list_by_criteria_req(properties, tags, self._session.capabilities)
        webdav_response = self._session.adapter_dav.request(
            "REPORT", dav_get_obj_path(self._session.user), content=element_tree_as_str(root)
        )
        request_info = f"list_files_by_criteria: {self._session.user}"
        check_error(webdav_response, request_info)
        return lf_parse_webdav_response(self._session.cfg.dav_url_suffix, webdav_response, request_info)

    def setfav(self, path: str | FsNode, value: int | bool) -> None:
        """Sets or unsets favourite flag for specific file.

        :param path: path to the object to set the state.
        :param value: value to set for the ``favourite`` state.
        """
        path = path.user_path if isinstance(path, FsNode) else path
        root = build_setfav_req(value)
        webdav_response = self._session.adapter_dav.request(
            "PROPPATCH", quote(dav_get_obj_path(self._session.user, path)), content=element_tree_as_str(root)
        )
        check_error(webdav_response, f"setfav: path={path}, value={value}")

    def trashbin_list(self) -> list[FsNode]:
        """Returns a list of all entries in the TrashBin."""
        properties = PROPFIND_PROPERTIES
        properties += ["nc:trashbin-filename", "nc:trashbin-original-location", "nc:trashbin-deletion-time"]
        return self._listdir(
            self._session.user, "", properties=properties, depth=1, exclude_self=False, prop_type=PropFindType.TRASHBIN
        )

    def trashbin_restore(self, path: str | FsNode) -> None:
        """Restore a file/directory from the TrashBin.

        :param path: path to delete, e.g., the ``user_path`` field from ``FsNode`` or the **FsNode** class itself.
        """
        restore_name = path.name if isinstance(path, FsNode) else path.split("/", maxsplit=1)[-1]
        path = path.user_path if isinstance(path, FsNode) else path

        dest = self._session.cfg.dav_endpoint + f"/trashbin/{self._session.user}/restore/{restore_name}"
        headers = Headers({"Destination": dest}, encoding="utf-8")
        response = self._session.adapter_dav.request(
            "MOVE",
            quote(f"/trashbin/{self._session.user}/{path}"),
            headers=headers,
        )
        check_error(response, f"trashbin_restore: user={self._session.user}, src={path}, dest={dest}")

    def trashbin_delete(self, path: str | FsNode, not_fail=False) -> None:
        """Deletes a file/directory permanently from the TrashBin.

        :param path: path to delete, e.g., the ``user_path`` field from ``FsNode`` or the **FsNode** class itself.
        :param not_fail: if set to ``True`` and the object is not found, it does not raise an exception.
        """
        path = path.user_path if isinstance(path, FsNode) else path
        response = self._session.adapter_dav.delete(quote(f"/trashbin/{self._session.user}/{path}"))
        if response.status_code == 404 and not_fail:
            return
        check_error(response)

    def trashbin_cleanup(self) -> None:
        """Empties the TrashBin."""
        check_error(self._session.adapter_dav.delete(f"/trashbin/{self._session.user}/trash"))

    def get_versions(self, file_object: FsNode) -> list[FsNode]:
        """Returns a list of all file versions if any."""
        require_capabilities("files.versioning", self._session.capabilities)
        return self._listdir(
            self._session.user,
            str(file_object.info.fileid) if file_object.info.fileid else file_object.file_id,
            properties=PROPFIND_PROPERTIES,
            depth=1,
            exclude_self=False,
            prop_type=PropFindType.VERSIONS_FILEID if file_object.info.fileid else PropFindType.VERSIONS_FILE_ID,
        )

    def restore_version(self, file_object: FsNode) -> None:
        """Restore a file with specified version.

        :param file_object: The **FsNode** class from :py:meth:`~nc_py_api.files.files.FilesAPI.get_versions`.
        """
        require_capabilities("files.versioning", self._session.capabilities)
        dest = self._session.cfg.dav_endpoint + f"/versions/{self._session.user}/restore/{file_object.name}"
        headers = Headers({"Destination": dest}, encoding="utf-8")
        response = self._session.adapter_dav.request(
            "MOVE",
            quote(f"/versions/{self._session.user}/{file_object.user_path}"),
            headers=headers,
        )
        check_error(response, f"restore_version: user={self._session.user}, src={file_object.user_path}")

    def list_tags(self) -> list[SystemTag]:
        """Returns list of the avalaible Tags."""
        root = build_list_tag_req()
        response = self._session.adapter_dav.request("PROPFIND", "/systemtags", content=element_tree_as_str(root))
        return build_list_tags_response(response)

    def get_tags(self, file_id: FsNode | int) -> list[SystemTag]:
        """Returns list of Tags assigned to the File or Directory."""
        fs_object = file_id.info.fileid if isinstance(file_id, FsNode) else file_id
        url_to_fetch = f"/systemtags-relations/files/{fs_object}/"
        response = self._session.adapter_dav.request("PROPFIND", url_to_fetch)
        object_tags_ids = build_tags_ids_for_object(self._session.cfg.dav_url_suffix + url_to_fetch, response)
        if not object_tags_ids:
            return []
        all_tags = self.list_tags()
        return [tag for tag in all_tags if tag.tag_id in object_tags_ids]

    def create_tag(self, name: str, user_visible: bool = True, user_assignable: bool = True) -> None:
        """Creates a new Tag.

        :param name: Name of the tag.
        :param user_visible: Should be Tag visible in the UI.
        :param user_assignable: Can Tag be assigned from the UI.
        """
        response = self._session.adapter_dav.post(
            "/systemtags",
            json={
                "name": name,
                "userVisible": user_visible,
                "userAssignable": user_assignable,
            },
        )
        check_error(response, info=f"create_tag({name})")

    def update_tag(
        self,
        tag_id: int | SystemTag,
        name: str | None = None,
        user_visible: bool | None = None,
        user_assignable: bool | None = None,
    ) -> None:
        """Updates the Tag information."""
        tag_id = tag_id.tag_id if isinstance(tag_id, SystemTag) else tag_id
        root = build_update_tag_req(name, user_visible, user_assignable)
        response = self._session.adapter_dav.request(
            "PROPPATCH", f"/systemtags/{tag_id}", content=element_tree_as_str(root)
        )
        check_error(response)

    def delete_tag(self, tag_id: int | SystemTag) -> None:
        """Deletes the tag."""
        tag_id = tag_id.tag_id if isinstance(tag_id, SystemTag) else tag_id
        response = self._session.adapter_dav.delete(f"/systemtags/{tag_id}")
        check_error(response)

    def tag_by_name(self, tag_name: str) -> SystemTag:
        """Returns Tag info by its name if found or ``None`` otherwise."""
        r = [i for i in self.list_tags() if i.display_name == tag_name]
        if not r:
            raise NextcloudExceptionNotFound(f"Tag with name='{tag_name}' not found.")
        return r[0]

    def assign_tag(self, file_id: FsNode | int, tag_id: SystemTag | int) -> None:
        """Assigns Tag to a file/directory."""
        self._file_change_tag_state(file_id, tag_id, True)

    def unassign_tag(self, file_id: FsNode | int, tag_id: SystemTag | int) -> None:
        """Removes Tag from a file/directory."""
        self._file_change_tag_state(file_id, tag_id, False)

    def lock(self, path: FsNode | str, lock_type: LockType = LockType.MANUAL_LOCK) -> None:
        """Locks the file.

        .. note:: Exception codes: 423 - existing lock present.
        """
        require_capabilities("files.locking", self._session.capabilities)
        full_path = dav_get_obj_path(self._session.user, path.user_path if isinstance(path, FsNode) else path)
        response = self._session.adapter_dav.request(
            "LOCK",
            quote(full_path),
            headers={"X-User-Lock": "1", "X-User-Lock-Type": str(lock_type.value)},
        )
        check_error(response, f"lock: user={self._session.user}, path={full_path}")

    def unlock(self, path: FsNode | str) -> None:
        """Unlocks the file.

        .. note:: Exception codes: 412 - the file is not locked, 423 - the lock is owned by another user.
        """
        require_capabilities("files.locking", self._session.capabilities)
        full_path = dav_get_obj_path(self._session.user, path.user_path if isinstance(path, FsNode) else path)
        response = self._session.adapter_dav.request(
            "UNLOCK",
            quote(full_path),
            headers={"X-User-Lock": "1"},
        )
        check_error(response, f"unlock: user={self._session.user}, path={full_path}")

    def _file_change_tag_state(self, file_id: FsNode | int, tag_id: SystemTag | int, tag_state: bool) -> None:
        fs_object = file_id.info.fileid if isinstance(file_id, FsNode) else file_id
        tag = tag_id.tag_id if isinstance(tag_id, SystemTag) else tag_id
        response = self._session.adapter_dav.request(
            "PUT" if tag_state else "DELETE", f"/systemtags-relations/files/{fs_object}/{tag}"
        )
        check_error(
            response,
            info=f"({'Adding' if tag_state else 'Removing'} `{tag}` {'to' if tag_state else 'from'} {fs_object})",
        )

    def _listdir(
        self,
        user: str,
        path: str,
        properties: list[str],
        depth: int,
        exclude_self: bool,
        prop_type: PropFindType = PropFindType.DEFAULT,
    ) -> list[FsNode]:
        root, dav_path = build_listdir_req(user, path, properties, prop_type)
        webdav_response = self._session.adapter_dav.request(
            "PROPFIND",
            quote(dav_path),
            content=element_tree_as_str(root),
            headers={"Depth": "infinity" if depth == -1 else str(depth)},
        )
        return build_listdir_response(
            self._session.cfg.dav_url_suffix, webdav_response, user, path, properties, exclude_self, prop_type
        )

    def __upload_stream(self, path: str, fp, chunk_size: int) -> FsNode:
        _tmp_path = "nc-py-api-" + random_string(56)
        _dav_path = quote(dav_get_obj_path(self._session.user, _tmp_path, root_path="/uploads"))
        _v2 = bool(self._session.cfg.options.upload_chunk_v2 and chunk_size >= 5 * 1024 * 1024)
        full_path = dav_get_obj_path(self._session.user, path)
        headers = Headers({"Destination": self._session.cfg.dav_endpoint + quote(full_path)}, encoding="utf-8")
        if _v2:
            response = self._session.adapter_dav.request("MKCOL", _dav_path, headers=headers)
        else:
            response = self._session.adapter_dav.request("MKCOL", _dav_path)
        check_error(response)
        try:
            start_bytes = end_bytes = 0
            chunk_number = 1
            while True:
                piece = fp.read(chunk_size)
                if not piece:
                    break
                end_bytes = start_bytes + len(piece)
                if _v2:
                    response = self._session.adapter_dav.put(
                        _dav_path + "/" + str(chunk_number), content=piece, headers=headers
                    )
                else:
                    _filename = str(start_bytes).rjust(15, "0") + "-" + str(end_bytes).rjust(15, "0")
                    response = self._session.adapter_dav.put(_dav_path + "/" + _filename, content=piece)
                check_error(
                    response,
                    f"upload_stream(v={_v2}): user={self._session.user}, path={path}, cur_size={end_bytes}",
                )
                start_bytes = end_bytes
                chunk_number += 1

            response = self._session.adapter_dav.request(
                "MOVE",
                _dav_path + "/.file",
                headers=headers,
            )
            check_error(
                response,
                f"upload_stream(v={_v2}): user={self._session.user}, path={path}, total_size={end_bytes}",
            )
            return FsNode(full_path.strip("/"), **etag_fileid_from_response(response))
        finally:
            self._session.adapter_dav.delete(_dav_path)
