# -*- coding: utf-8 -*-
from flask import Blueprint, request
from api.middleware.jwt_middleware import JwtMiddleware
from api.middleware.cargo_middleware import CargoMiddleware
from api.control.cargo_control import CargoControl

class CargoRoteador:
    """
    Classe responsável por configurar todas as rotas da entidade Cargo no Flask.

    Objetivos:
    - Criar um Blueprint isolado para as rotas de Cargo.
    - Receber middlewares e controlador via injeção de dependência.
    - Aplicar autenticação JWT e validações antes de chamar o controlador.
    """

    def __init__(self, jwt_middleware: JwtMiddleware, cargo_middleware: CargoMiddleware, cargo_control: CargoControl):
        """
        Construtor do roteador.

        :param jwt_middleware: Middleware responsável por validar token JWT.
        :param cargo_middleware: Middleware com validações específicas para Cargo (ex.: validação de corpo, id).
        :param cargo_control: Controlador que implementa a lógica de negócio (store, index, update, delete, show).

        Observações:
        - Blueprint é criado para permitir o registro isolado de rotas.
        - Injeção de dependência garante desacoplamento: o roteador não precisa criar middlewares ou controlador.
        """
        print("⬆️  CargoRoteador.__init__()")
        self.__jwt_middleware = jwt_middleware
        self.__cargo_middleware = cargo_middleware
        self.__cargo_control = cargo_control

        # Blueprint é a coleção de rotas da entidade Cargo
        self.__blueprint = Blueprint('cargo', __name__)

    def create_routes(self):
        """
        Configura e retorna todas as rotas REST da entidade Cargo.

        Rotas implementadas:
        - POST /        -> Cria um novo cargo
        - GET /         -> Lista todos os cargos
        - GET /<id>     -> Retorna um cargo por ID
        - PUT /<id>     -> Atualiza um cargo por ID
        - DELETE /<id>  -> Remove um cargo por ID

        Observações:
        - Cada rota aplica autenticação JWT.
        - Middlewares de validação são aplicados diretamente.
        - Para rotas que precisam do idCargo, o parâmetro vem da URI.
        """

        # POST / -> cria um cargo
        @self.__blueprint.route('/', methods=['POST'])
        @self.__jwt_middleware.validate_token  # valida token JWT antes de executar
        @self.__cargo_middleware.validate_body  # valida corpo da requisição
        def store():
            """
            Rota responsável por criar um novo cargo.
            O corpo da requisição deve conter os dados do cargo validados pelo middleware.
            """
            return self.__cargo_control.store()

        # GET / -> lista todos os cargos
        @self.__blueprint.route('/', methods=['GET'])
        @self.__jwt_middleware.validate_token  # valida token JWT
        def index():
            """
            Rota responsável por listar todos os cargos cadastrados no sistema.
            """
            return self.__cargo_control.index()

        # GET /<idCargo> -> retorna um cargo específico
        @self.__blueprint.route('/<int:idCargo>', methods=['GET'])
        @self.__jwt_middleware.validate_token
        @self.__cargo_middleware.validate_id_param  # valida se o ID é válido
        def show(idCargo):
            """
            Rota que retorna um cargo específico pelo seu ID.

            :param idCargo: int - ID do cargo vindo da URI.
            """
            return self.__cargo_control.show(idCargo)

        # PUT /<idCargo> -> atualiza um cargo
        @self.__blueprint.route('/<int:idCargo>', methods=['PUT'])
        @self.__jwt_middleware.validate_token
        @self.__cargo_middleware.validate_id_param
        @self.__cargo_middleware.validate_body
        def update(idCargo):
            """
            Rota que atualiza um cargo existente.

            Observações:
            - idCargo vem da URI (request.view_args['idCargo']).
            - Corpo da requisição validado pelo middleware validate_body.
            """
            return self.__cargo_control.update()

        # DELETE /<idCargo> -> remove um cargo
        @self.__blueprint.route('/<int:idCargo>', methods=['DELETE'])
        @self.__jwt_middleware.validate_token
        @self.__cargo_middleware.validate_id_param
        def destroy(idCargo):
            """
            Rota que remove um cargo pelo seu ID.

            :param idCargo: int - ID do cargo a ser removido.
            """
            return self.__cargo_control.destroy()

        # Retorna o Blueprint configurado para registro na aplicação Flask
        return self.__blueprint
