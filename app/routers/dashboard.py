from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import func, text
from app.models.products import Product
from app.models.transactions import Transaction
from app.core.database import get_db
from app.schemas.dashboard import DashboardMetrics, TopProduct, TransactionSummary

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/metrics", response_model=DashboardMetrics)
def get_dashboard_metrics(db: Session = Depends(get_db)):
    """
    Obtiene las métricas generales del inventario.
    """
    total_products = db.query(Product).count()
    total_value = db.query(func.sum(Product.price * Product.quantity)).scalar() or 0
    recent_transactions = db.query(Transaction).filter(
        Transaction.created_at >= func.now() - text("interval '24 hours'")
    ).count()
    low_stock_products = db.query(Product).filter(Product.quantity < 5).count()

    return {
        "total_products": total_products,
        "total_value": float(total_value),
        "recent_transactions": recent_transactions,
        "low_stock_products": low_stock_products
    }

@router.get("/top-products", response_model=list[TopProduct])
def get_top_products(db: Session = Depends(get_db)):
    """
    Obtiene los productos con más transacciones.
    """
    top_products = (
        db.query(Product.id, Product.name, func.count(Transaction.id).label("transactions"))
        .join(Transaction, Transaction.product_id == Product.id)
        .group_by(Product.id, Product.name)
        .order_by(func.count(Transaction.id).desc())
        .limit(5)
        .all()
    )

    return [{"id": p.id, "name": p.name, "transactions": p.transactions} for p in top_products]

@router.get("/recent-transactions", response_model=list[TransactionSummary])
def get_recent_transactions(db: Session = Depends(get_db)):
    """
    Obtiene las últimas transacciones registradas.
    """
    transactions = (
        db.query(
            Transaction.id,
            Product.name.label("product_name"),
            Transaction.quantity_change,
            Transaction.type,
            Transaction.created_at
        )
        .join(Product, Product.id == Transaction.product_id)
        .order_by(Transaction.created_at.desc())
        .limit(10)
        .all()
    )

    return [
        {
            "id": t.id,
            "product_name": t.product_name,
            "quantity_change": t.quantity_change,
            "type": t.type,
            "created_at": t.created_at
        }
        for t in transactions
    ]