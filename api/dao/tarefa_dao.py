# -*- coding: utf-8 -*-
from api.model.tarefa import Tarefa

"""
Classe responsável por gerenciar operações CRUD
para a entidade Tarefa no banco de dados.
"""

class TarefaDAO:
    def __init__(self, database_dependency):
        print("⬆️  TarefaDAO.__init__()")
        self.__database = database_dependency

    def create(self, objTarefa: Tarefa) -> int:
        print("🟢 TarefaDAO.create()")
        try:
            SQL = """
                INSERT INTO tarefas 
                (titulo, concluida, data_limite, projeto_id) 
                VALUES (%s, %s, %s, %s);
            """
            params = (
                objTarefa.titulo,
                objTarefa.concluida,
                objTarefa.data_limite,
                objTarefa.projeto_id,
            )

            insert_id = self.__database.execute_query(SQL, params)
            
            if not insert_id:
                raise Exception("Falha ao inserir tarefa")
            return insert_id
            
        except Exception as e:
            print(f"❌ Erro em TarefaDAO.create(): {e}")
            raise

    def delete(self, id: int) -> bool:
        print("🟢 TarefaDAO.delete()")
        try:
            SQL = "DELETE FROM tarefas WHERE id = %s;"
            affected = self.__database.execute_query(SQL, (id,))
            return affected > 0
        except Exception as e:
            print(f"❌ Erro em TarefaDAO.delete(): {e}")
            raise

    def update(self, objTarefa: Tarefa) -> bool:
        print("🟢 TarefaDAO.update()")
        try:
            SQL = """
                UPDATE tarefas 
                SET titulo=%s, concluida=%s, data_limite=%s, projeto_id=%s 
                WHERE id=%s;
            """
            params = (
                objTarefa.titulo,
                objTarefa.concluida,
                objTarefa.data_limite,
                objTarefa.projeto_id,
                objTarefa.id,
            )

            affected = self.__database.execute_query(SQL, params)
            return affected > 0
            
        except Exception as e:
            print(f"❌ Erro em TarefaDAO.update(): {e}")
            raise

    def findAll(self) -> list[dict]:
        print("🟢 TarefaDAO.findAll()")
        try:
            SQL = """
                SELECT 
                    t.id, 
                    t.titulo, 
                    t.concluida, 
                    t.data_limite, 
                    t.projeto_id,
                    p.nome as projeto_nome,
                    p.usuario_id,
                    u.nome as usuario_nome
                FROM tarefas t
                JOIN projetos p ON t.projeto_id = p.id
                JOIN usuarios u ON p.usuario_id = u.id;
            """
            rows = self.__database.execute_query(SQL, fetch=True)

            tarefas = [
                {
                    "id": row["id"],
                    "titulo": row["titulo"],
                    "concluida": bool(row["concluida"]),
                    "data_limite": row["data_limite"].isoformat() if row["data_limite"] else None,
                    "projeto_id": row["projeto_id"],
                    "projeto_nome": row["projeto_nome"],
                    "usuario_id": row["usuario_id"],
                    "usuario_nome": row["usuario_nome"]
                }
                for row in rows
            ]
            return tarefas
        except Exception as e:
            print(f"❌ Erro em TarefaDAO.findAll(): {e}")
            raise

    def findById(self, id: int) -> dict | None:
        print("✅ TarefaDAO.findById()")
        try:
            tarefasRaw = self.findByField("id", id)
            return tarefasRaw[0] if tarefasRaw else None
        except Exception as e:
            print(f"❌ Erro em TarefaDAO.findById(): {e}")
            raise

    def findByField(self, campo: str, valor) -> list[dict]:
        print(f"🟢 TarefaDAO.findByField() - Campo: {campo}, Valor: {valor}")
        try:
            allowedFields = ["id", "titulo", "concluida", "projeto_id"]
            if campo not in allowedFields:
                raise ValueError("Campo inválido para busca")

            SQL = f"""
                SELECT 
                    t.*,
                    p.nome as projeto_nome,
                    u.nome as usuario_nome
                FROM tarefas t
                JOIN projetos p ON t.projeto_id = p.id
                JOIN usuarios u ON p.usuario_id = u.id
                WHERE t.{campo} = %s;
            """
            resultados = self.__database.execute_query(SQL, (valor,), fetch=True)
            return resultados
        except Exception as e:
            print(f"❌ Erro em TarefaDAO.findByField(): {e}")
            raise

    def findByProjetoId(self, projeto_id: int) -> list[dict]:
        print("🟢 TarefaDAO.findByProjetoId()")
        try:
            SQL = """
                SELECT 
                    t.id, 
                    t.titulo, 
                    t.concluida, 
                    t.data_limite, 
                    t.projeto_id,
                    p.nome as projeto_nome
                FROM tarefas t
                JOIN projetos p ON t.projeto_id = p.id
                WHERE t.projeto_id = %s;
            """
            rows = self.__database.execute_query(SQL, (projeto_id,), fetch=True)

            tarefas = [
                {
                    "id": row["id"],
                    "titulo": row["titulo"],
                    "concluida": bool(row["concluida"]),
                    "data_limite": row["data_limite"].isoformat() if row["data_limite"] else None,
                    "projeto_id": row["projeto_id"],
                    "projeto_nome": row["projeto_nome"]
                }
                for row in rows
            ]
            return tarefas
        except Exception as e:
            print(f"❌ Erro em TarefaDAO.findByProjetoId(): {e}")
            raise

    def marcarComoConcluida(self, id: int) -> bool:
        print("🟢 TarefaDAO.marcarComoConcluida()")
        try:
            SQL = "UPDATE tarefas SET concluida = TRUE WHERE id = %s;"
            affected = self.__database.execute_query(SQL, (id,))
            return affected > 0
        except Exception as e:
            print(f"❌ Erro em TarefaDAO.marcarComoConcluida(): {e}")
            raise