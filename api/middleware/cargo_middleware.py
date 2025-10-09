# -*- coding: utf-8 -*-
from functools import wraps
from flask import request
from api.utils.error_response import ErrorResponse

class CargoMiddleware:
    """
    Middleware para validação de requisições relacionadas à entidade Cargo.

    Objetivos:
    - Garantir que os dados obrigatórios estejam presentes antes de chamar
      os métodos do Controller ou Service.
    - Lançar erros padronizados usando ErrorResponse quando a validação falhar.
    """

    def validate_body(self, f):
        """
        Decorator para validar o corpo da requisição (JSON) para operações de Cargo.

        Verifica apenas a existência:
        - O objeto 'cargo' existe
        - O campo obrigatório 'nomeCargo' está presente
        """
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print("🔷 CargoMiddleware.validate_body()")
            body = request.get_json()

            if not body or 'cargo' not in body:
                raise ErrorResponse(
                    400, "Erro na validação de dados",
                    {"message": "O campo 'cargo' é obrigatório!"}
                )

            cargo = body['cargo']
            if 'nomeCargo' not in cargo:
                raise ErrorResponse(
                    400, "Erro na validação de dados",
                    {"message": "O campo 'nomeCargo' é obrigatório!"}
                )

            return f(*args, **kwargs)
        return decorated_function

    def validate_id_param(self, f):
        """
        Decorator para validar o parâmetro de rota 'idCargo'.

        Verifica apenas a existência do parâmetro.
        """
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print("🔷 CargoMiddleware.validate_id_param()")
            if 'idCargo' not in kwargs:
                raise ErrorResponse(
                    400, "Erro na validação de dados",
                    {"message": "O parâmetro 'idCargo' é obrigatório!"}
                )
            return f(*args, **kwargs)
        return decorated_function
