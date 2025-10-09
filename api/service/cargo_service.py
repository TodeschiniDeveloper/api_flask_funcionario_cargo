# -*- coding: utf-8 -*-
from api.dao.cargo_dao import CargoDAO
from api.model.cargo import Cargo
from api.utils.error_response import ErrorResponse

"""
Classe responsável pela camada de serviço para a entidade Cargo.

Observações sobre injeção de dependência:
- O CargoService recebe uma instância de CargoDAO via construtor.
- Isso segue o padrão de injeção de dependência, tornando o serviço desacoplado
  do DAO concreto, facilitando testes unitários e substituição por mocks.
"""
class CargoService:
    def __init__(self, cargo_dao_dependency: CargoDAO):
        """
        Construtor da classe CargoService

        :param cargo_dao_dependency: CargoDAO - Instância de CargoDAO
        """
        print("⬆️  CargoService.__init__()")
        self.__cargoDAO = cargo_dao_dependency  # injeção de dependência

    def createCargo(self, cargoBodyRequest: dict) -> int:
        """
        Cria um novo cargo.

        :param cargoBodyRequest: dict - Dados do cargo {"nomeCargo"}
        :return: int - ID do novo cargo criado

        🔹 Validações:
        - nomeCargo não pode estar vazio
        - Não pode existir outro cargo com mesmo nome
        """
        print("🟣 CargoService.createCargo()")

        cargo = Cargo()
        cargo.nomeCargo = cargoBodyRequest.get("nomeCargo")

        # valida regra de negócio: cargo duplicado
        resultado = self.__cargoDAO.findByField("nomeCargo", cargo.nomeCargo)
        if resultado and len(resultado) > 0:
            raise ErrorResponse(
                400,
                "Cargo já existe",
                {"message": f"O cargo {cargo.nomeCargo} já existe"}
            )

        return  self.__cargoDAO.create(cargo)

    def findAll(self) -> list[dict]:
        """
        Retorna todos os cargos
        :return: list[dict]
        """
        print("🟣 CargoService.findAll()")
        return self.__cargoDAO.findAll()

    def findById(self, idCargo: int) -> dict | None:
        """
        Retorna um cargo por ID.

        :param idCargo: int
        :return: dict | None
        """
        print("🟣 CargoService.findById()")

        cargo = Cargo()
        cargo.idCargo = idCargo  # passa pela validação de domínio

        return self.__cargoDAO.findById(cargo.idCargo)

    def updateCargo(self, idCargo: int, jsonCargo: dict) -> bool:
        print (jsonCargo)
        """
        Atualiza um cargo existente.

        🔹 Regra de domínio: o idCargo deve ser um número inteiro positivo.

        :param idCargo: int - Identificador do cargo a ser atualizado
        :param jsonCargo: dict - Dados do cargo {"nomeCargo"}
        :return: bool - True se atualizado com sucesso
        :raises ValueError: se idCargo ou nomeCargo não atenderem às regras de domínio
        """
        print("🟣 CargoService.updateCargo()")

        cargo = Cargo()
        cargo.idCargo = idCargo
        cargo.nomeCargo = jsonCargo.get("nomeCargo")

        return self.__cargoDAO.update(cargo)

    def deleteCargo(self, idCargo: int) -> bool:
        """
        Deleta um cargo por ID.

        :param idCargo: int
        :return: bool
        """
        print("🟣 CargoService.deleteCargo()")

        cargo = Cargo()
        cargo.idCargo = idCargo  # validação de regra de domínio

        return self.__cargoDAO.delete(cargo)
