from fastapi import FastAPI
from app.routers import products, transactions, users, auth, dashboard

from app.core.database import create_tables, init_db
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes
    allow_credentials=True,  # Permitir cookies/autenticación
    allow_methods=["*"],  # Permitir todos los métodos HTTP (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(transactions.router)
app.include_router(products.router)
app.include_router(dashboard.router)


# 🚀 Crear las tablas al iniciar el backend
@app.on_event("startup")
async def on_startup():
    create_tables()
    init_db()

@app.get("/")
def root():
    return {"message": "Welcome to the API"}