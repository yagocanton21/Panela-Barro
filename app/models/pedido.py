from app.database import get_connection
import psycopg2.extras

# Inserir pedido
def inserir(comanda_id, produto_id, quantidade, valor_pago):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = "INSERT INTO pedidos (comanda_id, produto_id, quantidade, valor_pago) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (comanda_id, produto_id, quantidade, valor_pago))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

# Buscar extrato por cartão
def buscar_extrato_por_comanda(numero_comanda):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    query = """
        SELECT p.nome, ped.quantidade, ped.valor_pago, ped.momento
        FROM pedidos ped
        JOIN produtos p ON ped.produto_id = p.id
        JOIN comandas c ON ped.comanda_id = c.id
        WHERE c.numero_comanda = %s AND c.status = 'aberta'
    """
    cursor.execute(query, (numero_comanda,))
    itens = cursor.fetchall()
    cursor.close()
    conn.close()
    return itens

# Calcular total da comanda
def calcular_total_comanda(numero_comanda):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    query = """
        SELECT c.id, SUM(p.valor_pago) as total_consumo
        FROM comandas c
        LEFT JOIN pedidos p ON c.id = p.comanda_id
        WHERE c.numero_comanda = %s AND c.status = 'aberta'
        GROUP BY c.id
    """
    cursor.execute(query, (numero_comanda,))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    return resultado
