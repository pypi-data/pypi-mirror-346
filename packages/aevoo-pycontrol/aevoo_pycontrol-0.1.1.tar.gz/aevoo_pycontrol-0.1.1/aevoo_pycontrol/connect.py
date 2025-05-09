import httpx
import json
import os
import ssl
import yaml
from getpass import getpass
from pprint import pprint
from pydantic_core import to_jsonable_python

from .graphql_client import Client as ClientLib, Login, TokenWs

HOME_PATH = f"{os.path.expanduser('~')}/.config/aevoo"
CONFIG_FILE = f"{HOME_PATH}/.cli.yml"

ws_token_header = "x-ws-token"
auth_token_header = "x-auth-token"
auth_key = "Authorization"
persist_key = "persistent-token"

cert_ = "aevoo-ca.crt"
cert_path = f"{HOME_PATH}/{cert_}"

if not os.path.exists(HOME_PATH):
    os.mkdir(HOME_PATH, 0o700)


def ca_get(url: str):
    if not os.path.exists(cert_path):
        r = httpx.get(f"{url}/{cert_}")
        with open(cert_path, "wb") as f:
            f.write(r.content)


def _is_success(response: httpx.Response):
    if not response.is_success:
        pprint(f"Failed: {response.read()} ({response.status_code})")
        return False, [response.status_code]
    response_json = response.json()
    errors = response_json.get("errors")
    if errors:
        pprint(f"Errors: {errors}")
        return False, errors
    return True, None


class Client(ClientLib):
    config: dict[str, dict[str, str]] = None
    host: str
    profile: str
    proxy: str
    __persistent_token: str = None
    __auth_token: str = None
    __ws_token: str = None

    async def execute(
        self,
        query: str,
        operation_name: str | None = None,
        variables: dict[str, any] | None = None,
        **kwargs,
    ) -> httpx.Response:
        self._headers_update()
        data_ = dict(query=query, operationName=operation_name, variables=variables)
        response = await self.http_client.post(
            url=f"https://{self.host}{self.proxy}/api/v1",
            content=json.dumps(data_, default=to_jsonable_python),
            **kwargs,
        )
        self._response_check(response, True)
        return response

    async def connect(self, *, host: str, login: bool = None, profile: str = None):
        if profile is None:
            profile = "default"
        self.host = host
        self.profile = profile
        self.proxy = ""
        headers_ = {"Content-Type": "application/json"}
        ca_get(f"https://{host}")
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.load_verify_locations(cafile=cert_path)
        self.http_client = httpx.AsyncClient(
            headers=headers_, timeout=15, verify=ssl_ctx
        )
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE) as f:
                self.config = yaml.safe_load(f.read())
        elif not login:
            print("Configuration file not found.")
            print(" 1. Authenticate")
            print(" 2. Create an account")
            response = input("Choice : ")
            match int(response):
                case 2:
                    return await self._signup()
                case 1:
                    return await self._login()
                case _:
                    print(f"Invalid choice : {response}")
                    return False, None
        if login:
            return await self._login()

        _profile = self.config.get(profile)
        if _profile:
            self.host = _profile.get("host")
            self.__persistent_token = _profile.get("persistent_token")
            if self.__persistent_token is not None:
                return True, None
        raise Exception(f"Profile '{profile}' not found in {CONFIG_FILE}")

    async def token_reset(self):
        _exist = (await self.persistent_token_exist()).persistent_token_exist
        if _exist:
            _replace = input(f"Remote token exist, replace ? [y/N] ")
            if _replace.lower() not in ("y", "yes", "oui"):
                return False, ["Cancel"]
        request = await self.persistent_token_create(_exist)
        token = request.persistent_token_create
        if self.config is None:
            self.config = {}
        self.config[self.profile] = dict(host=self.host, persistent_token=token)
        with open(CONFIG_FILE, "w") as f:
            f.write(yaml.safe_dump(self.config))
        return True, None

    async def ws_switch(self, domain_dn: str, ws_cid: str):
        variables = dict(domainDn=domain_dn, wsCid=ws_cid)
        response = await self.execute(query=token_ws, variables=variables)
        ok, err = self._response_check(response)
        if not ok:
            return False, ok
        _t = TokenWs.model_validate(self.get_data(response)).token_ws
        if _t is None:
            return False, None
        return True, _t

    def _headers_update(self):
        h = self.http_client.headers
        if self.proxy == "":
            if self.__persistent_token is None:
                if self.__auth_token is not None:
                    h[auth_key] = f"Bearer {self.__auth_token}"
            else:
                h[persist_key] = self.__persistent_token
                if h.get(auth_key) is not None:
                    del h[auth_key]
        else:
            if h.get(persist_key) is not None:
                del h[persist_key]
            if self.__ws_token is not None:
                h[auth_key] = f"Bearer {self.__ws_token}"

    async def _login(self, email: str = None, initial: bool = True):
        if email is None:
            email = os.environ.get("AEVOOSHELL_EMAIL") or input("Email: ")
        target_ = (await self.login_target(email)).login_target
        if target_ is None:
            return False, ["Unknown target"]
        self.host = f"{target_.ws_cid}.{target_.domain_dn}.aevoo.com"

        _retry = 3
        while True:
            pwd_ = os.environ.get("AEVOOSHELL_PWD") or getpass("Password: ")
            vars_ = dict(email=email, password=pwd_)
            response = await self.execute(
                query=login, operation_name="login", variables=vars_
            )
            ok, err = self._response_check(response)
            if ok:
                break
            if _retry > 1:
                _retry -= 1
                continue
            return False, err
        if initial and not os.path.exists(CONFIG_FILE):
            print(f" 1. Reset or create persistent token ? ")
            print(" 2. Don't ask again")
            print(" 3. Continue")
            response = input("Choice : ")
            match int(response):
                case 3:
                    return await self.token_reset()
                case 2:
                    with open(CONFIG_FILE, "a") as f:
                        pass
                case 1:
                    pass
                case _:
                    print(f"Invalid choice : {response}")
                    return False, None

        return True, Login.model_validate(self.get_data(response))

    async def _signup(self):
        email = input("Email: ")
        signup_ = (await self.signup(email)).signup
        if not signup_.success:
            print(signup_.msg)
            return False, None
        key = input("Token (transmitted by email): ")
        _retry = 3
        while True:
            password = input("Password: ")
            if password == input("Confirm (password): "):
                break
            _retry -= 1
            print("Passwords are different")
            commit_ = (await self.password_reset(email, key, password)).password_reset
            if not commit_.success:
                print(commit_.msg)
            if _retry <= 0:
                return False, None
        return await self._login(email=email)

    def _response_check(self, response: httpx.Response, token_only=False):
        if not token_only:
            ok, err = _is_success(response)
            if not ok:
                return False, err
            errors = response.json().get("errors")
            if errors:
                return False, [e.get("message") for e in errors]
        auth_ = response.headers.get(auth_token_header)
        if auth_:
            self.__auth_token = auth_
        ws_ = response.headers.get(ws_token_header)
        if ws_:
            self.__ws_token = ws_
        return bool(auth_ or ws_), ["Authorization token missing"]


login = """
    mutation login($email: String!, $password: String!) {
      login(email: $email, password: $password) {
        ...MeFields
      }
    }

    fragment MeFields on UserContext {
      email
      domainDn
      exp
      flag
      profile
      readOnly
      wsCid
    }
"""

token_ws = """
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
