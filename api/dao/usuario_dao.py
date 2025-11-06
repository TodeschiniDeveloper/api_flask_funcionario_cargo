# -*- coding: utf-8 -*-
import bcrypt
from api.model.usuario import Usuario
from api.utils.error_response import ErrorResponse

"""
Classe responsável por gerenciar operações CRUD e autenticação
para a entidade Usuario no banco de dados.
"""

class UsuarioDAO:
    def __init__(self, database_dependency):
        print("⬆️  UsuarioDAO.__init__()")
        self.__database = database_dependency

    def create(self, objUsuario: Usuario) -> int:
        print("🟢 UsuarioDAO.create()")
        try:
            hashed = bcrypt.hashpw(objUsuario.senha_hash.encode("utf-8"), bcrypt.gensalt())
            objUsuario.senha_hash = hashed.decode("utf-8")

            SQL = """
                INSERT INTO usuarios 
                (nome, email, senha_hash) 
                VALUES (%s, %s, %s);
            """
            params = (
                objUsuario.nome,
                objUsuario.email,
                objUsuario.senha_hash,
            )

            insert_id = self.__database.execute_query(SQL, params)
            
            if not insert_id:
                raise Exception("Falha ao inserir usuário")
            return insert_id
            
        except Exception as e:
            print(f"❌ Erro em UsuarioDAO.create(): {e}")
            raise

    def delete(self, id: int) -> bool:
        print("🟢 UsuarioDAO.delete()")
        try:
            SQL = "DELETE FROM usuarios WHERE id = %s;"
            affected = self.__database.execute_query(SQL, (id,))
            return affected > 0
        except Exception as e:
            print(f"❌ Erro em UsuarioDAO.delete(): {e}")
            raise

    def update(self, objUsuario: Usuario) -> bool:
        print("🟢 UsuarioDAO.update()")
        try:
            if objUsuario.senha_hash:
                senhaHash = bcrypt.hashpw(objUsuario.senha_hash.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
                SQL = """
                    UPDATE usuarios 
                    SET nome=%s, email=%s, senha_hash=%s 
                    WHERE id=%s;
                """
                params = (
                    objUsuario.nome,
                    objUsuario.email,
                    senhaHash,
                    objUsuario.id,
                )
            else:
                SQL = """
                    UPDATE usuarios 
                    SET nome=%s, email=%s 
                    WHERE id=%s;
                """
                params = (
                    objUsuario.nome,
                    objUsuario.email,
                    objUsuario.id,
                )

            affected = self.__database.execute_query(SQL, params)
            return affected > 0
            
        except Exception as e:
            print(f"❌ Erro em UsuarioDAO.update(): {e}")
            raise

    def findAll(self) -> list[dict]:
        print("🟢 UsuarioDAO.findAll()")
        try:
            SQL = """
                SELECT id, nome, email, data_criacao 
                FROM usuarios;
            """
            rows = self.__database.execute_query(SQL, fetch=True)

            usuarios = [
                {
                    "id": row["id"],
                    "nome": row["nome"],
                    "email": row["email"],
                    "data_criacao": row["data_criacao"].isoformat() if row["data_criacao"] else None
                }
                for row in rows
            ]
            return usuarios
        except Exception as e:
            print(f"❌ Erro em UsuarioDAO.findAll(): {e}")
            raise

    def findById(self, id: int) -> dict | None:
        print("✅ UsuarioDAO.findById()")
        try:
            usuariosRaw = self.findByField("id", id)
            return usuariosRaw[0] if usuariosRaw else None
        except Exception as e:
            print(f"❌ Erro em UsuarioDAO.findById(): {e}")
            raise

    def findByField(self, campo: str, valor) -> list[dict]:
        print(f"🟢 UsuarioDAO.findByField() - Campo: {campo}, Valor: {valor}")
        try:
            allowedFields = ["id", "nome", "email"]
            if campo not in allowedFields:
                raise ValueError("Campo inválido para busca")

            SQL = f"SELECT * FROM usuarios WHERE {campo} = %s;"
            resultados = self.__database.execute_query(SQL, (valor,), fetch=True)
            return resultados
        except Exception as e:
            print(f"❌ Erro em UsuarioDAO.findByField(): {e}")
            raise

    def login(self, objUsuario: Usuario) -> Usuario | None:
        print("🟢 UsuarioDAO.login()")
        try:
            SQL = """
                SELECT 
                    id, 
                    nome,
                    email, 
                    senha_hash
                FROM usuarios
                WHERE email=%s;
            """
            rows = self.__database.execute_query(SQL, (objUsuario.email,), fetch=True)

            if len(rows) != 1:
                print("❌ Usuário não encontrado")
                return None

            usuarioDB = rows[0]
            
            # ✅ CORREÇÃO: Verificação robusta do bcrypt
            senha_bytes = objUsuario.senha_hash.encode("utf-8")
            
            # Pega o hash do banco - pode ser string ou bytes
            hash_do_banco = usuarioDB["senha_hash"]
            
            # Converte para bytes se for string
            if isinstance(hash_do_banco, str):
                hash_bytes = hash_do_banco.encode("utf-8")
            else:
                hash_bytes = hash_do_banco
            
            print(f"🔐 Verificando senha para: {objUsuario.email}")
            
            # Verifica a senha
            if not bcrypt.checkpw(senha_bytes, hash_bytes):
                print("❌ Senha inválida")
                return None

            # Cria objeto usuário com dados do banco
            usuario = Usuario()
            usuario.id = usuarioDB["id"]
            usuario.nome = usuarioDB["nome"]
            usuario.email = usuarioDB["email"]
            usuario.senha_hash = usuarioDB["senha_hash"]

            print(f"✅ Login bem-sucedido para: {usuario.email}")
            return usuario
            
        except Exception as e:
            print(f"❌ Erro em UsuarioDAO.login(): {e}")
            print(f"🔍 Detalhes do erro: {str(e)}")
            raise