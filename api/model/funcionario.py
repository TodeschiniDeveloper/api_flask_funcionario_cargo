# -*- coding: utf-8 -*-
from api.model.cargo import Cargo

"""
Representa a entidade Funcionario do sistema.

Objetivo:
- Encapsular os dados de um funcionário.
- Garantir integridade dos atributos via getters e setters.
- Associar corretamente um funcionário a um Cargo.
"""
class Funcionario:
    def __init__(self):
        """
        Inicializa todos os atributos como atributos de instância.
        """
        # Atributos privados de instância
        self.__idFuncionario = None
        self.__cargo = None
        self.__nomeFuncionario = None
        self.__email = None
        self.__senha = None
        self.__recebeValeTransporte = None

    @property
    def idFuncionario(self):
        """
        Getter para idFuncionario
        :return: int - Identificador do funcionário
        """
        return self.__idFuncionario

    @idFuncionario.setter
    def idFuncionario(self, valor):
        """
        Define o ID do funcionário.

        🔹 Regra de domínio: garante que o ID seja sempre um número inteiro positivo.

        :param valor: int - Número inteiro positivo representando o ID do funcionário.
        :raises ValueError: se não for número inteiro positivo.

        Exemplo:
        >>> f = Funcionario()
        >>> f.idFuncionario = 10   # ✅ válido
        >>> f.idFuncionario = -5   # ❌ lança erro
        """
        try:
            parsed = int(valor)
        except (ValueError, TypeError):
            raise ValueError("idFuncionario deve ser um número inteiro.")

        if parsed <= 0:
            raise ValueError("idFuncionario deve ser um número inteiro positivo.")

        self.__idFuncionario = parsed

    @property
    def cargo(self):
        """
        Getter para cargo
        :return: Cargo - Objeto Cargo associado
        """
        return self.__cargo

    @cargo.setter
    def cargo(self, value):
        """
        Define o Cargo do funcionário.

        🔹 Regra de domínio: garante que sempre exista um Cargo válido associado.

        :param value: Cargo - Instância válida da classe Cargo.
        :raises ValueError: se não for instância de Cargo.

        Exemplo:
        >>> f = Funcionario()
        >>> f.cargo = Cargo()
        """
        if not isinstance(value, Cargo):
            raise ValueError("cargo deve ser uma instância válida de Cargo.")

        self.__cargo = value

    @property
    def nomeFuncionario(self):
        """
        Getter para nomeFuncionario
        :return: str - Nome do funcionário
        """
        return self.__nomeFuncionario

    @nomeFuncionario.setter
    def nomeFuncionario(self, value):
        """
        Define o nome do funcionário.

        🔹 Regra de domínio: deve ser string não vazia com pelo menos 3 caracteres.

        :param value: str - Nome do funcionário.
        :raises ValueError: se inválido.

        Exemplo:
        >>> f = Funcionario()
        >>> f.nomeFuncionario = "João Silva"  # ✅ válido
        """
        if not isinstance(value, str):
            raise ValueError("nomeFuncionario deve ser uma string.")

        nome = value.strip()

        if len(nome) < 3:
            raise ValueError("nomeFuncionario deve ter pelo menos 3 caracteres.")

        self.__nomeFuncionario = nome

    @property
    def email(self):
        """
        Getter para email
        :return: str - Email do funcionário
        """
        return self.__email

    @email.setter
    def email(self, value):
        """
        Define o email do funcionário.

        🔹 Regra de domínio: deve ser válido, não vazio e no formato correto.

        :param value: str - Email do funcionário.
        :raises ValueError: se inválido.
        """
        if not isinstance(value, str):
            raise ValueError("email deve ser uma string.")

        email_trimmed = value.strip()

        if email_trimmed == "":
            raise ValueError("email não pode ser vazio.")

        import re
        email_regex = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
        if not re.match(email_regex, email_trimmed):
            raise ValueError("email em formato inválido.")

        self.__email = email_trimmed

    @property
    def senha(self):
        """
        Getter para senha
        :return: str - Senha do funcionário
        """
        return self.__senha

    @senha.setter
    def senha(self, value):
        """
        Define a senha do funcionário.

        🔹 Regra de domínio: 
        - Mínimo 6 caracteres
        - Pelo menos 1 número
        - Pelo menos 1 letra maiúscula
        - Pelo menos 1 caractere especial

        :param value: str - Senha do funcionário.
        :raises ValueError: se inválida.
        """
        if not isinstance(value, str):
            raise ValueError("senha deve ser uma string.")

        senha_trimmed = value.strip()

        if senha_trimmed == "":
            raise ValueError("senha não pode ser vazia.")

        if len(senha_trimmed) < 6:
            raise ValueError("senha deve ter pelo menos 6 caracteres.")

        if not any(c.isupper() for c in senha_trimmed):
            raise ValueError("senha deve conter pelo menos uma letra maiúscula.")

        if not any(c.isdigit() for c in senha_trimmed):
            raise ValueError("senha deve conter pelo menos um número.")

        if not any(c in "!@#$%^&*(),.?\":{}|<>" for c in senha_trimmed):
            raise ValueError("senha deve conter pelo menos um caractere especial.")

        self.__senha = senha_trimmed

    @property
    def recebeValeTransporte(self):
        """
        Getter para recebeValeTransporte
        :return: int (0 ou 1)
        """
        return self.__recebeValeTransporte

    @recebeValeTransporte.setter
    def recebeValeTransporte(self, value):
        """
        Define se o funcionário recebe vale transporte.

        🔹 Regra de domínio: garante que o valor seja sempre 0 (não) ou 1 (sim).

        :param value: int - 0 ou 1
        :raises ValueError: se não for 0 ou 1.
        """
        if value not in (0, 1):
            raise ValueError("recebeValeTransporte deve ser 0 ou 1.")

        self.__recebeValeTransporte = value
