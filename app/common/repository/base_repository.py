from abc import abstractmethod, ABCMeta
from typing import Generic, List, TypeVar

from app.common.database import Base

M = TypeVar("M", bound=Base)


class BaseRepository(Generic[M], metaclass=ABCMeta):
    @abstractmethod
    def create(self, entity: M) -> M:
        pass

    @abstractmethod
    def read(self, id: str) -> M:
        pass

    @abstractmethod
    def query(self, **kwargs) -> List[M]:
        pass

    @abstractmethod
    def update(self, id: str, entity: M) -> M:
        pass

    @abstractmethod
    def delete(self, id: str) -> None:
        pass
