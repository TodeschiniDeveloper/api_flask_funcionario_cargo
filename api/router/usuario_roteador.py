# -*- coding: utf-8 -*-
from flask import Blueprint, request
from api.middleware.jwt_middleware import JwtMiddleware
from api.middleware.usuario_middleware import UsuarioMiddleware
from api.control.usuario_control import UsuarioControl

class UsuarioRoteador:
    """
    Classe responsável por configurar todas as rotas da entidade Usuario no Flask.

    Objetivos:
    - Criar um Blueprint isolado para as rotas de Usuario.
    - Receber middlewares e controlador via injeção de dependência.
    - Aplicar autenticação JWT e validações antes de chamar o controlador.
    """

    def __init__(self, jwt_middleware: JwtMiddleware, usuario_middleware: UsuarioMiddleware, usuario_control: UsuarioControl):
        """
        Construtor do roteador.

        :param jwt_middleware: Middleware responsável por validar token JWT.
        :param usuario_middleware: Middleware com validações específicas para Usuario.
        :param usuario_control: Controlador que implementa a lógica de negócio.
        """
        print("⬆️  UsuarioRoteador.__init__()")
        self.__jwt_middleware = jwt_middleware
        self.__usuario_middleware = usuario_middleware
        self.__usuario_control = usuario_control

        # Blueprint é a coleção de rotas da entidade Usuario
        self.__blueprint = Blueprint('usuario', __name__)

    def create_routes(self):
        """
        Configura e retorna todas as rotas REST da entidade Usuario.

        Rotas implementadas:
        - POST /login    -> Login de usuário
        - POST /         -> Cria um novo usuário
        - GET /          -> Lista todos os usuários
        - GET /<id>      -> Retorna um usuário por ID
        - PUT /<id>      -> Atualiza um usuário por ID
        - DELETE /<id>   -> Remove um usuário por ID
        """

        # POST /login -> autentica usuário
        @self.__blueprint.route('/login', methods=['POST'])
        @self.__usuario_middleware.validate_login_body
        def login():
            """
            Rota responsável por autenticar um usuário.
            Não requer autenticação JWT.
            """
            return self.__usuario_control.login()

        # POST / -> cria um usuário
        @self.__blueprint.route('/', methods=['POST'])
        @self.__usuario_middleware.validate_body
        def store():
            """
            Rota responsável por criar um novo usuário.
            Não requer autenticação JWT para permitir cadastro.
            """
            return self.__usuario_control.store()

        # GET / -> lista todos os usuários
        @self.__blueprint.route('/', methods=['GET'])
        @self.__jwt_middleware.validate_token
        def index():
            """
            Rota responsável por listar todos os usuários cadastrados no sistema.
            Requer autenticação JWT.
            """
            return self.__usuario_control.index()

        # GET /<id> -> retorna um usuário específico
        @self.__blueprint.route('/<int:id>', methods=['GET'])
        @self.__jwt_middleware.validate_token
        @self.__usuario_middleware.validate_id_param
        def show(id):
            """
            Rota que retorna um usuário específico pelo seu ID.
            Requer autenticação JWT.

            :param id: int - ID do usuário vindo da URI.
            """
            return self.__usuario_control.show(id)

        # PUT /<id> -> atualiza um usuário
        @self.__blueprint.route('/<int:id>', methods=['PUT'])
        @self.__jwt_middleware.validate_token
        @self.__usuario_middleware.validate_id_param
        @self.__usuario_middleware.validate_body_update
        def update(id):
            """
            Rota que atualiza um usuário existente.
            Requer autenticação JWT.

            :param id: int - ID do usuário a ser atualizado.
            """
            return self.__usuario_control.update(id)

        # DELETE /<id> -> remove um usuário
        @self.__blueprint.route('/<int:id>', methods=['DELETE'])
        @self.__jwt_middleware.validate_token
        @self.__usuario_middleware.validate_id_param
        def destroy(id):
            """
            Rota que remove um usuário pelo seu ID.
            Requer autenticação JWT.

            :param id: int - ID do usuário a ser removido.
            """
            return self.__usuario_control.destroy(id)

        # Retorna o Blueprint configurado para registro na aplicação Flask
        return self.__blueprint