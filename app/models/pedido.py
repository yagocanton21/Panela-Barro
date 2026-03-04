from app.database import get_connection
import psycopg2.extras

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

def buscar_extrato_por_cartao(numero_cartao):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    query = """
        SELECT p.nome, ped.quantidade, ped.valor_pago, ped.momento
        FROM pedidos ped
        JOIN produtos p ON ped.produto_id = p.id
        JOIN comandas c ON ped.comanda_id = c.id
        WHERE c.numero_cartao = %s AND c.status = 'aberta'
    """
    cursor.execute(query, (numero_cartao,))
    itens = cursor.fetchall()
    cursor.close()
    conn.close()
    return itens

def calcular_total_comanda(numero_cartao):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    query = """
        SELECT c.id, SUM(p.valor_pago) as total_consumo
        FROM comandas c
        LEFT JOIN pedidos p ON c.id = p.comanda_id
        WHERE c.numero_cartao = %s AND c.status = 'aberta'
        GROUP BY c.id
    """
    cursor.execute(query, (numero_cartao,))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    return resultado
