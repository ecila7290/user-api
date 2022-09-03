from typing import Type, List, Dict

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.common.exceptions import EntityNotFoundException, ConflictException
from app.common.repository.base_repository import BaseRepository, M


class SqliteRepository(BaseRepository[M]):
    Entity: Type[M]
    db: Session

    def create(self, entity: M) -> M:
        try:
            self.db.add(entity)
            self.db.commit()
            self.db.refresh(entity)
        except IntegrityError as e:
            raise ConflictException(str(e))
        return entity

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

    def update(self, id: str, entity: M) -> M:
        entity_to_update = self.db.query(self.Entity).filter(self.Entity.id == id).first()
        if entity_to_update is None:
            raise EntityNotFoundException(id=id, entity_type=self.Entity)

        for key, value in entity.__dict__.items():
            setattr(entity_to_update, key, value)

        self.db.add(entity_to_update)
        self.db.commit()
        self.db.refresh(entity_to_update)
        return entity_to_update

    def delete(self, id: str) -> None:
        current_data = self.db.query(self.Entity).filter(self.Entity.id == id).first()
        if current_data is None:
            raise EntityNotFoundException(id=id, entity_type=self.Entity)
        self.db.delete(current_data)
        self.db.commit()
