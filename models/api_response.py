from typing import Optional
from pydantic import BaseModel


class ApiResponse(BaseModel):
    """Стандартный ответ API"""
    code: Optional[int] = None
    type: Optional[str] = None
    message: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "ApiResponse":
        return cls.model_validate(data)