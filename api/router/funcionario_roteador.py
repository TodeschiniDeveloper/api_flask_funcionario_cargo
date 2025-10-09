# -*- coding: utf-8 -*-
from flask import Blueprint, request
from functools import wraps
from api.middleware.jwt_middleware import JwtMiddleware
from api.middleware.funcionario_middleware import FuncionarioMiddleware
from api.control.funcionario_control import FuncionarioControl

class FuncionarioRoteador:
    """
    Classe responsável por configurar as rotas da entidade Funcionario no Flask.
    Utiliza middlewares e controlador via injeção de dependência.
    """

    def __init__(self, jwt_middleware:JwtMiddleware, funcionario_middleware:FuncionarioMiddleware, funcionario_control:FuncionarioControl):
        """
        Construtor da classe.

        :param jwt_middleware: Middleware para validação de tokens JWT.
        :param funcionario_middleware: Middleware para validar parâmetros e corpo da requisição.
        :param funcionario_control: Controlador responsável pela lógica de negócio da entidade Funcionario.
        """
        print("⬆️  FuncionarioRoteador.__init__()")
        self.jwt_middleware = jwt_middleware
        self.funcionario_middleware = funcionario_middleware
        self.funcionario_control = funcionario_control
        # Cria um Blueprint específico para as rotas de funcionário
        self.blueprint = Blueprint('funcionario', __name__)

    def create_routes(self):
        """
        Configura as rotas da API REST para a entidade Funcionario.
        Cada rota aplica middlewares e chama o método correspondente do controlador.
        """

        # Rota de login (não requer JWT, apenas validação do corpo da requisição)
        @self.blueprint.route('/login', methods=['POST'])
        @self._flask_decorator(self.funcionario_middleware.validate_login_body)
        def login():
            print("funcionarioRoteador.login()")
            # Chama o controlador para autenticar o usuário
            return self.funcionario_control.login()

        # Rota para criar um funcionário (requer JWT e validação do corpo)
        # POST / -> cria um funcionário
        @self.blueprint.route('/', methods=['POST'])
        @self.jwt_middleware.validate_token
        @self._flask_decorator(self.funcionario_middleware.validate_create_body)
        def store():
            # Delegamos a lógica de criação ao controlador
            return self.funcionario_control.store()

        # Rota para atualizar um funcionário específico (requer JWT, validação do ID e corpo)
        # PUT / -> Atualiza um funcionário
        @self.blueprint.route('/<int:idFuncionario>', methods=['PUT'])
        @self.jwt_middleware.validate_token
        @self._flask_decorator(self.funcionario_middleware.validate_id_param)
        @self._flask_decorator(self.funcionario_middleware.validate_create_body)
        def update(idFuncionario):
            # Passa o objeto request e o ID ao controlador
            return self.funcionario_control.update(idFuncionario)

        # Rota para excluir um funcionário pelo ID (requer JWT e validação do ID)
        # DELETE / -> exclui um funcionário
        @self.blueprint.route('/<int:idFuncionario>', methods=['DELETE'])
        @self.jwt_middleware.validate_token
        @self._flask_decorator(self.funcionario_middleware.validate_id_param)
        def destroy(idFuncionario):
            # Chama o controlador para deletar o funcionário
            return self.funcionario_control.destroy(idFuncionario)

        # Rota para listar todos os funcionários (requer JWT)
        # GET / -> Lista todos os funcionários
        @self.blueprint.route('/', methods=['GET'])
        @self.jwt_middleware.validate_token
        def index():
            # Retorna lista de funcionários
            return self.funcionario_control.index()

        # Rota para buscar um funcionário específico pelo ID (requer JWT e validação do ID)
        # GET /<idFuncionario> -> retorna um funcionario específico
        @self.blueprint.route('/<int:idFuncionario>', methods=['GET'])
        @self.jwt_middleware.validate_token
        @self._flask_decorator(self.funcionario_middleware.validate_id_param)
        def show(idFuncionario):
            # Busca funcionário pelo ID
            return self.funcionario_control.show(idFuncionario)

        # Retorna o blueprint configurado, para ser registrado no app Flask
        return self.blueprint

    def _flask_decorator(self, middleware_func):
        """
        Converte funções de middleware estilo Node.js em decorators Flask.
        Isso permite reaproveitar middlewares que recebem 'request' como parâmetro.
        
        :param middleware_func: Função middleware que recebe 'request'.
        :return: Decorator compatível com Flask.
        """
        def decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                # Executa o middleware antes de chamar a função original
                middleware_func(request)
                return f(*args, **kwargs)
            return wrapper
        return decorator
