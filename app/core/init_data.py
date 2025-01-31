from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.products import Product
from app.models.transactions import Transaction
from app.models.users import User
from app.core.security import hash_password
import uuid
import random

def seed_database(db: Session):
    """Verifica si hay datos y, si no, los inserta."""
    if db.query(Product).first():
        print("⚡ La base de datos ya tiene datos. No es necesario inicializar.")
        return

    print("Insertando datos iniciales en la base de datos...")

    # Crear usuario administrador
    admin_email = "admin@example.com"
    admin_password = "admin123"
    admin_user = User(
        id=uuid.uuid4(),
        email=admin_email,
        password_hash=hash_password(admin_password),
        full_name="Admin User"
    )
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)

    # Datos de productos
    products_data = [
        ("Laptop HP ProBook", "Laptop empresarial con procesador i5, 8GB RAM, 256GB SSD", 15, 899.99),
        ("Monitor Dell 24\"", "Monitor LED Full HD 1080p con panel IPS", 20, 249.99),
        ("Teclado Mecánico", "Teclado mecánico con switches Cherry MX", 30, 79.99),
        ("Mouse Inalámbrico", "Mouse ergonómico con batería de larga duración", 50, 29.99),
        ("Impresora Multifuncional", "Impresora láser con scanner y copiadora", 10, 299.99),
        ("Escritorio Ajustable", "Escritorio con altura ajustable eléctrico", 8, 449.99),
        ("Silla Ergonómica", "Silla de oficina con soporte lumbar", 12, 199.99),
        ("Disco Duro Externo 1TB", "Disco duro portátil USB 3.0", 25, 69.99),
        ("Webcam HD", "Cámara web 1080p con micrófono integrado", 18, 59.99),
        ("Dock Station USB-C", "Hub multipuerto con HDMI y carga PD", 15, 89.99),
    ]

    products = []
    for name, description, quantity, price in products_data:
        product = Product(
            id=uuid.uuid4(),
            name=name,
            description=description,
            quantity=quantity,
            price=price,
            created_by=admin_user.id
        )
        db.add(product)
        products.append(product)

    db.commit()
    db.refresh(products[0])  # Forzar que SQLAlchemy registre los IDs

    # Crear transacciones asegurando saldo positivo
    for product in products:
        total_in = 0
        total_out = 0
        for _ in range(5):
            quantity_change = random.randint(1, 5)  # Solo entradas
            transaction = Transaction(
                id=uuid.uuid4(),
                product_id=product.id,
                quantity_change=quantity_change,
                type="IN",
                created_by=admin_user.id
            )
            db.add(transaction)
            total_in += quantity_change

        for _ in range(3):  # Menos transacciones de salida
            max_out = min(random.randint(1, 3), total_in - total_out)
            if max_out <= 0:
                continue
            transaction = Transaction(
                id=uuid.uuid4(),
                product_id=product.id,
                quantity_change=-max_out,
                type="OUT",
                created_by=admin_user.id
            )
            db.add(transaction)
            total_out += max_out

    db.commit()

    # Actualizar cantidades de productos basado en las transacciones
    for product in products:
        total_change = db.query(Transaction).filter_by(product_id=product.id).with_entities(func.sum(Transaction.quantity_change)).scalar()
        product.quantity = total_change or product.quantity
    db.commit()

    print("Datos iniciales cargados exitosamente.")
