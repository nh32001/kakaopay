from typing import TYPE_CHECKING
from abc import abstractmethod, ABC

if TYPE_CHECKING:
    from ..local_data_loader.data_handler import DataHandler


class DataLoader(ABC):
    _handler: 'DataHandler' = None

    @classmethod
    @abstractmethod
    async def load(cls, path: str, handler: 'DataHandler', encoding: str = 'utf-8'):
        pass

    @classmethod
    @abstractmethod
    async def _get_reader(cls, filename: str, encoding: str, delimiter: str = ','):
        pass
