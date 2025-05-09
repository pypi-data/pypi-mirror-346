"""
This file contains utility to parse URLs
This is usesful for the client
"""

import re
from dataclasses import dataclass
from typing import Optional

URL_REG = re.compile("(?:(http|https)://)?(?:([^@:]+)(?::([^@:]+))@)?([^:/]*)(?::(\d+))?(/[^\?]*)?(\?.*)")


@dataclass
class Credentials:
    username: str
    password: str | None

    def dumps(self) -> str:
        if self.password:
            return f"{self.username}:{self.password}"
        return self.username

    @staticmethod
    def build(username, password) -> Optional["Credentials"]:
        return Credentials(username, password) if username else None


@dataclass
class Host:
    scheme: str
    hostname: str
    port: int | None

    def dumps(self, credentials: Credentials | None) -> str:
        creds = f"{credentials.dumps()}@" if credentials else ""
        port = f":{self.port}" if self.port else ""
        return f"{self.scheme}://{creds}{self.hostname}{port}"
    
    @staticmethod
    def build(username, password) -> Optional["Credentials"]:
        return Credentials(username, password) if username else None


@dataclass
class URL:
    url: str 
    host: Host
    credentials: Credentials | None
    route: str
    params: str

    @property
    def ssl(self) -> bool:
        return self.scheme == "https"
    

    @staticmethod
    def from_url(url: str) -> "URL":
        """
        Clean the url:
        * Add scheme if missing
        * Remove trailing slash and path
        * Extract the host
        """
        scheme, username, password, host, port, route, params = URL_REG.match(url).groups()
        return URL(
            url=url,
            host=Host(scheme, host, port),
            credentials=Credentials.build(username, password),
            route=route,
            params=params,
        )
    
    def get_host(self, with_credentials=False) -> str:
        credentials = self.credentials if with_credentials else None
        host = self.host.dumps(credentials)
        return host
    
    def get_url(self, with_credentials=False) -> str:
        host = self.get_host(with_credentials=with_credentials)
        params = self.params
        if params:
            params = f"?{params}"
        url = f"{host}{self.route}{params}"
        return url