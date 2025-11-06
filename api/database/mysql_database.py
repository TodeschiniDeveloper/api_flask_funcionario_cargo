# -*- coding: utf-8 -*-
import mysql.connector
from mysql.connector import pooling, Error
import sys
import os


class MysqlDatabase:
    """
    Classe responsável por gerenciar a conexão com o banco MySQL.

    Implementa um singleton usando pool de conexões para reutilização,
    garantindo eficiência e desempenho na aplicação.
    """
    __pool = None
    __instance = None

    def __init__(self, pool_name="projeto_pool", pool_size=10, pool_reset_session=True,
                 host="127.0.0.1", user="root", password="", database="projeto", port=3306):
        """
        Construtor que recebe parâmetros de configuração do pool.
        
        Configurações padrão para XAMPP:
        - host: 127.0.0.1
        - user: root  
        - password: (vazia)
        - database: projeto
        - port: 3306
        """
        self.pool_name = pool_name
        self.pool_size = pool_size
        self.pool_reset_session = pool_reset_session
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port

    def __new__(cls, *args, **kwargs):
        """
        Implementa padrão Singleton para garantir apenas uma instância.
        """
        if cls.__instance is None:
            cls.__instance = super(MysqlDatabase, cls).__new__(cls)
        return cls.__instance

    def connect(self):
        """
        Cria e retorna o pool de conexões MySQL.
        Se o pool já existir, retorna o mesmo (singleton).
        """
        if MysqlDatabase.__pool is None:
            try:
                print("🔄 Iniciando pool de conexões MySQL...")
                
                MysqlDatabase.__pool = mysql.connector.pooling.MySQLConnectionPool(
                    pool_name=self.pool_name,
                    pool_size=self.pool_size,
                    pool_reset_session=self.pool_reset_session,
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    port=self.port,
                    autocommit=False  # Controle manual de transações
                )

                # Testa a conexão
                conn = MysqlDatabase.__pool.get_connection()
                print("✅ Conectado ao MySQL (banco: projeto) com sucesso!")
                
                # Verifica versão do MySQL
                cursor = conn.cursor()
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()[0]
                print(f"📋 Versão do MySQL: {version}")
                
                cursor.close()
                conn.close()
                
            except mysql.connector.Error as err:
                print(f"❌ Falha ao conectar ao MySQL (banco: projeto): {err}")
                print(f"🔧 Configuração usada: {self.host}:{self.port}, user: {self.user}, db: {self.database}")
                sys.exit(1)
        return MysqlDatabase.__pool

    def get_connection(self):
        """
        Obtém uma conexão do pool.
        
        :return: MySQLConnection object
        :raises: mysql.connector.Error se não conseguir conexão
        """
        try:
            pool = self.connect()
            conn = pool.get_connection()
            
            # Configurações adicionais da conexão
            conn.autocommit = False
            
            return conn
        except mysql.connector.Error as err:
            print(f"❌ Erro ao obter conexão do pool: {err}")
            raise

    def execute_query(self, query: str, params: tuple = None, fetch: bool = False):
        """
        Executa uma query e retorna os resultados.
        
        :param query: SQL query string
        :param params: Tuple com parâmetros para a query
        :param fetch: Se True, retorna resultados da consulta
        :return: Resultados se fetch=True, None caso contrário
        """
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute(query, params or ())
            
            if fetch:
                result = cursor.fetchall()
                return result
            else:
                conn.commit()
                return cursor.lastrowid if query.strip().upper().startswith('INSERT') else cursor.rowcount
                
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            print(f"❌ Erro ao executar query: {err}")
            print(f"🔍 Query: {query}")
            print(f"🔍 Parâmetros: {params}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def test_connection(self):
        """
        Método para testar a conexão e verificar o estado do banco.
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            print("\n" + "="*50)
            print("🧪 TESTE DE CONEXÃO - BANCO 'projeto'")
            print("="*50)
            
            # Verifica se as tabelas existem
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print("📊 Tabelas no banco:")
            for table in tables:
                table_name = list(table.values())[0]
                print(f"   - {table_name}")
            
            # Conta registros em cada tabela
            print("\n📈 Estatísticas dos dados:")
            
            cursor.execute("SELECT COUNT(*) as total FROM usuarios")
            usuarios_count = cursor.fetchone()['total']
            print(f"   👥 Usuários: {usuarios_count}")
            
            cursor.execute("SELECT COUNT(*) as total FROM projetos")
            projetos_count = cursor.fetchone()['total']
            print(f"   📁 Projetos: {projetos_count}")
            
            cursor.execute("SELECT COUNT(*) as total FROM tarefas")
            tarefas_count = cursor.fetchone()['total']
            print(f"   ✅ Tarefas: {tarefas_count}")
            
            # Informações sobre projetos
            cursor.execute("""
                SELECT status, COUNT(*) as count 
                FROM projetos 
                GROUP BY status
            """)
            projetos_status = cursor.fetchall()
            print(f"   📋 Status dos projetos:")
            for status in projetos_status:
                print(f"     - {status['status']}: {status['count']}")
            
            # Informações sobre tarefas
            cursor.execute("""
                SELECT 
                    COUNT(*) as total,
                    SUM(concluida) as concluidas,
                    COUNT(*) - SUM(concluida) as pendentes
                FROM tarefas
            """)
            tarefas_stats = cursor.fetchone()
            print(f"   📊 Tarefas: {tarefas_stats['total']} total, "
                  f"{tarefas_stats['concluidas']} concluídas, "
                  f"{tarefas_stats['pendentes']} pendentes")
            
            cursor.close()
            conn.close()
            
            print("✅ Teste de conexão concluído com sucesso!")
            return True
            
        except mysql.connector.Error as err:
            print(f"❌ Erro ao testar conexão: {err}")
            return False

    def get_pool_status(self):
        """
        Retorna informações sobre o estado do pool de conexões.
        """
        if MysqlDatabase.__pool is None:
            return {"status": "Pool não inicializado"}
        
        return {
            "status": "Ativo",
            "pool_name": self.pool_name,
            "pool_size": self.pool_size,
            "database": self.database
        }

    def close_pool(self):
        """
        Fecha todas as conexões do pool.
        Útil para shutdown graceful da aplicação.
        """
        if MysqlDatabase.__pool is not None:
            print("🔒 Fechando pool de conexões MySQL...")
            # O pool fecha automaticamente quando não há mais referências
            MysqlDatabase.__pool = None
            MysqlDatabase.__instance = None
            print("✅ Pool de conexões fechado.")


# Função auxiliar para criar instância configurada
def create_database_instance():
    """
    Factory function para criar instância do banco com configurações padrão.
    
    Pode ser customizada com variáveis de ambiente:
    - MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE, MYSQL_PORT
    """
    config = {
        'host': os.getenv('MYSQL_HOST', '127.0.0.1'),
        'user': os.getenv('MYSQL_USER', 'root'),
        'password': os.getenv('MYSQL_PASSWORD', ''),
        'database': os.getenv('MYSQL_DATABASE', 'projeto'),
        'port': int(os.getenv('MYSQL_PORT', '3306')),
        'pool_size': int(os.getenv('MYSQL_POOL_SIZE', '10'))
    }
    
    return MysqlDatabase(**config)


# Exemplo de uso
if __name__ == "__main__":
    # Teste da classe
    print("🧪 Testando conexão com o banco 'projeto'...")
    
    db = create_database_instance()
    
    # Testa a conexão
    if db.test_connection():
        print("\n🎉 Conexão estabelecida com sucesso!")
        
        # Mostra status do pool
        pool_status = db.get_pool_status()
        print(f"\n📊 Status do pool: {pool_status}")
        
        # Exemplo de query
        try:
            usuarios = db.execute_query("SELECT id, nome, email FROM usuarios LIMIT 5", fetch=True)
            print(f"\n👥 Primeiros 5 usuários:")
            for usuario in usuarios:
                print(f"   - {usuario['nome']} ({usuario['email']})")
        except Exception as e:
            print(f"❌ Erro ao executar query de exemplo: {e}")
    else:
        print("\n💥 Falha na conexão com o banco!")