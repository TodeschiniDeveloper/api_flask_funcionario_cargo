# -*- coding: utf-8 -*-
from flask import request, jsonify
import traceback
from api.service.projeto_service import ProjetoService
from api.utils.error_response import ErrorResponse

"""
Classe responsável por controlar os endpoints da API REST para a entidade Projeto.

Implementa métodos de CRUD, utilizando injeção de dependência
para receber a instância de ProjetoService, desacoplando a lógica de negócio
da camada de controle.
"""
class ProjetoControl:
    def __init__(self, projeto_service: ProjetoService):
        """
        Construtor da classe ProjetoControl
        :param projeto_service: Instância do ProjetoService (injeção de dependência)
        """
        print("⬆️  ProjetoControl.constructor()")
        self.__projeto_service = projeto_service

    def store(self):
        """Cria um novo projeto"""
        print("🔵 ProjetoControl.store()")
        try:
            json_projeto = request.json.get("projeto")
            newIdProjeto = self.__projeto_service.createProjeto(json_projeto)
            return jsonify({
                "success": True,
                "message": "Projeto criado com sucesso",
                "data": {
                    "projeto": {
                        "id": newIdProjeto,
                        "nome": json_projeto.get("nome"),
                        "descricao": json_projeto.get("descricao"),
                        "data_inicio": json_projeto.get("data_inicio"),
                        "status": json_projeto.get("status", "Pendente"),
                        "usuario_id": json_projeto.get("usuario_id")
                    }
                }
            }), 201
        except ErrorResponse as e:
            return jsonify({
                "success": False,
                "error": {
                    "message": e.message,
                    "details": e.details,
                    "code": e.status_code
                }
            }), e.status_code
        except Exception as e:
            print(f"❌ Erro inesperado em store: {traceback.format_exc()}")
            return jsonify({
                "success": False,
                "error": {
                    "message": "Erro interno no servidor",
                    "code": 500
                }
            }), 500

    def index(self):
        """Lista todos os projetos cadastrados"""
        print("🔵 ProjetoControl.index()")
        try:
            lista_projetos = self.__projeto_service.findAll()
            return jsonify({
                "success": True,
                "message": "Executado com sucesso",
                "data": {"projetos": lista_projetos}
            }), 200
        except Exception as e:
            print(f"❌ Erro inesperado em index: {traceback.format_exc()}")
            return jsonify({
                "success": False,
                "error": {
                    "message": "Erro interno no servidor",
                    "code": 500
                }
            }), 500

    def show(self, id):
        """Busca um projeto pelo ID"""
        print("🔵 ProjetoControl.show()")
        try:
            projeto = self.__projeto_service.findById(id)
            return jsonify({
                "success": True,
                "message": "Executado com sucesso",
                "data": projeto
            }), 200
        except ErrorResponse as e:
            return jsonify({
                "success": False,
                "error": {
                    "message": e.message,
                    "details": e.details,
                    "code": e.status_code
                }
            }), e.status_code
        except Exception as e:
            print(f"❌ Erro inesperado em show: {traceback.format_exc()}")
            return jsonify({
                "success": False,
                "error": {
                    "message": "Erro interno no servidor",
                    "code": 500
                }
            }), 500

    def update(self, id):
        """Atualiza os dados de um projeto existente"""
        print("🔵 ProjetoControl.update()")
        try:
            projeto_atualizado = self.__projeto_service.updateProjeto(id, request.json)

            return jsonify({
                "success": True,
                "message": "Projeto atualizado com sucesso",
                "data": {
                    "projeto": {
                        "id": int(id),
                        "nome": request.json.get("projeto", {}).get("nome"),
                        "status": request.json.get("projeto", {}).get("status")
                    }
                }
            }), 200
        except ErrorResponse as e:
            return jsonify({
                "success": False,
                "error": {
                    "message": e.message,
                    "details": e.details,
                    "code": e.status_code
                }
            }), e.status_code
        except Exception as e:
            print(f"❌ Erro inesperado em update: {traceback.format_exc()}")
            return jsonify({
                "success": False,
                "error": {
                    "message": "Erro interno no servidor",
                    "code": 500
                }
            }), 500

    def destroy(self, id):
        """Remove um projeto pelo ID"""
        print("🔵 ProjetoControl.destroy()")
        try:
            excluiu = self.__projeto_service.deleteProjeto(id)
            return jsonify({
                "success": True,
                "message": "Projeto excluído com sucesso"
            }), 200
        except ErrorResponse as e:
            return jsonify({
                "success": False,
                "error": {
                    "message": e.message,
                    "details": e.details,
                    "code": e.status_code
                }
            }), e.status_code
        except Exception as e:
            print(f"❌ Erro inesperado em destroy: {traceback.format_exc()}")
            return jsonify({
                "success": False,
                "error": {
                    "message": "Erro interno no servidor",
                    "code": 500
                }
            }), 500

    def show_by_usuario(self, usuario_id):
        """Lista todos os projetos de um usuário específico"""
        print("🔵 ProjetoControl.show_by_usuario()")
        try:
            projetos = self.__projeto_service.findByUsuarioId(usuario_id)
            return jsonify({
                "success": True,
                "message": "Executado com sucesso",
                "data": {"projetos": projetos}
            }), 200
        except ErrorResponse as e:
            return jsonify({
                "success": False,
                "error": {
                    "message": e.message,
                    "details": e.details,
                    "code": e.status_code
                }
            }), e.status_code
        except Exception as e:
            print(f"❌ Erro inesperado em show_by_usuario: {traceback.format_exc()}")
            return jsonify({
                "success": False,
                "error": {
                    "message": "Erro interno no servidor",
                    "code": 500
                }
            }), 500