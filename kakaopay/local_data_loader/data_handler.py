
from abc import ABC, abstractmethod


class DataHandler(ABC):
    @abstractmethod
    async def handle(self, data_iter: iter):
        pass
