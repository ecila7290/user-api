from typing import Type, Generic, TypeVar, List, Dict

from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.common.database import get_db
from app.common.exceptions import EntityNotFoundException
from app.common.repository.base_repository import BaseRepository, M

CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class SqliteRepository(BaseRepository[M], Generic[CreateSchemaType, UpdateSchemaType]):
    Entity: Type[M]

    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    def create(self, entity: CreateSchemaType) -> Entity:
        db_entity = self.Entity(**entity.dict())
        self.db.add(db_entity)
        self.db.commit()
        self.db.refresh(db_entity)
        return db_entity

    def read(self, id: str) -> Entity:
        entity = self.db.query(self.Entity).filter(self.Entity.id == id).first()
        if entity is None:
            raise EntityNotFoundException(id=id, entity_type=self.Entity)
        return entity

    def query(self, offset: int = 0, limit: int = 20, filters: Dict = {}) -> List[Entity]:
        query = self.db.query(self.Entity)
        for _filter, value in filters.items():
            query = query.filter(_filter == value)
        return query.offset(offset).limit(limit).all()

    def update(self, id: str, entity: UpdateSchemaType) -> Entity:
        current_data = self.db.query(self.Entity).filter(self.Entity.id == id).first()
        if current_data is None:
            raise EntityNotFoundException(id=id, entity_type=self.Entity)

        entity_dict = entity.dict(exclude_unset=True)
        for key, value in entity_dict.items():
            setattr(current_data, key, value)

        self.db.add(current_data)
        self.db.commit()
        self.db.refresh(current_data)
        return current_data

    def delete(self, id: str) -> None:
        current_data = self.db.query(self.Entity).filter(self.Entity.id == id).first()
        if current_data is None:
            raise EntityNotFoundException(id=id, entity_type=self.Entity)
        self.db.delete(current_data)
        self.db.commit()
