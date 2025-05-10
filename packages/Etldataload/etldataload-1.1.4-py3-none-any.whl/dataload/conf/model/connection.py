from dataclasses import dataclass

@dataclass
class Headers:
    token: str
    content_type: str

@dataclass
class Csv:
    path: str

@dataclass
class RestAPI:
    base_url: str
    key: str
    headers: Headers

@dataclass
class Postgresql:
    host: str
    user: str
    password: str
    timeout: int
    max_retries: int
    port: int
    database: str

@dataclass
class Mysql:
    host: str
    user: str
    password: str
    port: int
    database: str

@dataclass
class Connection:
    alias: str
    type: str
    csv : Csv = None
    restapi: RestAPI = None
    postgresql: Postgresql = None
    mysql: Mysql = None