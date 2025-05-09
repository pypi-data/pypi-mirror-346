from __future__ import annotations

import httpx
import os
from typing import TYPE_CHECKING

from .connect import Client

if TYPE_CHECKING:
    from .graphql_client import TokenWsTokenWs

HOST_DEFAULT = "console.aevoo.com"
HOME_PATH = f"{os.path.expanduser('~')}/.config/aevoo"
CONFIG_FILE = f"{HOME_PATH}/.cli.yml"


class Context:
    api: Client
    auth_dn: str = None
    auth_ws: str = None
    user_ctx: TokenWsTokenWs
    _client_: Client
    _http_client_: httpx.AsyncClient

    async def connect(
        self, *, host: str = None, login: bool = None, profile: str = None
    ):
        self.api = Client()
        if host is None:
            host = HOST_DEFAULT
        ok, err = await self.api.connect(host=host, login=login, profile=profile)
        if not ok:
            raise Exception(err)
        ok, err = await self._ws_ctx_load()
        if not ok:
            raise Exception(err)
        self.auth_dn = self.user_ctx.domain_dn
        self.auth_ws = self.user_ctx.ws_cid

    async def switch(self, domain_dn: str, ws_cid: str):
        ok, token = await self._ws_ctx_load()
        if not ok or domain_dn == self.auth_dn and ws_cid == self.auth_ws:
            return ok, token

        return await self._ws_ctx_load(domain_dn=domain_dn, ws_cid=ws_cid)

    async def _ws_ctx_load(self, *, domain_dn: str = None, ws_cid: str = None):
        _r_dom = domain_dn in (None, self.auth_dn)
        _r_ws = ws_cid in (None, self.auth_ws)
        _is_root = _r_dom and _r_ws
        if _is_root:
            self.api.proxy = ""

        ok, _t = await self.api.ws_switch(domain_dn, ws_cid)

        if not ok or not (
            domain_dn in (None, _t.domain_dn) and ws_cid in (None, _t.ws_cid)
        ):
            return False, _t

        self.user_ctx = _t
        if not _is_root:
            self.api.proxy = f"/proxy/{domain_dn}/{ws_cid}"
        return True, _t
