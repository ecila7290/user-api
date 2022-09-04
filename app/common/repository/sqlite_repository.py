import datetime
from typing import Type, List, Dict

from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.common.exceptions import EntityNotFoundException, ConflictException
from app.common.repository.base_repository import BaseRepository, M

# TODO: sqlite에 timezone aware한 형태로 저장하려 했으나 불가능하여
# 엔티티를 반환할 때 datetime을 timezone aware하게 만들어서 반환하도록 함 추후 수정 필요.
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
        for field, value in entity.__dict__.items():
            if type(value) is datetime.datetime:
                setattr(entity, field, value.replace(tzinfo=datetime.timezone.utc))
        return entity

    def read(self, id: str) -> M:
        entity = self.db.query(self.Entity).filter(self.Entity.id == id).first()
        if entity is None:
            raise EntityNotFoundException(id=id, entity_type=self.Entity)
        for field, value in entity.__dict__.items():
            if type(value) is datetime.datetime:
                setattr(entity, field, value.replace(tzinfo=datetime.timezone.utc))
        return entity

    def query(self, offset: int = 0, limit: int = 20, filters: Dict = {}, sort: List[str] = []) -> List[M]:
        query = self.db.query(self.Entity)
        if filters:
            for _filter, value in filters.items():
                query = query.filter(getattr(self.Entity, _filter) == value)
        if sort:
            for field in sort:
                if field.startswith("-"):
                    query = query.order_by(desc(field[1:]))
                else:
                    query = query.order_by(field)
        entities = query.offset(offset).limit(limit).all()
        for entity in entities:
            for field, value in entity.__dict__.items():
                if type(value) is datetime.datetime:
                    setattr(entity, field, value.replace(tzinfo=datetime.timezone.utc))
        return entities

    def update(self, id: str, entity: M) -> M:
        entity_to_update = self.db.query(self.Entity).filter(self.Entity.id == id).first()
        if entity_to_update is None:
            raise EntityNotFoundException(id=id, entity_type=self.Entity)

        for key, value in entity.__dict__.items().items():
            setattr(entity_to_update, key, value)

        self.db.add(entity_to_update)
        self.db.commit()
        self.db.refresh(entity_to_update)
        for field, value in entity_to_update.__dict__.items():
            if type(value) is datetime.datetime:
                setattr(entity_to_update, field, value.replace(tzinfo=datetime.timezone.utc))
        return entity_to_update

    def delete(self, id: str) -> None:
        current_data = self.db.query(self.Entity).filter(self.Entity.id == id).first()
        if current_data is None:
            raise EntityNotFoundException(id=id, entity_type=self.Entity)
        self.db.delete(current_data)
        self.db.commit()
