# -*- coding: utf-8 -*-
from functools import wraps
from flask import request
from api.utils.error_response import ErrorResponse

class FuncionarioMiddleware:
    """
    Middleware para validação de requisições relacionadas à entidade Funcionario.

    Objetivos:
    - Garantir que os campos obrigatórios existam antes de chamar os métodos do Controller ou Service.
    - Lançar erros padronizados usando ErrorResponse quando a validação falhar.
    """

    def validate_create_body(self, f):
        """
        Decorator para validar o corpo da requisição para criação de um novo funcionário.

        Verifica apenas a existência:
        - O objeto 'funcionario' existe
        - Campos obrigatórios: nomeFuncionario, email, senha, recebeValeTransporte
        - Objeto 'cargo' existe com campo 'idCargo'
        """
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print("🔷 FuncionarioMiddleware.validate_create_body()")
            body = request.get_json()
            
            if not body or 'funcionario' not in body:
                raise ErrorResponse(400, "Erro na validação de dados", {"message": "O campo 'funcionario' é obrigatório!"})

            funcionario = body['funcionario']

            # Apenas verificar existência dos campos obrigatórios
            campos_obrigatorios = ["nomeFuncionario", "email", "senha", "recebeValeTransporte"]
            for campo in campos_obrigatorios:
                if campo not in funcionario:
                    raise ErrorResponse(400, "Erro na validação de dados", {"message": f"O campo '{campo}' é obrigatório!"})

            if 'cargo' not in funcionario or 'idCargo' not in funcionario['cargo']:
                raise ErrorResponse(400, "Erro na validação de dados", {"message": "O campo 'cargo.idCargo' é obrigatório!"})

            return f(*args, **kwargs)
        return decorated_function

    def validate_login_body(self, f):
        """
        Decorator para validar o corpo da requisição para login de um funcionário.

        Verifica apenas a existência:
        - O objeto 'funcionario' existe
        - Campos obrigatórios: email, senha
        """
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print("🔷 FuncionarioMiddleware.validate_login_body()")
            body = request.get_json()

            if not body or 'funcionario' not in body:
                raise ErrorResponse(400, "Erro na validação de dados", {"message": "O campo 'funcionario' é obrigatório!"})

            funcionario = body['funcionario']

            campos_obrigatorios = ["email", "senha"]
            for campo in campos_obrigatorios:
                if campo not in funcionario:
                    raise ErrorResponse(400, "Erro na validação de dados", {"message": f"O campo '{campo}' é obrigatório!"})

            return f(*args, **kwargs)
        return decorated_function

    def validate_id_param(self, f):
        """
        Decorator para validar o parâmetro de rota 'idFuncionario'.

        Verifica apenas a existência do parâmetro.
        """
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print("🔷 FuncionarioMiddleware.validate_id_param()")
            if 'idFuncionario' not in kwargs:
                raise ErrorResponse(400, "Erro na validação de dados", {"message": "O parâmetro 'idFuncionario' é obrigatório!"})
            return f(*args, **kwargs)
        return decorated_function
