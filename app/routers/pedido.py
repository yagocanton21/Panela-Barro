from fastapi import APIRouter, HTTPException
from app.models import pedido as pedido_model
from app.models import comanda as comanda_model
from app.models import produto as produto_model

router = APIRouter()

@router.post("/lancar")
def lancar_item(numero_comanda: int, produto_id: int, quantidade: float):
    # Buscar a comanda aberta
    comanda = comanda_model.buscar_aberta_por_comanda(numero_comanda)
    if not comanda:
        raise HTTPException(status_code=404, detail="Não existe comanda aberta para este cartão")

    # Buscar o preço do produto
    produto = produto_model.buscar_por_id(produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    # Calcular e inserir
    try:
        valor_pago = float(produto['preco_base']) * quantidade
        pedido_model.inserir(comanda['id'], produto_id, quantidade, valor_pago)
        return {
            "mensagem": "Lançamento realizado com sucesso",
            "valor_item": valor_pago
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Buscar extrato por cartão
@router.get("/extrato/{numero_comanda}")
def ver_extrato(numero_comanda: int):
    return pedido_model.buscar_extrato_por_comanda(numero_comanda)
