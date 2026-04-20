from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field


class PetStatus(str, Enum):
    AVAILABLE = "available"
    PENDING = "pending"
    SOLD = "sold"


class Category(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class Tag(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class Pet(BaseModel):
    """Модель питомца для Petstore v3"""
    id: Optional[int] = None
    category: Optional[Category] = None
    name: str = Field(..., min_length=1)
    photoUrls: List[str] = Field(default_factory=list)  # Обязательное поле
    tags: Optional[List[Tag]] = Field(default_factory=list)
    status: Optional[str] = None  # API принимает любую строку

    def to_dict(self) -> dict:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(cls, data: dict) -> "Pet":
        return cls.model_validate(data)