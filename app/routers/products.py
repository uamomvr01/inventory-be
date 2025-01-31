from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.products import Product
from app.models.transactions import Transaction
from app.schemas.products import ProductCreate, ProductUpdate, ProductResponse
from uuid import UUID

router = APIRouter(prefix="/products", tags=["products"])

@router.get("", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    """
    Obtiene todos los productos del inventario.
    """
    return db.query(Product).all()


@router.post("", response_model=ProductResponse)
def create_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo producto en el inventario.
    """
    product = Product(**product_data.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: UUID, product_data: ProductUpdate, db: Session = Depends(get_db)):
    """
    Modifica un producto existente en el inventario.
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Actualizar solo los campos que se envían en la solicitud
    update_data = product_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}")
def delete_product(product_id: UUID, db: Session = Depends(get_db)):
    """
    Elimina un producto del inventario junto con sus transacciones asociadas.
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Eliminar transacciones asociadas antes de eliminar el producto
    db.query(Transaction).filter(Transaction.product_id == product_id).delete(synchronize_session=False)

    db.delete(product)
    db.commit()

    return {"message": "Producto y transacciones asociadas eliminados correctamente"}
