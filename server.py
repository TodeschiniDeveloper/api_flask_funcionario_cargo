# -*- coding: utf-8 -*-
from flask import Flask
from flask_cors import CORS
import sys
import os

# Adiciona o diretório raiz ao path para imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.http.mysql_database import MysqlDatabase, create_database_instance
from api.http.meu_token_jwt import MeuTokenJWT
from api.middleware.jwt_middleware import JwtMiddleware
from api.middleware.usuario_middleware import UsuarioMiddleware
from api.middleware.projeto_middleware import ProjetoMiddleware
from api.middleware.tarefa_middleware import TarefaMiddleware

from api.dao.usuario_dao import UsuarioDAO
from api.dao.projeto_dao import ProjetoDAO
from api.dao.tarefa_dao import TarefaDAO

from api.service.usuario_service import UsuarioService
from api.service.projeto_service import ProjetoService
from api.service.tarefa_service import TarefaService

from api.control.usuario_control import UsuarioControl
from api.control.projeto_control import ProjetoControl
from api.control.tarefa_control import TarefaControl

from api.roteador.usuario_roteador import UsuarioRoteador
from api.roteador.projeto_roteador import ProjetoRoteador
from api.roteador.tarefa_roteador import TarefaRoteador


class Server:
    """
    Classe principal do servidor Flask.
    
    Responsável por:
    - Configurar a aplicação Flask
    - Inicializar todas as dependências
    - Registrar blueprints (rotas)
    - Gerenciar ciclo de vida do servidor
    """
    
    def __init__(self, porta=5000, host='0.0.0.0', debug=True):
        """
        Construtor do servidor.
        
        :param porta: Porta do servidor
        :param host: Host do servidor
        :param debug: Modo debug
        """
        self.porta = porta
        self.host = host
        self.debug = debug
        self.app = None
        self.database = None
        self.dependencies = {}

    def init(self):
        """
        Inicializa todas as dependências do servidor.
        """
        print("🔄 Inicializando servidor...")
        
        # 1. Criar aplicação Flask
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'chave_secreta_projeto_mvcs'
        
        # 2. Configurar CORS
        CORS(self.app, resources={
            r"/api/*": {
                "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
                "methods": ["GET", "POST", "PUT", "DELETE"],
                "allow_headers": ["Content-Type", "Authorization"]
            }
        })
        
        # 3. Inicializar banco de dados
        self._init_database()
        
        # 4. Configurar dependências
        self._configure_dependencies()
        
        # 5. Registrar rotas
        self._register_routes()
        
        # 6. Configurar error handlers
        self._configure_error_handlers()
        
        print("✅ Servidor inicializado com sucesso!")

    def _init_database(self):
        """Inicializa e testa a conexão com o banco de dados."""
        print("🗄️  Inicializando banco de dados...")
        try:
            self.database = create_database_instance()
            
            # Testar conexão
            if self.database.test_connection():
                print("✅ Conexão com banco de dados estabelecida")
            else:
                raise Exception("Falha ao conectar com o banco de dados")
                
        except Exception as e:
            print(f"❌ Erro ao inicializar banco de dados: {e}")
            raise

    def _configure_dependencies(self):
        """Configura todas as dependências do sistema (Injeção de Dependência)."""
        print("🔗 Configurando dependências...")
        
        try:
            # JWT
            jwt_instance = MeuTokenJWT()
            jwt_middleware = JwtMiddleware(jwt_instance)
            
            # DAOs
            usuario_dao = UsuarioDAO(self.database)
            projeto_dao = ProjetoDAO(self.database)
            tarefa_dao = TarefaDAO(self.database)
            
            # Services
            usuario_service = UsuarioService(usuario_dao)
            projeto_service = ProjetoService(projeto_dao, usuario_dao)
            tarefa_service = TarefaService(tarefa_dao, projeto_dao)
            
            # Middlewares
            usuario_middleware = UsuarioMiddleware()
            projeto_middleware = ProjetoMiddleware()
            tarefa_middleware = TarefaMiddleware()
            
            # Controls
            usuario_control = UsuarioControl(usuario_service)
            projeto_control = ProjetoControl(projeto_service)
            tarefa_control = TarefaControl(tarefa_service)
            
            # Roteadores
            usuario_roteador = UsuarioRoteador(jwt_middleware, usuario_middleware, usuario_control)
            projeto_roteador = ProjetoRoteador(jwt_middleware, projeto_middleware, projeto_control)
            tarefa_roteador = TarefaRoteador(jwt_middleware, tarefa_middleware, tarefa_control)
            
            # Salvar dependências
            self.dependencies = {
                'jwt_middleware': jwt_middleware,
                'usuario_roteador': usuario_roteador,
                'projeto_roteador': projeto_roteador,
                'tarefa_roteador': tarefa_roteador
            }
            
            print("✅ Dependências configuradas com sucesso")
            
        except Exception as e:
            print(f"❌ Erro ao configurar dependências: {e}")
            raise

    def _register_routes(self):
        """Registra todos os blueprints (rotas) na aplicação Flask."""
        print("🛣️  Registrando rotas...")
        
        try:
            # Registrar blueprints com prefixo /api
            self.app.register_blueprint(
                self.dependencies['usuario_roteador'].create_routes(),
                url_prefix='/api/usuarios'
            )
            self.app.register_blueprint(
                self.dependencies['projeto_roteador'].create_routes(),
                url_prefix='/api/projetos'
            )
            self.app.register_blueprint(
                self.dependencies['tarefa_roteador'].create_routes(),
                url_prefix='/api/tarefas'
            )
            
            # Rota de health check
            @self.app.route('/api/health')
            def health_check():
                return {
                    "status": "healthy",
                    "message": "Servidor funcionando corretamente",
                    "timestamp": "2024-01-01T00:00:00Z"  # Você pode usar datetime aqui
                }
            
            # Rota raiz
            @self.app.route('/')
            def index():
                return {
                    "message": "Bem-vindo ao Sistema de Gerenciamento de Projetos",
                    "version": "1.0.0",
                    "endpoints": {
                        "usuarios": "/api/usuarios",
                        "projetos": "/api/projetos",
                        "tarefas": "/api/tarefas",
                        "health": "/api/health"
                    }
                }
            
            print("✅ Rotas registradas com sucesso")
            
        except Exception as e:
            print(f"❌ Erro ao registrar rotas: {e}")
            raise

    def _configure_error_handlers(self):
        """Configura handlers de erro globais."""
        print("⚙️  Configurando handlers de erro...")
        
        @self.app.errorhandler(404)
        def not_found(error):
            return {
                "success": False,
                "error": {
                    "message": "Endpoint não encontrado",
                    "code": 404
                }
            }, 404

        @self.app.errorhandler(500)
        def internal_error(error):
            return {
                "success": False,
                "error": {
                    "message": "Erro interno do servidor",
                    "code": 500
                }
            }, 500

    def run(self):
        """
        Inicia o servidor Flask.
        """
        if not self.app:
            raise Exception("Servidor não inicializado. Chame init() primeiro.")
        
        print(f"🌐 Servidor iniciado em http://{self.host}:{self.porta}")
        print("📋 Endpoints disponíveis:")
        print("   👥 /api/usuarios/*")
        print("   📁 /api/projetos/*") 
        print("   ✅ /api/tarefas/*")
        print("   ❤️  /api/health")
        print("\n⏹️  Pressione CTRL+C para parar o servidor")
        
        self.app.run(
            host=self.host,
            port=self.porta,
            debug=self.debug,
            use_reloader=False
        )

    def shutdown(self):
        """Desliga o servidor gracefulmente."""
        print("🔒 Encerrando servidor...")
        if self.database:
            self.database.close_pool()
        print("✅ Servidor encerrado")


# Para uso com Gunicorn ou outros WSGI servers
def create_app():
    """Factory function para criação da app (uso com Gunicorn)."""
    server = Server()
    server.init()
    return server.app


if __name__ == "__main__":
    # Para teste direto
    server = Server()
    server.init()
    server.run()