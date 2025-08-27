from dataclasses import dataclass

@dataclass
class Actor:
    id: int
    first_name: str
    last_name: str

import sqlite3
from typing import List
from models import Actor

class ActorManager:
    """
    Uma classe gerenciadora para lidar com operações CRUD para instâncias de Actor em um banco de dados SQLite.
    """

    def __init__(self, db_name: str, table_name: str):
        """
        Inicializa o gerenciador, cria uma conexão com o banco de dados e garante que a tabela exista.
        :param db_name: Nome do arquivo do banco SQLite.
        :param table_name: Nome da tabela para armazenar os atores.
        """
        self.db_name = db_name
        self.table_name = table_name
        self.conn = sqlite3.connect(self.db_name)
        self._create_table()

    def _create_table(self):
        """Cria a tabela de atores se ela não existir."""
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def create(self, first_name: str, last_name: str) -> None:
        """
        Insere um novo ator no banco de dados.
        :param first_name: Primeiro nome do ator.
        :param last_name: Sobrenome do ator.
        """
        query = f"INSERT INTO {self.table_name} (first_name, last_name) VALUES (?, ?)"
        try:
            self.conn.execute(query, (first_name, last_name))
            self.conn.commit()
        except sqlite3.DatabaseError as e:
            print(f"Erro ao criar ator: {e}")

    def all(self) -> List[Actor]:
        """
        Recupera todos os atores do banco de dados.
        :return: Lista de instâncias da classe Actor.
        """
        query = f"SELECT id, first_name, last_name FROM {self.table_name}"
        cursor = self.conn.execute(query)
        rows = cursor.fetchall()
        return [Actor(id=row[0], first_name=row[1], last_name=row[2]) for row in rows]

    def update(self, pk: int, new_first_name: str, new_last_name: str) -> None:
        """
        Atualiza o nome de um ator existente.
        :param pk: ID do ator.
        :param new_first_name: Novo primeiro nome.
        :param new_last_name: Novo sobrenome.
        """
        query = f"UPDATE {self.table_name} SET first_name = ?, last_name = ? WHERE id = ?"
        try:
            self.conn.execute(query, (new_first_name, new_last_name, pk))
            self.conn.commit()
        except sqlite3.DatabaseError as e:
            print(f"Erro ao atualizar ator: {e}")

    def delete(self, pk: int) -> None:
        """
        Remove um ator pelo ID.
        :param pk: ID do ator.
        """
        query = f"DELETE FROM {self.table_name} WHERE id = ?"
        try:
            self.conn.execute(query, (pk,))
            self.conn.commit()
        except sqlite3.DatabaseError as e:
            print(f"Erro ao deletar ator: {e}")

    def close(self):
        """Fecha a conexão com o banco de dados."""
        self.conn.close()

    def __enter__(self):
        """Permite uso com gerenciadores de contexto."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Garante que a conexão seja fechada ao sair do contexto."""
        self.close()
