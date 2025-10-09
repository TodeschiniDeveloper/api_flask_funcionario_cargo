import bcrypt
from api.model.funcionario import Funcionario
from api.model.cargo import Cargo

"""
Classe responsável por gerenciar operações CRUD e autenticação
para a entidade Funcionario no banco de dados.

Esta classe utiliza injeção de dependência para receber a instância
de MysqlDatabase, que fornece conexões do pool.
"""

class FuncionarioDAO:
    def __init__(self, database_dependency):
        print("⬆️  FuncionarioDAO.__init__()")
        self.__database = database_dependency

    def create(self, objFuncionario: Funcionario) -> int:
        print("🟢 FuncionarioDAO.create()")
        hashed = bcrypt.hashpw(objFuncionario.senha.encode("utf-8"), bcrypt.gensalt())
        objFuncionario.senha = hashed.decode("utf-8")

        SQL = """
            INSERT INTO funcionario 
            (nomeFuncionario, email, senha, recebeValeTransporte, Cargo_idCargo) 
            VALUES (%s, %s, %s, %s, %s);
        """
        params = (
            objFuncionario.nomeFuncionario,
            objFuncionario.email,
            objFuncionario.senha,
            objFuncionario.recebeValeTransporte,
            objFuncionario.cargo.idCargo,
        )

        with self.__database.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(SQL, params)
                conn.commit()
                insert_id = cursor.lastrowid

        if not insert_id:
            raise Exception("Falha ao inserir funcionário")
        return insert_id

    def delete(self, idFuncionario: int) -> bool:
        print("🟢 FuncionarioDAO.delete()")
        SQL = "DELETE FROM funcionario WHERE idFuncionario = %s;"

        with self.__database.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(SQL, (idFuncionario,))
                conn.commit()
                affected = cursor.rowcount

        return affected > 0

    def update(self, objFuncionario: Funcionario) -> bool:
        print("🟢 FuncionarioDAO.update()")
        if objFuncionario.senha:
            senhaHash = bcrypt.hashpw(objFuncionario.senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            SQL = """
                UPDATE funcionario 
                SET nomeFuncionario=%s, email=%s, senha=%s, recebeValeTransporte=%s, Cargo_idCargo=%s 
                WHERE idFuncionario=%s;
            """
            params = (
                objFuncionario.nomeFuncionario,
                objFuncionario.email,
                senhaHash,
                objFuncionario.recebeValeTransporte,
                objFuncionario.cargo.idCargo,
                objFuncionario.idFuncionario,
            )
        else:
            SQL = """
                UPDATE funcionario 
                SET nomeFuncionario=%s, email=%s, recebeValeTransporte=%s, Cargo_idCargo=%s 
                WHERE idFuncionario=%s;
            """
            params = (
                objFuncionario.nomeFuncionario,
                objFuncionario.email,
                objFuncionario.recebeValeTransporte,
                objFuncionario.cargo.idCargo,
                objFuncionario.idFuncionario,
            )

        with self.__database.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(SQL, params)
                conn.commit()
                affected = cursor.rowcount

        return affected > 0

    def findAll(self) -> list[dict]:
        print("🟢 FuncionarioDAO.findAll()")
        SQL = """
            SELECT idFuncionario,nomeFuncionario,email,recebeValeTransporte,idCargo,nomeCargo 
            FROM funcionario
            JOIN cargo on funcionario.Cargo_idCargo = idCargo;
        """

        with self.__database.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(SQL)
                rows = cursor.fetchall()

        funcionarios = [
            {
                "idFuncionario": row["idFuncionario"],
                "nomeFuncionario": row["nomeFuncionario"],
                "email": row["email"],
                "recebeValeTransporte": row["recebeValeTransporte"],
                "cargo": {
                    "idCargo": row["idCargo"],
                    "nomeCargo": row["nomeCargo"]
                }
            }
            for row in rows
        ]
        return funcionarios

    def findById(self, idFuncionario: int) -> dict | None:
        funcionariosRaw = self.findByField("idFuncionario", idFuncionario)
        print("✅ FuncionarioDAO.findById()")
        return funcionariosRaw[0] if funcionariosRaw else None

    def findByField(self, campo: str, valor) -> list[dict]:
        print(f"🟢 FuncionarioDAO.findByField() - Campo: {campo}, Valor: {valor}")
        allowedFields = ["idFuncionario", "nomeFuncionario", "email", "senha", "recebeValeTransporte", "Cargo_idCargo"]
        if campo not in allowedFields:
            raise ValueError("Campo inválido para busca")

        SQL = f"SELECT * FROM funcionario WHERE {campo} = %s;"
        with self.__database.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(SQL, (valor,))
                resultados = cursor.fetchall()

        return resultados

    def login(self, objFuncionario: Funcionario) -> Funcionario | None:
        print("🟢 FuncionarioDAO.login()")
        SQL = """
            SELECT 
                idFuncionario, 
                nomeFuncionario,
                email, 
                senha, 
                recebeValeTransporte, 
                idCargo, 
                nomeCargo
            FROM funcionario
            JOIN cargo ON cargo.idCargo = funcionario.Cargo_idCargo
            WHERE email=%s;
        """

        with self.__database.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(SQL, (objFuncionario.email,))
                rows = cursor.fetchall()

        if len(rows) != 1:
            print("Funcionário não encontrado")
            return None

        funcionarioDB = rows[0]

        if not bcrypt.checkpw(
            objFuncionario.senha.encode("utf-8"),
            funcionarioDB["senha"].encode("utf-8")
        ):
            print("Senha inválida")
            return None

        objCargo = Cargo()
        objCargo.idCargo = int(funcionarioDB["idCargo"])
        objCargo.nomeCargo = funcionarioDB["nomeCargo"]

        funcionario = Funcionario()
        funcionario.idFuncionario = funcionarioDB["idFuncionario"]
        funcionario.cargo = objCargo
        funcionario.nomeFuncionario = funcionarioDB["nomeFuncionario"]
        funcionario.email = funcionarioDB["email"]
        funcionario.recebeValeTransporte = funcionarioDB["recebeValeTransporte"]

        print("✅ FuncionarioDAO.login() -> sucesso")
        return funcionario
