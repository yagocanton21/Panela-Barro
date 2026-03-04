from app.database import get_connection
import psycopg2.extras

# 1. Função para buscar todos os produtos
def listar_todos():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT * FROM produtos ORDER BY nome")
    produtos = cursor.fetchall()
    cursor.close()
    conn.close()
    return produtos

# 2. Função para buscar apenas um produto por ID
def buscar_por_id(id):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT * FROM produtos WHERE id = %s", (id,))
    produto = cursor.fetchone()
    cursor.close()
    conn.close()
    return produto

# 3. Função para inserir um novo produto
def inserir(nome, preco_base, categoria, unidade_medida):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO produtos (nome, preco_base, categoria, unidade_medida) VALUES (%s, %s, %s, %s)",
            (nome, preco_base, categoria, unidade_medida)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

# 4. Função para deletar um produto
def deletar(id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM produtos WHERE id = %s", (id,))
        linhas_afetadas = cursor.rowcount
        conn.commit()
        return linhas_afetadas
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()
