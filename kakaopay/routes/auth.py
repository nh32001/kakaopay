
from datetime import datetime
from functools import wraps
from typing import TYPE_CHECKING, Tuple

from jwt import InvalidSignatureError

from sanic_restful import Resource
from sqlalchemy.orm.exc import NoResultFound

from ..constant.constant import ResponseCode
from ..database.sqlite_database import SqliteDataBase
from ..database.models import Account
from .utils import db_connect, db_close, convert_response, jwt_encode, jwt_decode

if TYPE_CHECKING:
    from sqlalchemy.orm import Session
    from sanic.response import HTTPResponse
    from sanic.request import Request


def authorized(f):
    @wraps(f)
    async def decorated_function(request):
        # run some method that checks the request
        # for the client's authorization status
        is_authorized = await check_request_for_authorization_status(request)

        if is_authorized:
            # the user is authorized.
            # run the handler method and return the response
            res = await f(request)
            return res
        else:
            # the user is not authorized.
            return await convert_response({'status': 'not_authorized'}, ResponseCode.AUTH_ERROR)
    return decorated_function


async def check_request_for_authorization_status(request: 'Request') -> bool:
    await db_connect()
    session = SqliteDataBase.create_session()

    header = request.headers.get("Authorization")
    if header is None:
        return False

    tokens = header.split(' ')
    if len(tokens) != 2:
        return False

    t_type = tokens[0]
    if t_type != 'basic':
        return False

    token: str = tokens[1]

    try:
        payload: dict = await jwt_decode(token.encode())
    except InvalidSignatureError:
        return False

    try:
        session.query(Account).filter(Account.account_id == payload['id']).one()
    except NoResultFound:
        return False

    # TODO check valid type
    return True


class SignUp(Resource):
    async def post(self, request: 'Request') -> 'HTTPResponse':
        await db_connect()
        session = SqliteDataBase.create_session()
        res = await self._logic(session, request)
        await db_close(session)
        return res

    async def _logic(self, session: 'Session', request: 'Request') -> 'HTTPResponse':
        req_json = request.json

        account_id = req_json.get("id")
        if account_id is None:
            return await convert_response({"error": "account id is empty"}, ResponseCode.RESPONSE_ERROR)
        account_pwd = req_json.get("pw")
        if account_pwd is None:
            return await convert_response({"error": "account pw is empty"}, ResponseCode.RESPONSE_ERROR)

        user = session.query(Account).filter(Account.account_id == account_id).first()
        if user:
            return await convert_response({"msg": f"already exist account"}, ResponseCode.RESPONSE_ERROR)

        account = Account(account_id, account_pwd)
        session.add(account)
        session.commit()

        token: bytes = await jwt_encode(account_id, account.valid_token_time.timestamp())
        return await convert_response({"token": token.decode()})


class SignIn(Resource):
    async def put(self, request: 'Request') -> 'HTTPResponse':
        await db_connect()
        session = SqliteDataBase.create_session()
        res = await self._logic(session, request)
        await db_close(session)
        return res

    async def _logic(self, session: 'Session', request: 'Request') -> 'HTTPResponse':
        req_json = request.json

        account_id = req_json.get("id")
        if account_id is None:
            return await convert_response({"error": "account id is empty"}, ResponseCode.RESPONSE_ERROR)
        account_pwd = req_json.get("pw")
        if account_pwd is None:
            return await convert_response({"error": "account pw is empty"}, ResponseCode.RESPONSE_ERROR)

        try:
            user = session.query(Account).filter(Account.account_id == account_id).one()
        except NoResultFound:
            return await convert_response({"msg": f"account is empty"}, ResponseCode.RESPONSE_ERROR)

        if user.account_pwd != account_pwd:
            return await convert_response({"error": "invalid pw"}, ResponseCode.RESPONSE_ERROR)

        session.commit()

        token: bytes = await jwt_encode(account_id, user.valid_token_time.timestamp())
        return await convert_response({"token": token.decode()})


class RefreshToken(Resource):
    async def put(self, request: 'Request') -> 'HTTPResponse':
        await db_connect()
        session = SqliteDataBase.create_session()
        res = await self._logic(session, request)
        await db_close(session)
        return res

    async def _logic(self, session: 'Session', request: 'Request') -> 'HTTPResponse':
        ret: Tuple[bool, str] = await self._valid_header(request)
        ret_bool, ret_token = ret

        if not ret_bool:
            return await convert_response({"error": "invalid refresh token"}, ResponseCode.RESPONSE_ERROR)

        try:
            payload: dict = await jwt_decode(ret_token.encode())
        except InvalidSignatureError:
            return await convert_response({"error": "invalid refresh token"}, ResponseCode.RESPONSE_ERROR)

        try:
            user = session.query(Account).filter(Account.account_id == payload['id']).one()
        except NoResultFound:
            return await convert_response({"msg": f"account is empty"}, ResponseCode.RESPONSE_ERROR)

        user.valid_token_time = datetime.utcnow()
        session.commit()

        token: bytes = await jwt_encode(user.account_id, user.valid_token_time.timestamp())
        return await convert_response({"token": token.decode()})

    async def _valid_header(self, request: 'Request') -> tuple:
        header = request.headers.get("Authorization")

        if header is None:
            return False, ""

        tokens = header.split(' ')
        if len(tokens) != 2:
            return False, ""

        t_type = tokens[0]
        if t_type != 'bearer':
            return False, ""

        token: str = tokens[1]
        return True, token
