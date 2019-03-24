
import os
import re
from typing import TYPE_CHECKING

from ..constant.constant import ROOT_DB_PATH, ROOT_CSV_PATH
from ..local_data_loader.data_handler import DataHandler
from ..local_data_loader.csv_loader import CSVLoader
from ..database.sqlite_database import SqliteDataBase
from ..database.models import Institute, Bank

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


class BankHandler(DataHandler):
    regex = re.compile('[^ ㄱ-ㅣ가-힣/]+')

    def __init__(self, db_path: str):
        self.db_path: str = db_path

    async def handle(self, data_iter: iter):
        SqliteDataBase.open(self.db_path)
        session = SqliteDataBase.create_session()
        if session.query(Institute).count() > 0:
            raise Exception("already exist DB")
        for row_index, row in enumerate(data_iter):
            row = [x for x in row if x != ""]
            if row_index == 0:
                await self._make_institute_table(row, session)
            else:
                await self._make_bank_table(row, session)
        session.commit()
        SqliteDataBase.close(session)

    async def _make_institute_table(self, row: list, session: 'Session'):
        prefix = "bnk"
        bank_index = 3000
        for index, name in enumerate(row[2:]):
            name = self.regex.sub('', name[:-4])
            ins = Institute(name, prefix+str(bank_index + index + 1))
            session.add(ins)

    async def _make_bank_table(self, row: list, session: 'Session'):
        year = int(row[0])
        month = int(row[1])

        prefix = "bnk"
        bank_index = 3000
        for index, value in enumerate(row[2:]):
            value = int(value.replace(",", ""))
            code = prefix + str(bank_index + index + 1)
            bnk = Bank(code, year, month, value)
            session.add(bnk)


async def load_local_data():
    data_path = os.path.abspath(os.path.join(ROOT_CSV_PATH, 'data.csv'))
    db_path = os.path.abspath(os.path.join(ROOT_DB_PATH, 'data.sqlite'))
    await CSVLoader.load(data_path, BankHandler(db_path), encoding='euc_kr')
