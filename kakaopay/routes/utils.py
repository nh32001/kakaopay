import json
import os
from typing import TYPE_CHECKING

import jwt
from sanic import response

from ..constant.constant import ROOT_DB_PATH, JWT_SECRET, AUTH_ALGORITHM
from ..database.sqlite_database import SqliteDataBase


if TYPE_CHECKING:
    from sqlalchemy.orm import Session


async def db_connect():
    db_path = os.path.abspath(os.path.join(ROOT_DB_PATH, 'data.sqlite'))
    SqliteDataBase.open(db_path)


async def db_close(session: 'Session'):
    SqliteDataBase.close(session)


async def convert_response(data: dict, status = 200):
    return response.json(data, status=status, dumps=json.dumps)


async def jwt_encode(account_id: str, valid_timestamp: float) -> bytes:
    return jwt.encode({'id': account_id, "valid_time": valid_timestamp}, JWT_SECRET, algorithm=AUTH_ALGORITHM)


async def jwt_decode(token: bytes) -> dict:
    return jwt.decode(token, JWT_SECRET, algorithms=AUTH_ALGORITHM)