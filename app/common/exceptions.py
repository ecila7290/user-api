from typing import Type

from app.common.repository.base_repository import M


class EntityNotFoundException(Exception):
    def __init__(self, id: str, entity_type: Type[M]) -> None:
        self.id = id
        self.entity_type = entity_type

    def __str__(self) -> str:
        return f"{self.entity_type.__name__} with id: {id} does not exist."


class ConflictException(Exception):
    def __init__(self, message) -> None:
        self.message = message

    def __str__(self) -> str:
        return f"Conflict exception: {self.message}"
