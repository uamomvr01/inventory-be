from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class ProductBase(BaseModel):
    name: str
    description: str
    quantity: int
    price: float

class ProductCreate(ProductBase):
    created_by: UUID

class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    quantity: int | None = None
    price: float | None = None

class ProductResponse(ProductBase):
    id: UUID
    created_by: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True