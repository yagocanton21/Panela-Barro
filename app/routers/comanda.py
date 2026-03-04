from fastapi import APIRouter, HTTPException
from app.models import comanda as comanda_model
from app.models import pedido as pedido_model

router = APIRouter()

@router.get("/listar")
def listar_comandas():
    return comanda_model.listar_todas_abertas()

@router.post("/abrir/{numero_cartao}")
def abrir_comanda(numero_cartao: int):
    # Usa o model para verificar se já existe
    if comanda_model.buscar_aberta_por_cartao(numero_cartao):
        raise HTTPException(status_code=400, detail="Este cartão já está em uso!")

    try:
        comanda_model.abrir(numero_cartao)
        return {"mensagem": f"Comanda {numero_cartao} aberta"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/fechar/{numero_cartao}")
def fechar_comanda(numero_cartao: int):
    # 1. Busca o total acumulado usando o model de pedidos
    resultado = pedido_model.calcular_total_comanda(numero_cartao)
    
    if not resultado:
        raise HTTPException(status_code=404, detail="Comanda aberta não encontrada")

    total = resultado['total_consumo'] if resultado['total_consumo'] else 0.0

    # 2. Fecha a comanda usando o model de comandas
    try:
        comanda_model.fechar(resultado['id'], total)
        return {"mensagem": "Fechada com sucesso", "total": total}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
