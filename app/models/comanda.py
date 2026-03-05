from app.database import get_connection
import psycopg2.extras
from datetime import datetime

# Buscar comanda aberta
def buscar_aberta_por_comanda(numero_comanda):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT * FROM comandas WHERE numero_comanda = %s AND status = 'aberta'", (numero_comanda,))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    return resultado

# Abrir comanda
def abrir(numero_comanda):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO comandas (numero_comanda) VALUES (%s)", (numero_comanda,))
    conn.commit()
    cursor.close()
    conn.close()

# Fechar comanda
def fechar(id_comanda, total):
    conn = get_connection()
    cursor = conn.cursor()
    agora = datetime.now()
    cursor.execute(
        "UPDATE comandas SET status = 'fechada', fechada_em = %s, total = %s WHERE id = %s",
        (agora, total, id_comanda)
    )
    conn.commit()
    cursor.close()
    conn.close()

# Listar todas as comandas abertas
def listar_todas_abertas():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT * FROM comandas WHERE status = 'aberta' ORDER BY numero_comanda")
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultados
