from typing import Type, List, Dict

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.common.exceptions import EntityNotFoundException, ConflictException
from app.common.repository.base_repository import BaseRepository, M, CreateSchemaType, UpdateSchemaType


class SqliteRepository(BaseRepository[M, CreateSchemaType, UpdateSchemaType]):
    Entity: Type[M]
    db: Session

    def create(self, entity: CreateSchemaType) -> M:
        db_entity = self.Entity(**entity.dict())
        try:
            self.db.add(db_entity)
            self.db.commit()
            self.db.refresh(db_entity)
        except IntegrityError as e:
            raise ConflictException(str(e))
        return db_entity

    def read(self, id: str) -> M:
        entity = self.db.query(self.Entity).filter(self.Entity.id == id).first()
        if entity is None:
            raise EntityNotFoundException(id=id, entity_type=self.Entity)
        return entity

    def query(self, offset: int = 0, limit: int = 20, filters: Dict = {}) -> List[M]:
        query = self.db.query(self.Entity)
        for _filter, value in filters.items():
            query = query.filter(_filter == value)
        return query.offset(offset).limit(limit).all()

    def update(self, id: str, entity: UpdateSchemaType) -> M:
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
