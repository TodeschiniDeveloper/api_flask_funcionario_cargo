from server import Server
"""
Arquivo principal de inicialização do servidor Flask.

Responsabilidades:
- Cria a instância do servidor
- Inicializa todas as dependências (banco, middlewares, rotas)
- Inicia o servidor na porta especificada
"""
def main():
    try:
        print("🚀 Iniciando servidor Flask...")
        
        # Cria instância do servidor na porta 8080
        server = Server(porta=5000)  # Mudei para 5000 (padrão Flask)

        # Inicializa servidor (DB, middlewares, roteadores)
        server.init()

        # Inicia servidor Flask
        server.run()

    except Exception as error:
        print("❌ Erro ao iniciar o servidor:", error)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()