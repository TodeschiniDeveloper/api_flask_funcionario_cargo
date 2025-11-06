# -*- coding: utf-8 -*-
from flask import Blueprint, request
from api.middleware.jwt_middleware import JwtMiddleware
from api.middleware.projeto_middleware import ProjetoMiddleware
from api.control.projeto_control import ProjetoControl

class ProjetoRoteador:
    """
    Classe responsável por configurar todas as rotas da entidade Projeto no Flask.

    Objetivos:
    - Criar um Blueprint isolado para as rotas de Projeto.
    - Receber middlewares e controlador via injeção de dependência.
    - Aplicar autenticação JWT e validações antes de chamar o controlador.
    """

    def __init__(self, jwt_middleware: JwtMiddleware, projeto_middleware: ProjetoMiddleware, projeto_control: ProjetoControl):
        """
        Construtor do roteador.

        :param jwt_middleware: Middleware responsável por validar token JWT.
        :param projeto_middleware: Middleware com validações específicas para Projeto.
        :param projeto_control: Controlador que implementa a lógica de negócio.
        """
        print("⬆️  ProjetoRoteador.__init__()")
        self.__jwt_middleware = jwt_middleware
        self.__projeto_middleware = projeto_middleware
        self.__projeto_control = projeto_control

        # Blueprint é a coleção de rotas da entidade Projeto
        self.__blueprint = Blueprint('projeto', __name__)

    def create_routes(self):
        """
        Configura e retorna todas as rotas REST da entidade Projeto.

        Rotas implementadas:
        - POST /        -> Cria um novo projeto
        - GET /         -> Lista todos os projetos
        - GET /<id>     -> Retorna um projeto por ID
        - PUT /<id>     -> Atualiza um projeto por ID
        - DELETE /<id>  -> Remove um projeto por ID
        - GET /usuario/<usuario_id> -> Lista projetos por usuário
        """

        # POST / -> cria um projeto
        @self.__blueprint.route('/', methods=['POST'])
        @self.__jwt_middleware.validate_token
        @self.__projeto_middleware.validate_body
        def store():
            """
            Rota responsável por criar um novo projeto.
            """
            return self.__projeto_control.store()

        # GET / -> lista todos os projetos
        @self.__blueprint.route('/', methods=['GET'])
        @self.__jwt_middleware.validate_token
        def index():
            """
            Rota responsável por listar todos os projetos cadastrados no sistema.
            """
            return self.__projeto_control.index()

        # GET /<id> -> retorna um projeto específico
        @self.__blueprint.route('/<int:id>', methods=['GET'])
        @self.__jwt_middleware.validate_token
        @self.__projeto_middleware.validate_id_param
        def show(id):
            """
            Rota que retorna um projeto específico pelo seu ID.

            :param id: int - ID do projeto vindo da URI.
            """
            return self.__projeto_control.show(id)

        # PUT /<id> -> atualiza um projeto
        @self.__blueprint.route('/<int:id>', methods=['PUT'])
        @self.__jwt_middleware.validate_token
        @self.__projeto_middleware.validate_id_param
        @self.__projeto_middleware.validate_body_update
        def update(id):
            """
            Rota que atualiza um projeto existente.

            :param id: int - ID do projeto a ser atualizado.
            """
            return self.__projeto_control.update(id)

        # DELETE /<id> -> remove um projeto
        @self.__blueprint.route('/<int:id>', methods=['DELETE'])
        @self.__jwt_middleware.validate_token
        @self.__projeto_middleware.validate_id_param
        def destroy(id):
            """
            Rota que remove um projeto pelo seu ID.

            :param id: int - ID do projeto a ser removido.
            """
            return self.__projeto_control.destroy(id)

        # GET /usuario/<usuario_id> -> lista projetos por usuário
        @self.__blueprint.route('/usuario/<int:usuario_id>', methods=['GET'])
        @self.__jwt_middleware.validate_token
        @self.__projeto_middleware.validate_usuario_id_param
        def show_by_usuario(usuario_id):
            """
            Rota que retorna todos os projetos de um usuário específico.

            :param usuario_id: int - ID do usuário.
            """
            return self.__projeto_control.show_by_usuario(usuario_id)

        # Retorna o Blueprint configurado para registro na aplicação Flask
        return self.__blueprint