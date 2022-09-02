from abc import abstractmethod, ABCMeta
from typing import Generic, List, TypeVar

from pydantic import BaseModel

from app.common.database import Base

M = TypeVar("M", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository(Generic[M, CreateSchemaType, UpdateSchemaType], metaclass=ABCMeta):
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
