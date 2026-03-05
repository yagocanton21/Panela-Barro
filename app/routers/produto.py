from fastapi import APIRouter, HTTPException
from app.models import produto as produto_model # Importa as funções do banco

router = APIRouter()

# Listar produtos
@router.get("/listar")
def listar_produtos():
    return produto_model.listar_todos()

# Adicionar produto 
@router.post("/adicionar")
def adicionar_produto(nome: str, preco_base: float, categoria: str, unidade_medida: str = "kg"):
    try:
        produto_model.inserir(nome, preco_base, categoria, unidade_medida)
        return {"mensagem": "Produto adicionado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Buscar produto específico
@router.get("/buscar/{id}")
def buscar_produto(id: int):
    resultado = produto_model.buscar_por_id(id)
    if not resultado:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return resultado

# Deletar produto
@router.delete("/deletar/{id}")
def deletar_produto(id: int):
    try:
        linhas = produto_model.deletar(id)
        if linhas == 0:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        return {"mensagem": "Produto deletado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
