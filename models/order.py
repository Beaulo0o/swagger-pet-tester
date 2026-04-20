"""
Модели для заказов (Order)
"""
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class OrderStatus(str, Enum):
    """Статусы заказа"""
    PLACED = "placed"
    APPROVED = "approved"
    DELIVERED = "delivered"


class Order(BaseModel):
    """
    Модель заказа питомца
    Соответствует схеме Petstore API
    """
    id: Optional[int] = None
    petId: int = Field(..., gt=0, description="ID питомца")
    quantity: int = Field(default=1, ge=1, le=100, description="Количество")
    shipDate: Optional[datetime] = None
    status: Optional[OrderStatus] = Field(default=OrderStatus.PLACED, description="Статус заказа")
    complete: bool = Field(default=False, description="Завершён ли заказ")

    class Config:
        from_attributes = True

    @field_validator('petId')
    @classmethod
    def pet_id_must_be_positive(cls, v: int) -> int:
        """Валидация ID питомца"""
        if v <= 0:
            raise ValueError('petId must be positive')
        return v

    @field_validator('quantity')
    @classmethod
    def quantity_must_be_valid(cls, v: int) -> int:
        """Валидация количества"""
        if v < 1:
            raise ValueError('quantity must be at least 1')
        if v > 100:
            raise ValueError('quantity cannot exceed 100')
        return v

    def to_dict(self) -> dict:
        """Конвертация в словарь (исключая None значения)"""
        data = self.model_dump(exclude_none=True, by_alias=True)
        # Конвертируем datetime в строку ISO формата
        if 'shipDate' in data and data['shipDate']:
            data['shipDate'] = data['shipDate'].isoformat()
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Order":
        """Создание из словаря"""
        # Парсим дату, если она есть
        if 'shipDate' in data and data['shipDate']:
            data['shipDate'] = datetime.fromisoformat(data['shipDate'].replace('Z', '+00:00'))
        return cls.model_validate(data)

    def __str__(self) -> str:
        return f"Order(id={self.id}, petId={self.petId}, status={self.status})"