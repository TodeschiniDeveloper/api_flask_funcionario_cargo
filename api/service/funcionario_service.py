# -*- coding: utf-8 -*-
from api.dao.funcionario_dao import FuncionarioDAO
from api.dao.cargo_dao import CargoDAO
from api.model.funcionario import Funcionario
from api.model.cargo import Cargo
from api.utils.error_response import ErrorResponse
from api.http.meu_token_jwt import MeuTokenJWT


"""
Classe responsável pela camada de serviço para a entidade Funcionario.

Observações sobre injeção de dependência:
- O FuncionarioService recebe instâncias de FuncionarioDAO e CargoDAO via construtor.
- Isso desacopla o serviço das implementações concretas dos DAOs.
- Facilita testes unitários e uso de mocks.
"""
class FuncionarioService:
    def __init__(self, funcionario_dao_dependency: FuncionarioDAO, cargo_dao_dependency: CargoDAO):
        """
        Construtor da classe FuncionarioService

        :param funcionario_dao_dependency: FuncionarioDAO
        :param cargo_dao_dependency: CargoDAO
        """
        print("⬆️  FuncionarioService.__init__()")
        self.__funcionarioDAO = funcionario_dao_dependency
        self.__cargoDAO = cargo_dao_dependency

    def createFuncionario(self, jsonFuncionario: dict) -> Funcionario:
        """
        Cria um novo funcionário.

        :param jsonFuncionario: dict contendo dados do funcionário
        :return: Funcionario com ID atribuído
        :raises ErrorResponse: se email já existir ou cargo for inválido
        """
        print("🟣 FuncionarioService.createFuncionario()")

        objCargo = Cargo()
        objCargo.idCargo = jsonFuncionario["cargo"]["idCargo"]

        objFuncionario = Funcionario()
        objFuncionario.nomeFuncionario = jsonFuncionario["nomeFuncionario"]
        objFuncionario.email = jsonFuncionario["email"]
        objFuncionario.senha = jsonFuncionario["senha"]
        objFuncionario.recebeValeTransporte = jsonFuncionario["recebeValeTransporte"]
        objFuncionario.cargo = objCargo

        # regra de negócio: validar cargo
        cargoExiste =  self.__cargoDAO.findByField("idCargo", objFuncionario.cargo.idCargo)
        if not cargoExiste:
            raise ErrorResponse(
                400,
                "O cargo informado não existe",
                {"message": f"O cargo {objFuncionario.cargo.idCargo} não foi encontrado"}
            )

        # regra de negócio: validar email duplicado
        emailExiste =  self.__funcionarioDAO.findByField("email", objFuncionario.email)
        if emailExiste and len(emailExiste) > 0:
            raise ErrorResponse(
                400,
                "Funcionário já existe",
                {"message": f"O email {objFuncionario.email} já está cadastrado"}
            )

        
        return self.__funcionarioDAO.create(objFuncionario)
   

    def loginFuncionario(self, jsonFuncionario: dict) -> dict:
        """
        Realiza login de um funcionário e retorna token JWT.

        :param jsonFuncionario: dict {"email", "senha"}
        :return: dict {user, token}
        :raises ErrorResponse: se login falhar
        """
        # Print do JSON recebido, antes de qualquer lógica
        print("🟣 FuncionarioService.loginFuncionario()")
        print(jsonFuncionario)

        objFuncionario = Funcionario()
        objFuncionario.email = jsonFuncionario["email"]
        objFuncionario.senha = jsonFuncionario["senha"]
      
        encontrado = self.__funcionarioDAO.login(objFuncionario)

        if not encontrado:
            raise ErrorResponse(
                401,
                "Usuário ou senha inválidos",
                {"message": "Não foi possível realizar autenticação"}
            )

        jwt = MeuTokenJWT()
        user = {
            "funcionario": {
                "email": encontrado.email,
                "role": getattr(encontrado.cargo, "nomeCargo", None),
                "name": encontrado.nomeFuncionario,
                "idFuncionario": encontrado.idFuncionario
            }
        }
        return {"user": user, "token": jwt.gerarToken(user["funcionario"])}
    

    def findAll(self) -> list[dict]:
        """
        Retorna todos os funcionários.
        """
        print("🟣 FuncionarioService.findAll()")
        return  self.__funcionarioDAO.findAll()

    def findById(self, idFuncionario: int) -> dict:
        """
        Busca funcionário por ID.

        :param idFuncionario: int
        :return: dict
        :raises ErrorResponse: se funcionário não for encontrado
        """
        objFuncionario = Funcionario()
        objFuncionario.idFuncionario = idFuncionario

        funcionario =  self.__funcionarioDAO.findById(objFuncionario.idFuncionario)
        if not funcionario:
            raise ErrorResponse(
                404,
                "Funcionário não encontrado",
                {"message": f"Não existe funcionário com id {idFuncionario}"}
            )
        return funcionario

    def updateFuncionario(self, idFuncionario: int, requestBody: dict) -> bool:
        """
        Atualiza dados de um funcionário.

        :param idFuncionario: int
        :param requestBody: dict {"funcionario": {...}}
        :return: bool
        """
        print("🟣 FuncionarioService.updateFuncionario()")

        jsonFuncionario = requestBody["funcionario"]

        objCargo = Cargo()
        objCargo.idCargo = jsonFuncionario["cargo"]["idCargo"]

        objFuncionario = Funcionario()
        objFuncionario.idFuncionario = idFuncionario
        objFuncionario.nomeFuncionario = jsonFuncionario["nomeFuncionario"]
        objFuncionario.email = jsonFuncionario["email"]
        objFuncionario.senha = jsonFuncionario["senha"]
        objFuncionario.recebeValeTransporte = jsonFuncionario["recebeValeTransporte"]
        objFuncionario.cargo = objCargo

        return  self.__funcionarioDAO.update(objFuncionario)

    def deleteFuncionario(self, idFuncionario: int) -> bool:
        """
        Remove funcionário por ID.

        :param idFuncionario: int
        :return: bool
        """
        print("🟣 FuncionarioService.deleteFuncionario()")
        return  self.__funcionarioDAO.delete(idFuncionario)
