# -*- coding: utf-8 -*-
from flask import request, jsonify
import traceback
from api.service.funcionario_service import FuncionarioService
"""
Classe responsável por controlar os endpoints da API REST para a entidade Funcionario.

Implementa métodos de CRUD e autenticação, utilizando injeção de dependência
para receber a instância de FuncionarioService, desacoplando a lógica de negócio
da camada de controle.
"""
class FuncionarioControl:
    def __init__(self, funcionario_service: FuncionarioService):
        """
        Construtor da classe FuncionarioControl
        :param funcionario_service: Instância do FuncionarioService (injeção de dependência)
        """
        print("⬆️  FuncionarioControl.constructor()")
        self.__funcionario_service = funcionario_service

    def login(self):
        print ("🔵 FuncionarioControl.login()")
        """Autentica um funcionário pelo email e senha"""
        
        json_funcionario = request.json.get("funcionario")
        resultado = self.__funcionario_service.loginFuncionario(json_funcionario)
        return jsonify({
            "success": True,
            "message": "Login efetuado com sucesso!",
            "data": resultado
        }), 201
    

    def store(self):
        """Cria um novo funcionário"""
        print("🔵 FuncionarioControl.store()")
        
        json_funcionario = request.json.get("funcionario")
        newIdFuncionario = self.__funcionario_service.createFuncionario(json_funcionario)
        return jsonify({
        "success": True,
        "message": "Cadastro realizado com sucesso",
        "data": {
            "funcionario": {
                "idFuncionario": newIdFuncionario,
                "nomeFuncionario": json_funcionario.get("nomeFuncionario"),
                "email": json_funcionario.get("email"),
                "senha": json_funcionario.get("senha"),  # se quiser incluir hash
                "recebeValeTransporte": json_funcionario.get("recebeValeTransporte"),
                "cargo": {
                    "idCargo": json_funcionario.get("cargo", {}).get("idCargo"),
                    "nomeCargo": json_funcionario.get("cargo", {}).get("nomeCargo")
                }
                # Adicione aqui outros atributos do funcionário, se houver
            }
        }
    }), 201
        

    def index(self):
        """Lista todos os funcionários cadastrados"""
        
        lista_funcionarios = self.__funcionario_service.findAll()
        return jsonify({
            "success": True,
            "message": "Executado com sucesso",
            "data": {"funcionarios": lista_funcionarios}
        }), 200
        

    def show(self, idFuncionario):
        """Busca um funcionário pelo ID"""
        
        funcionario = self.__funcionario_service.findById(idFuncionario)
        return jsonify({
            "success": True,
            "message": "Executado com sucesso",
            "data": funcionario
        }), 200
        

    def update(self, idFuncionario):
        """Atualiza os dados de um funcionário existente"""
        funcionario_atualizado = self.__funcionario_service.updateFuncionario(idFuncionario, request.json)

        if funcionario_atualizado: 
            return jsonify({
                "success": True,
                "message": "Atualizado com sucesso",
                "data": {
                    "funcionario": {
                        "idFuncionario": int(idFuncionario),
                        "nomeFuncionario": request.json.get("funcionario", {}).get("nomeFuncionario")
                    }
                }
            }), 200
        else:
            # Caso não tenha conseguido atualizar
            return jsonify({
                "success": False,
                "error": {
                    "message": f"Não foi possível atualizar o funcionário com ID {idFuncionario}",
                    "code": 404
                },
                "data": {}
            }), 404

    def destroy(self, idFuncionario):
        """Remove um funcionário pelo ID"""
        
        excluiu = self.__funcionario_service.deleteFuncionario(idFuncionario)
        if not excluiu:
            return jsonify({
                "success": False,
                "message": "Funcionário não encontrado",
                "error": {"message": f"Não existe funcionário com id {idFuncionario}"}
            }), 404

        return jsonify({
            "success": True,
            "message": "Excluído com sucesso"
        }), 204
        
