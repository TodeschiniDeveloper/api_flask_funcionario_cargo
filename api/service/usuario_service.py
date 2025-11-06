# -*- coding: utf-8 -*-
from api.dao.usuario_dao import UsuarioDAO
from api.model.usuario import Usuario
from api.utils.error_response import ErrorResponse
from api.http.meu_token_jwt import MeuTokenJWT


"""
Classe responsável pela camada de serviço para a entidade Usuario.

Observações sobre injeção de dependência:
- O UsuarioService recebe instâncias de UsuarioDAO via construtor.
- Isso desacopla o serviço das implementações concretas dos DAOs.
- Facilita testes unitários e uso de mocks.
"""
class UsuarioService:
    def __init__(self, usuario_dao_dependency: UsuarioDAO):
        """
        Construtor da classe UsuarioService

        :param usuario_dao_dependency: UsuarioDAO
        """
        print("⬆️  UsuarioService.__init__()")
        self.__usuarioDAO = usuario_dao_dependency

    def createUsuario(self, jsonUsuario: dict) -> int:
        """
        Cria um novo usuário.

        :param jsonUsuario: dict contendo dados do usuário
        :return: int ID do usuário criado
        :raises ErrorResponse: se email já existir
        """
        print("🟣 UsuarioService.createUsuario()")

        # ✅ CORREÇÃO: Extrai do objeto "usuario" se existir
        usuario_data = jsonUsuario.get("usuario", jsonUsuario)
        
        objUsuario = Usuario()
        objUsuario.nome = usuario_data["nome"]
        objUsuario.email = usuario_data["email"]
        objUsuario.senha_hash = usuario_data["senha_hash"]

        # regra de negócio: validar email duplicado
        emailExiste = self.__usuarioDAO.findByField("email", objUsuario.email)
        if emailExiste and len(emailExiste) > 0:
            raise ErrorResponse(
                400,
                "Usuário já existe",
                {"message": f"O email {objUsuario.email} já está cadastrado"}
            )

        user_id = self.__usuarioDAO.create(objUsuario)
        print(f"✅ Usuário criado com ID: {user_id}")
        return user_id

    def loginUsuario(self, jsonUsuario: dict) -> dict:
        """
        Realiza login de um usuário e retorna token JWT.

        :param jsonUsuario: dict {"email", "senha_hash"} dentro de "usuario"
        :return: dict {user, token}
        :raises ErrorResponse: se login falhar
        """
        print("🟣 UsuarioService.loginUsuario()")
        print(f"📨 Dados recebidos para login: {jsonUsuario}")

        # ✅ CORREÇÃO: Extrai do objeto "usuario" com fallback
        usuario_data = jsonUsuario.get("usuario", jsonUsuario)
        
        objUsuario = Usuario()
        objUsuario.email = usuario_data["email"]
        objUsuario.senha_hash = usuario_data["senha_hash"]
        
        print(f"🔐 Tentando login para: {objUsuario.email}")
      
        encontrado = self.__usuarioDAO.login(objUsuario)

        if not encontrado:
            print("❌ Login falhou - usuário não encontrado ou senha incorreta")
            raise ErrorResponse(
                401,
                "Usuário ou senha inválidos",
                {"message": "Não foi possível realizar autenticação"}
            )

        jwt = MeuTokenJWT()
        user = {
            "usuario": {
                "email": encontrado.email,
                "nome": encontrado.nome,  # ✅ CORREÇÃO: era "name", mudado para "nome"
                "id": encontrado.id
            }
        }
        token = jwt.gerarToken(user["usuario"])
        
        print(f"✅ Login bem-sucedido para: {encontrado.email}")
        print(f"🔑 Token gerado: {token[:50]}...")
        
        return {
            "user": user, 
            "token": token
        }

    def findAll(self) -> list[dict]:
        """
        Retorna todos os usuários.
        """
        print("🟣 UsuarioService.findAll()")
        return self.__usuarioDAO.findAll()

    def findById(self, id: int) -> dict:
        """
        Busca usuário por ID.

        :param id: int
        :return: dict
        :raises ErrorResponse: se usuário não for encontrado
        """
        usuario = self.__usuarioDAO.findById(id)
        if not usuario:
            raise ErrorResponse(
                404,
                "Usuário não encontrado",
                {"message": f"Não existe usuário com id {id}"}
            )
        return usuario

    def updateUsuario(self, id: int, requestBody: dict) -> bool:
        """
        Atualiza dados de um usuário.

        :param id: int
        :param requestBody: dict {"usuario": {...}}
        :return: bool
        """
        print("🟣 UsuarioService.updateUsuario()")

        jsonUsuario = requestBody["usuario"]

        objUsuario = Usuario()
        objUsuario.id = id
        objUsuario.nome = jsonUsuario["nome"]
        objUsuario.email = jsonUsuario["email"]
        
        # A senha é opcional na atualização
        if "senha_hash" in jsonUsuario and jsonUsuario["senha_hash"]:
            objUsuario.senha_hash = jsonUsuario["senha_hash"]

        return self.__usuarioDAO.update(objUsuario)

    def deleteUsuario(self, id: int) -> bool:
        """
        Remove usuário por ID.

        :param id: int
        :return: bool
        """
        print("🟣 UsuarioService.deleteUsuario()")
        return self.__usuarioDAO.delete(id)