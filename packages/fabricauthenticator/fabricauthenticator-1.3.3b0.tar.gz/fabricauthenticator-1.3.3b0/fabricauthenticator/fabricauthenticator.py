"""FabricAuthenticator for Jupyterhub

Based on CILogon authentication,
in addition checks if user belongs to Fabric JUPYTERHUB COU.

"""
import asyncio
import concurrent
import inspect
import os
from typing import Union, List, Dict

from ldap3.abstract import entry
from oauthenticator import CILogonOAuthenticator
from tornado import web
from ldap3 import Connection, Server, ALL


JUPYTERHUB_COU = os.getenv('FABRIC_COU_JUPYTERHUB', 'CO:COU:Jupyterhub:members:active')


class FabricAuthenticator(CILogonOAuthenticator):
    """ The FabricAuthenticator inherits from CILogonAuthenticator.
    """
    async def authenticate(self, handler, data=None, **kwargs):
        """ First invoke CILogon authenticate method,
            then check if user has JUPYTERHUB_COU attribute.
        """
        auth_model = await super(FabricAuthenticator, self).authenticate(handler, data)
        # check COU
        auth_state = auth_model.get("auth_state")
        cilogon_user = auth_state.get("user", {})

        user_email = cilogon_user.get("email")
        user_sub = cilogon_user.get("sub")
        if not self.is_in_allowed_cou(user_email, user_sub):
            self.log.warn("FABRIC user {} is not in {}".format(auth_model["name"], JUPYTERHUB_COU))
            raise web.HTTPError(403, "Access not allowed")
        self.log.debug("FABRIC user authenticated")
        return auth_model

    async def pre_spawn_start(self, user, spawner):
        """ Populate credentials to spawned notebook environment
        """
        auth_state = await user.get_auth_state()
        self.log.debug("pre_spawn_start: {}".format(user.name))
        if not auth_state:
            return
        spawner.environment['CILOGON_ID_TOKEN'] \
            = auth_state['token_response'].get('id_token', '')
        spawner.environment['CILOGON_REFRESH_TOKEN'] \
            = auth_state['token_response'].get('refresh_token', '')
        self.log.info(f"FABRIC {user} token: {auth_state['token_response'].get('refresh_token', '')}")
        # setup environment
        nb_user = str(user.name)
        if "@" in nb_user:
            nb_user = nb_user.split("@", 1)[0]
        spawner.environment['NB_USER'] = nb_user
        self.log.debug(f"Environment: {spawner.environment}")

    async def refresh_user(self, user, handler=None, **kwargs):
        """
        1. Check if token is valid and then call _shutdown_servers and then redirect to login page
        2. If time of refresh_user is set as token expiry, directly call _shutdown_servers and then redirect to login page
        This is shutdown single user servers and once redirected to login, auth flow gets run and new tokens are passed to spawner
        """
        await self._shutdown_servers(user, handler)
        handler.clear_cookie("jupyterhub-hub-login")
        handler.clear_cookie("jupyterhub-session-id")
        handler.redirect('/hub/logout')
        return True

    @staticmethod
    async def maybe_future(obj):
        """Return an asyncio Future
        Use instead of gen.maybe_future
        For our compatibility, this must accept:
        - asyncio coroutine (gen.maybe_future doesn't work in tornado < 5)
        - tornado coroutine (asyncio.ensure_future doesn't work)
        - scalar (asyncio.ensure_future doesn't work)
        - concurrent.futures.Future (asyncio.ensure_future doesn't work)
        - tornado Future (works both ways)
        - asyncio Future (works both ways)
        """
        if inspect.isawaitable(obj):
            # already awaitable, use ensure_future
            return asyncio.ensure_future(obj)
        elif isinstance(obj, concurrent.futures.Future):
            return asyncio.wrap_future(obj)
        else:
            # could also check for tornado.concurrent.Future
            # but with tornado >= 5.1 tornado.Future is asyncio.Future
            f = asyncio.Future()
            f.set_result(obj)
            return f

    async def _shutdown_servers(self, user, handler):
        """Shutdown servers for logout
        Get all active servers for the provided user, stop them.
        """
        active_servers = [
            name
            for (name, spawner) in user.spawners.items()
            if spawner.active and not spawner.pending
        ]
        if active_servers:
            self.log.info("Shutting down %s's servers", user.name)
            futures = []
            for server_name in active_servers:
                result = handler.stop_single_user(user, server_name)
                futures.append(self.maybe_future(obj=result))
            await asyncio.gather(*futures)

    def is_in_allowed_cou(self, email, sub):
        """ Checks if user is in Comanage JUPYTERHUB COU.

            Args:
                email: i.e. email
                sub: user sub

            Returns:
                Boolean value: True if username has attribute of JUPYTERHUB_COU, False otherwise
        """
        attributelist = self.get_ldap_attributes(email, sub)
        if attributelist:
            self.log.debug("attributelist acquired.")
            # Check if OIDC sub is registered with FABRIC;
            # protect against Idps which use same email addresses
            if sub is not None and attributelist['uid']:
                if sub not in attributelist['uid']:
                    return False
            if attributelist['isMemberOf']:
                for attribute in attributelist['isMemberOf']:
                    if attribute == JUPYTERHUB_COU:
                        return True
        return False

    @staticmethod
    def get_ldap_attributes(email: str, sub: str) -> Union[entry.Entry, None]:
        """Get the LDAP attributes from the Fabric CILogon instance.

        Args:
            email (str): The email address of the user.
            sub (str): The subject identifier (sub) of the user.

        Returns:
            Union[entry.Entry, None]: The attributes list if found, otherwise None.
        """
        # Fetch environment variables with defaults
        ldap_host = os.getenv('LDAP_HOST', '')
        ldap_user = os.getenv('LDAP_USER', '')
        ldap_password = os.getenv('LDAP_PASSWORD', '')
        ldap_search_base = os.getenv('LDAP_SEARCH_BASE', '')

        # Create the server and connection
        server = Server(ldap_host, use_ssl=True, get_info=ALL)
        conn = Connection(server, ldap_user, ldap_password, auto_bind=True)

        # Construct the search filter
        ldap_search_filter = f'(uid={sub})' if sub else f'(mail={email})'

        # Perform the search
        profile_found = conn.search(
            search_base=ldap_search_base,
            search_filter=ldap_search_filter,
            attributes=['isMemberOf', 'uid', 'mail']
        )

        # Retrieve the attributes if found
        attributes = conn.entries[0] if profile_found else None

        # Unbind the connection
        conn.unbind()

        return attributes