# -*- coding: utf-8 -*-
from api.model.projeto import Projeto

"""
Classe responsável por gerenciar operações CRUD
para a entidade Projeto no banco de dados.
"""

class ProjetoDAO:
    def __init__(self, database_dependency):
        print("⬆️  ProjetoDAO.__init__()")
        self.__database = database_dependency

    def create(self, objProjeto: Projeto) -> int:
        print("🟢 ProjetoDAO.create()")
        try:
            SQL = """
                INSERT INTO projetos 
                (nome, descricao, data_inicio, status, usuario_id) 
                VALUES (%s, %s, %s, %s, %s);
            """
            params = (
                objProjeto.nome,
                objProjeto.descricao,
                objProjeto.data_inicio,
                objProjeto.status,
                objProjeto.usuario_id,
            )

            insert_id = self.__database.execute_query(SQL, params)
            
            if not insert_id:
                raise Exception("Falha ao inserir projeto")
            return insert_id
            
        except Exception as e:
            print(f"❌ Erro em ProjetoDAO.create(): {e}")
            raise

    def delete(self, id: int) -> bool:
        print("🟢 ProjetoDAO.delete()")
        try:
            SQL = "DELETE FROM projetos WHERE id = %s;"
            affected = self.__database.execute_query(SQL, (id,))
            return affected > 0
        except Exception as e:
            print(f"❌ Erro em ProjetoDAO.delete(): {e}")
            raise

    def update(self, objProjeto: Projeto) -> bool:
        print("🟢 ProjetoDAO.update()")
        try:
            SQL = """
                UPDATE projetos 
                SET nome=%s, descricao=%s, data_inicio=%s, status=%s, usuario_id=%s 
                WHERE id=%s;
            """
            params = (
                objProjeto.nome,
                objProjeto.descricao,
                objProjeto.data_inicio,
                objProjeto.status,
                objProjeto.usuario_id,
                objProjeto.id,
            )

            affected = self.__database.execute_query(SQL, params)
            return affected > 0
            
        except Exception as e:
            print(f"❌ Erro em ProjetoDAO.update(): {e}")
            raise

    def findAll(self) -> list[dict]:
        print("🟢 ProjetoDAO.findAll()")
        try:
            SQL = """
                SELECT 
                    p.id, 
                    p.nome, 
                    p.descricao, 
                    p.data_inicio, 
                    p.status, 
                    p.usuario_id,
                    u.nome as usuario_nome
                FROM projetos p
                JOIN usuarios u ON p.usuario_id = u.id;
            """
            rows = self.__database.execute_query(SQL, fetch=True)

            projetos = [
                {
                    "id": row["id"],
                    "nome": row["nome"],
                    "descricao": row["descricao"],
                    "data_inicio": row["data_inicio"].isoformat() if row["data_inicio"] else None,
                    "status": row["status"],
                    "usuario_id": row["usuario_id"],
                    "usuario_nome": row["usuario_nome"]
                }
                for row in rows
            ]
            return projetos
        except Exception as e:
            print(f"❌ Erro em ProjetoDAO.findAll(): {e}")
            raise

    def findById(self, id: int) -> dict | None:
        print("✅ ProjetoDAO.findById()")
        try:
            projetosRaw = self.findByField("id", id)
            return projetosRaw[0] if projetosRaw else None
        except Exception as e:
            print(f"❌ Erro em ProjetoDAO.findById(): {e}")
            raise

    def findByField(self, campo: str, valor) -> list[dict]:
        print(f"🟢 ProjetoDAO.findByField() - Campo: {campo}, Valor: {valor}")
        try:
            allowedFields = ["id", "nome", "status", "usuario_id"]
            if campo not in allowedFields:
                raise ValueError("Campo inválido para busca")

            SQL = f"""
                SELECT 
                    p.*,
                    u.nome as usuario_nome
                FROM projetos p
                JOIN usuarios u ON p.usuario_id = u.id
                WHERE p.{campo} = %s;
            """
            resultados = self.__database.execute_query(SQL, (valor,), fetch=True)
            return resultados
        except Exception as e:
            print(f"❌ Erro em ProjetoDAO.findByField(): {e}")
            raise

    def findByUsuarioId(self, usuario_id: int) -> list[dict]:
        print("🟢 ProjetoDAO.findByUsuarioId()")
        try:
            SQL = """
                SELECT 
                    p.id, 
                    p.nome, 
                    p.descricao, 
                    p.data_inicio, 
                    p.status, 
                    p.usuario_id,
                    u.nome as usuario_nome
                FROM projetos p
                JOIN usuarios u ON p.usuario_id = u.id
                WHERE p.usuario_id = %s;
            """
            rows = self.__database.execute_query(SQL, (usuario_id,), fetch=True)

            projetos = [
                {
                    "id": row["id"],
                    "nome": row["nome"],
                    "descricao": row["descricao"],
                    "data_inicio": row["data_inicio"].isoformat() if row["data_inicio"] else None,
                    "status": row["status"],
                    "usuario_id": row["usuario_id"],
                    "usuario_nome": row["usuario_nome"]
                }
                for row in rows
            ]
            return projetos
        except Exception as e:
            print(f"❌ Erro em ProjetoDAO.findByUsuarioId(): {e}")
            raise