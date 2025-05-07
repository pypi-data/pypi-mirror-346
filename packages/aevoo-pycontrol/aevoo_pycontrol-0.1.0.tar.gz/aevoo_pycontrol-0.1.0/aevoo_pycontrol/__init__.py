from __future__ import annotations

import httpx
import json
import os
import yaml
from dataclasses import dataclass
from getpass import getpass
from typing import TYPE_CHECKING

from aevoo_pycontrol.graphql_client import Client, TokenWs

if TYPE_CHECKING:
    from aevoo_pycontrol.graphql_client import TokenWsTokenWs

ws_token_header = "x-ws-token"

query = """
    mutation tokenWs($domainDn: String, $wsCid: String) {
      tokenWs(domainDn: $domainDn, wsCid: $wsCid) {
          domainDn
          email
          exp
          flag
          profile
          readOnly
          wsCid
      }
    }
    """

HOME_PATH = f"{os.path.expanduser('~')}/.config/aevoo"
CONFIG_FILE = f"{HOME_PATH}/.cli.yml"


def _config_get(target: str = "default"):
    with open(CONFIG_FILE) as f:
        content = f.read()
    config: dict[str, dict[str, str]] = yaml.safe_load(content)
    _profile = config.get(target)
    if _profile:
        return Config(**_profile)
    raise Exception(f"Profile '{target}' not found in {CONFIG_FILE}")


def _config_write():
    if not os.path.exists(HOME_PATH):
        os.mkdir(HOME_PATH, 0o700)
    host = "https://console.aevoo.fr"
    login = input("Login: ")
    password = getpass("Password: ")
    config_ = dict()


@dataclass
class Config:
    host: str = "console.aevoo.fr"
    port: int = 443
    persistent_token: str = None


class Context:
    config: Config
    headers: dict[str, str]
    root_domain_dn: str = None
    root_url: str
    root_ws_cid: str = None
    token_level: int
    url: str
    user_ctx: TokenWsTokenWs

    @property
    def api(self) -> Client:
        http_client = httpx.AsyncClient(
            headers=self.headers,
            timeout=30,
        )
        return Client(f"{self.url}/api/v1", http_client=http_client)

    async def connect(self, target: str = "default"):
        if not os.path.exists(CONFIG_FILE):
            if input(
                "Configuration file not found, initialize the configuration file (~/.config/aevoo/.cli.yml) with a persistent token (y/N) ? "
            ).lower() not in ("y", "yes", "oui", 1):
                raise Exception("Configuration not found")

        self.config = _config_get(target)

        self.root_url = f"https://{self.config.host}:{self.config.port}"
        await self._ws_ctx_load()
        self.root_domain_dn = self.user_ctx.domain_dn
        self.root_ws_cid = self.user_ctx.ws_cid
        self.token_level = 0

    async def switch(self, domain_dn: str, ws_cid: str, auth_dn: str = None):
        ok, token = await self._ws_ctx_load()
        if not ok:
            return False, token
        if domain_dn == self.root_domain_dn and ws_cid == self.root_ws_cid:
            self.token_level = 0
            return ok, token

        if auth_dn is None:
            self.token_level = 1
            return await self._ws_ctx_load(domain_dn=domain_dn, ws_cid=ws_cid)

        _auth_fields = auth_dn.split(".")
        _auth_ws_cid = _auth_fields[0]
        if len(_auth_fields) == 1:
            _auth_dom_dn = domain_dn
        else:
            _auth_dom_dn = auth_dn[1]

        ok, token = await self._ws_ctx_load(domain_dn=_auth_dom_dn, ws_cid=_auth_ws_cid)
        if not ok:
            return False, token
        if _auth_dom_dn == self.root_domain_dn and _auth_ws_cid == self.root_ws_cid:
            self.token_level = 1
            return ok, token

        self.token_level = 2
        return await self._ws_ctx_load(domain_dn=domain_dn, ws_cid=ws_cid)

    async def _ws_ctx_load(self, *, domain_dn: str = None, ws_cid: str = None):
        _r_dom = domain_dn in (None, self.root_domain_dn)
        _r_ws = ws_cid in (None, self.root_ws_cid)
        _is_root = _r_dom and _r_ws
        if _is_root:
            self.url = self.root_url
            self.headers = {"persistent-token": self.config.persistent_token}

        variables = dict(domainDn=domain_dn, wsCid=ws_cid)
        api = self.api
        response = await api.execute(query=query, variables=variables)
        if response.status_code != 200:
            raise Exception(f"Connection failed : {response.status_code}")
        content = json.loads(response.content.decode())
        _t = TokenWs.model_validate(api.get_data(response)).token_ws
        if _t is None:
            return False, None

        if domain_dn not in (None, _t.domain_dn) or ws_cid not in (None, _t.ws_cid):
            return False, _t

        for key, value in response.headers.raw:
            if key.lower() == ws_token_header.encode():
                self.user_ctx = _t
                if not _is_root:
                    self.url = f"{self.root_url}/proxy/{domain_dn}/{ws_cid}"
                token = value.decode()
                self.headers = {"Authorization": f"Bearer {token}"}
                return True, _t
        else:
            raise Exception([e.get("message") for e in content.get("errors")])
