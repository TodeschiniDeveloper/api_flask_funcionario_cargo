from flask import request, jsonify
from api.service.cargo_service import CargoService
"""
Classe responsável por controlar os endpoints da API REST para a entidade Cargo.

Esta classe implementa métodos CRUD e utiliza injeção de dependência
para receber a instância de CargoService, desacoplando a lógica de negócio
da camada de controle.
"""
class CargoControl:
    def __init__(self, cargo_service:CargoService):
        """
        Construtor da classe CargoControl
        :param cargo_service: Instância do CargoService (injeção de dependência)
        """
        print("⬆️  CargoControl.constructor()")
        self.__cargo_service = cargo_service

    def store(self):
        """Cria um novo cargo"""
        print("🔵 CargoControle.store()")
       
        cargo_body_request = request.json.get("cargo")
        novo_id = self.__cargo_service.createCargo(cargo_body_request)

        obj_resposta = {
            "success": True,
            "message": "Cadastro realizado com sucesso",
            "data": {
                "cargos": [
                    {
                        "idCargo": novo_id,
                        "nomeCargo": cargo_body_request.get("nomeCargo")
                    }
                ]
            }
        }

        if novo_id:
            return jsonify(obj_resposta), 200
        

    def index(self):
        """Lista todos os cargos cadastrados"""
        print("🔵 CargoControle.index()")
       
        array_cargos = self.__cargo_service.findAll()
        
        return jsonify({
            "success": True,
            "message": "Busca realizada com sucesso",
            "data": {"cargos": array_cargos}
        }), 200
        

    def show(self):
          # Pega o idCargo diretamente da URI
        idCargo = request.view_args.get("idCargo")

        cargo = self.__cargo_service.findById(idCargo)
        obj_resposta = {
            "success": True,
            "message": "Executado com sucesso",
            "data": {"cargos": cargo}
        }
        return jsonify(obj_resposta), 200
      

    def update(self):
        """Atualiza os dados de um cargo existente"""
        print("🔵 CargoControle.update()")
       
        # Pega o idCargo diretamente da URI
        idCargo = request.view_args.get("idCargo")

        # Pega os dados do cargo no corpo da requisição
        json_cargo = request.json.get("cargo")
        print(json_cargo)

        resposta = self.__cargo_service.updateCargo(idCargo, json_cargo)
        return jsonify({
            "success": True,
            "message": "Cargo atualizado com sucesso",
            "data": {
                "cargo": {
                    "idCargo": int(idCargo),
                    "nomeCargo": json_cargo.get("nomeCargo")
                }
            }
        }), 200
   

    def destroy(self):
        """Remove um cargo pelo ID"""
        print("🔵 CargoControle.destroy()")
        # Pega o idCargo diretamente da URI
        idCargo = request.view_args.get("idCargo")
        
        excluiu = self.__cargo_service.deleteCargo(idCargo)
        if not excluiu:
            return jsonify({
                "success": False,
                "message": f"Não existe Cargo com id {idCargo}"
            }), 404

        return jsonify({
            "success": True,
            "message": "Excluído com sucesso"
        }), 204
        
