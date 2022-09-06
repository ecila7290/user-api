from typing import Type, Union

from app.common.repository.base_repository import M


class BadRequestException(Exception):
    def __init__(self, message) -> None:
        self.message = message

    def __str__(self) -> str:
        return self.message


class EntityNotFoundException(Exception):
    def __init__(self, id: str, entity_type: Union[Type[M], str]) -> None:
        self.id = id
        self.entity_type = entity_type

    def __str__(self) -> str:
        return f"{self.entity_type if type(self.entity_type) is str else self.entity_type.__name__} with id: {self.id} does not exist."


class ConflictException(Exception):
    def __init__(self, message) -> None:
        self.message = message

    def __str__(self) -> str:
        return f"Conflict exception: {self.message}"


class InvalidValueException(Exception):
    def __init__(self, message) -> None:
        self.message = message

    def __str__(self) -> str:
        return self.message


class UnauthorizedException(Exception):
    def __init__(self, message) -> None:
        self.message = message

    def __str__(self) -> str:
        return self.message
