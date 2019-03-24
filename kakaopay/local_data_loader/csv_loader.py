
import csv
from typing import TYPE_CHECKING

from ..local_data_loader.data_loader import DataLoader

if TYPE_CHECKING:
    from ..local_data_loader.data_handler import DataHandler


class CSVLoader(DataLoader):

    @classmethod
    async def load(cls, path: str, handler: 'DataHandler', encoding: str = 'utf-8'):
        cls._handler = handler
        await CSVLoader._get_reader(path, encoding=encoding)

    @classmethod
    async def _get_reader(cls, filename: str, encoding: str, delimiter: str = ','):
        with open(filename, "r", newline='', encoding=encoding) as csv_file:
            reader = csv.reader(csv_file, delimiter=delimiter)
            if cls._handler:
                await cls._handler.handle(reader)
            else:
                raise Exception("No Data Handler")
