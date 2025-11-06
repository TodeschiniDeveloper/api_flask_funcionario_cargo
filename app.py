from server import Server
from datetime import datetime

"""
Arquivo principal de inicialização do servidor Flask.
"""

def main():
    try:
        print("🚀 Iniciando servidor Flask...")
        print(f"⏰ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        
        # Cria instância do servidor
        server = Server(porta=5000)  # CORRIGIDO: apenas 5000

        # Inicializa servidor
        server.init()

        # Inicia servidor Flask
        server.run()

    except Exception as error:
        print(f"❌ Erro ao iniciar o servidor: {error}")
        print("💡 Possíveis soluções:")
        print("   - Verifique se o MySQL está rodando no XAMPP")
        print("   - Confirme se a porta 5000 está livre")
        print("   - Verifique as credenciais do banco de dados")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()