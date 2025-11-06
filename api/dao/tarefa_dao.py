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

        with self.__database.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(SQL, params)
                conn.commit()
                insert_id = cursor.lastrowid

        if not insert_id:
            raise Exception("Falha ao inserir tarefa")
        return insert_id

    def delete(self, id: int) -> bool:
        print("🟢 TarefaDAO.delete()")
        SQL = "DELETE FROM tarefas WHERE id = %s;"

        with self.__database.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(SQL, (id,))
                conn.commit()
                affected = cursor.rowcount

        return affected > 0

    def update(self, objTarefa: Tarefa) -> bool:
        print("🟢 TarefaDAO.update()")
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

        with self.__database.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(SQL, params)
                conn.commit()
                affected = cursor.rowcount

        return affected > 0

    def findAll(self) -> list[dict]:
        print("🟢 TarefaDAO.findAll()")
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

        with self.__database.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(SQL)
                rows = cursor.fetchall()

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

    def findById(self, id: int) -> dict | None:
        tarefasRaw = self.findByField("id", id)
        print("✅ TarefaDAO.findById()")
        return tarefasRaw[0] if tarefasRaw else None

    def findByField(self, campo: str, valor) -> list[dict]:
        print(f"🟢 TarefaDAO.findByField() - Campo: {campo}, Valor: {valor}")
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
        with self.__database.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(SQL, (valor,))
                resultados = cursor.fetchall()

        return resultados

    def findByProjetoId(self, projeto_id: int) -> list[dict]:
        print("🟢 TarefaDAO.findByProjetoId()")
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

        with self.__database.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(SQL, (projeto_id,))
                rows = cursor.fetchall()

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

    def marcarComoConcluida(self, id: int) -> bool:
        print("🟢 TarefaDAO.marcarComoConcluida()")
        SQL = "UPDATE tarefas SET concluida = TRUE WHERE id = %s;"

        with self.__database.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(SQL, (id,))
                conn.commit()
                affected = cursor.rowcount

        return affected > 0