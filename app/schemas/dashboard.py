from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class DashboardMetrics(BaseModel):
    total_products: int
    total_value: float
    recent_transactions: int
    low_stock_products: int

class TopProduct(BaseModel):
    id: UUID
    name: str
    transactions: int

class TransactionSummary(BaseModel):
    id: UUID
    product_name: str
    quantity_change: int
    type: str
    created_at: datetime