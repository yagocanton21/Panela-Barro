from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import produto, comanda, pedido

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rota de produtos
app.include_router(produto.router, prefix="/produtos", tags=["Produtos"])

# Rota de comandas
app.include_router(comanda.router, prefix="/comandas", tags=["Comandas"])

# Rota de pedidos
app.include_router(pedido.router, prefix="/pedidos", tags=["Pedidos"])

@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao Sistema de Comandas - Panela de Barro!"}