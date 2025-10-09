# -*- coding: utf-8 -*-
from api.model.cargo import Cargo

"""
Representa o DAO (Data Access Object) de Cargo.

Objetivo:
- Encapsular operações de acesso a dados relacionadas à entidade Cargo.
- Permitir injeção de dependência do MysqlDatabase (que fornece conexões do pool).
"""
class CargoDAO:
    def __init__(self, database_dependency):
        """
        Construtor do DAO, recebe o Database (pool de conexões) por injeção de dependência.

        :param database_dependency: Instância de MysqlDatabase
        """
        print("⬆️  CargoDAO.__init__()")
        self.__database = database_dependency  

    def create(self, objCargo: Cargo) -> int:
        SQL = "INSERT INTO cargo (nomeCargo) VALUES (%s);"
        params = (objCargo.nomeCargo,)

        with self.__database.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(SQL, params)
                conn.commit()
                insert_id = cursor.lastrowid

        if not insert_id:
            raise Exception("Falha ao inserir cargo")
        print("✅ CargoDAO.create()")
        return insert_id

    def delete(self, cargo: Cargo) -> bool:
        SQL = "DELETE FROM cargo WHERE idCargo = %s;"
        params = (cargo.idCargo,)

        with self.__database.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(SQL, params)
                conn.commit()
                affected = cursor.rowcount

        print("✅ CargoDAO.delete()")
        return affected > 0

    def update(self, objCargo: Cargo) -> bool:
        SQL = "UPDATE cargo SET nomeCargo = %s WHERE idCargo = %s;"
        params = (objCargo.nomeCargo, objCargo.idCargo)

        with self.__database.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(SQL, params)
                conn.commit()
                affected = cursor.rowcount

        print("✅ CargoDAO.update()")
        return affected > 0

    def findAll(self) -> list[dict]:
        SQL = "SELECT * FROM cargo;"

        with self.__database.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(SQL)
                resultados = cursor.fetchall()

        print(f"✅ CargoDAO.findAll() -> {len(resultados)} registros encontrados")
        return resultados

    def findById(self, idCargo: int) -> dict | None:
        resultados = self.findByField("idCargo", idCargo)
        print("✅ CargoDAO.findById()")
        return resultados[0] if resultados else None

    def findByField(self, field: str, value) -> list[dict]:
        allowed_fields = ["idCargo", "nomeCargo"]
        if field not in allowed_fields:
            raise ValueError(f"Campo inválido para busca: {field}")

        SQL = f"SELECT * FROM cargo WHERE {field} = %s;"
        params = (value,)

        with self.__database.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(SQL, params)
                resultados = cursor.fetchall()

        print("✅ CargoDAO.findByField()")
        return resultados
