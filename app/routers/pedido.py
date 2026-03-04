from fastapi import APIRouter, HTTPException
from app.models import pedido as pedido_model
from app.models import comanda as comanda_model
from app.models import produto as produto_model

router = APIRouter()

@router.post("/lancar")
def lancar_item(numero_cartao: int, produto_id: int, quantidade: float):
    # 1. Buscar a comanda aberta
    comanda = comanda_model.buscar_aberta_por_cartao(numero_cartao)
    if not comanda:
        raise HTTPException(status_code=404, detail="Não existe comanda aberta para este cartão")

    # 2. Buscar o preço do produto
    produto = produto_model.buscar_por_id(produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    # 3. Calcular e inserir
    try:
        valor_pago = float(produto['preco_base']) * quantidade
        pedido_model.inserir(comanda['id'], produto_id, quantidade, valor_pago)
        return {
            "mensagem": "Lançamento realizado com sucesso",
            "valor_item": valor_pago
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/extrato/{numero_cartao}")
def ver_extrato(numero_cartao: int):
    return pedido_model.buscar_extrato_por_cartao(numero_cartao)
