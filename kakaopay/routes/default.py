
from typing import TYPE_CHECKING

from sanic_restful import Resource
from sqlalchemy.sql import func

from .auth import authorized
from .utils import db_connect, db_close, convert_response

from ..constant.constant import ResponseCode
from ..database.sqlite_database import SqliteDataBase
from ..database.models import Institute, Bank
from ..load_local_data.load_local_data import load_local_data


if TYPE_CHECKING:
    from sqlalchemy.orm import Session
    from sanic.response import HTTPResponse
    from sanic.request import Request


class Api1(Resource):
    method_decorators = {"post": authorized}

    async def post(self, request: 'Request') -> 'HTTPResponse':
        try:
            await load_local_data()
        except:
            return await convert_response({"msg": "already exist DB"}, ResponseCode.RESPONSE_ERROR)
        return await convert_response({"msg": "init DB"})


class Api2(Resource):
    method_decorators = {"get": authorized}

    async def get(self, request: 'Request') -> 'HTTPResponse':
        await db_connect()
        session = SqliteDataBase.create_session()
        res = await self._logic(session)
        await db_close(session)
        return res

    async def _logic(self, session: 'Session') -> 'HTTPResponse':
        data: list = []
        for ins in session.query(Institute.institute_name).order_by(Institute.id):
            data.append(ins.institute_name)
        return await convert_response({"bank": data})


class Api3(Resource):
    method_decorators = {"get": authorized}

    async def get(self, request: 'Request') -> 'HTTPResponse':
        await db_connect()
        session = SqliteDataBase.create_session()
        res = await self._logic(session)
        await db_close(session)
        return res

    async def _logic(self, session: 'Session') -> 'HTTPResponse':
        content: list = []
        total_sum = {}
        detail_sum = {}

        # SELECT b.institute_name, a.year, sum(a.value) FROM bank a \
        # JOIN institute b on a.institute_code = b.institute_code GROUP BY a.institute_code, a.year

        # SELECT year, sum(value) FROM bank GROUP BY year

        for year, value in session.query(Bank.year, func.sum(Bank.value)).group_by(Bank.year):
            total_sum[year] = value

        for year, name, value in session.query(Bank.year, Institute.institute_name, func.sum(Bank.value)).\
                join(Institute, Institute.institute_code == Bank.institute_code).\
                group_by(Bank.institute_code, Bank.year):
            if year not in detail_sum:
                detail_sum[year] = {}
            detail_sum[year][name] = value

        for year, value in total_sum.items():
            data = {"year": f"{year}",
                    "total_amount": value,
                    "detail_amount": detail_sum[year]}
            content.append(data)

        return await convert_response({"name": "주택금융 공급현황", "content": content})


class Api4(Resource):
    method_decorators = {"get": authorized}

    async def get(self, request: 'Request') -> 'HTTPResponse':
        await db_connect()
        session = SqliteDataBase.create_session()
        res = await self._logic(session)
        await db_close(session)
        return res

    async def _logic(self, session: 'Session') -> 'HTTPResponse':

        """
        SELECT institute_code, year, max(amountsum)
        FROM (
        SELECT institute_code, year, sum(value) as amountsum
        FROM bank
        GROUP BY institute_code, year
        )
        """

        stmt = session.query(Bank.institute_code, Bank.year, func.sum(Bank.value).label("sum")).\
            group_by(Bank.institute_code, Bank.year).subquery()

        data = session.query(Institute.institute_name, stmt.c.year, func.max(stmt.c.sum)). \
            join(Institute, Institute.institute_code == stmt.c.institute_code).one()

        return await convert_response({"bank": data[0],
                                       "year": data[1]})


class Api5(Resource):
    method_decorators = {"get": authorized}

    async def get(self, request: 'Request') -> 'HTTPResponse':
        await db_connect()
        session = SqliteDataBase.create_session()
        res = await self._logic(session)
        await db_close(session)
        return res

    async def _logic(self, session: 'Session') -> 'HTTPResponse':

        """
        SELECT year, max(am)
        FROM (
        SELECT institute_code, year, avg(value) as am
        FROM bank
        WHERE institute_code == 'bnk3008'
        GROUP BY year
        )
        """

        stmt = session.query(Bank.institute_code, Bank.year, func.avg(Bank.value).label("avg")).\
            filter(Bank.institute_code == "bnk3008").group_by(Bank.year).subquery()

        year, value = session.query(stmt.c.year, func.min(stmt.c.avg)).one()
        min_data = {"year": year, "amount": value}
        year, value = session.query(stmt.c.year, func.max(stmt.c.avg)).one()
        max_data = {"year": year, "amount": value}

        return await convert_response({"bank": "외환은행",
                                       "support_amount": [min_data, max_data]})
