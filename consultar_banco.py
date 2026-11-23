"""Mostra no terminal tudo o que está salvo no banco de dados (habitos.db).

Como usar:  python consultar_banco.py
"""
import os
import sqlite3

ARQUIVO_BANCO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "habitos.db")


def mostrar_tabela(cursor, titulo, consulta):
    print(f"\n===== {titulo} =====")
    cursor.execute(consulta)
    linhas = cursor.fetchall()
    if len(linhas) == 0:
        print("(vazio)")
    for linha in linhas:
        print(linha)


def main():
    if not os.path.exists(ARQUIVO_BANCO):
        print("O banco ainda não existe. Abra o app primeiro com: python main.py")
        return

    conexao = sqlite3.connect(ARQUIVO_BANCO)
    cursor = conexao.cursor()
    mostrar_tabela(cursor, "USUARIO (id, nome, xp, nivel)",
                   "SELECT id, nome, xp, nivel FROM usuario")
    mostrar_tabela(cursor, "HABITO (id, nome, dificuldade, frequencia, ultima_conclusao)",
                   "SELECT id, nome, dificuldade, frequencia, ultima_conclusao FROM habito")
    mostrar_tabela(cursor, "HISTORICO (id, nome_habito, xp, data)",
                   "SELECT id, nome_habito, xp, data FROM historico")
    conexao.close()


if __name__ == "__main__":
    main()
