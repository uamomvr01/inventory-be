from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class TransactionBase(BaseModel):
    product_id: UUID
    quantity_change: int
    type: str  # Puede ser "In" o "OUT"

class TransactionCreate(TransactionBase):
    created_by: UUID

class TransactionResponse(TransactionBase):
    id: UUID
    created_by: UUID
    created_at: datetime

    class Config:
        from_attributes = True