from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    """Модель пользователя для Petstore v3"""
    id: Optional[int] = None
    username: str
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    phone: Optional[str] = None
    userStatus: int = 0

    def to_dict(self) -> dict:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        return cls.model_validate(data)