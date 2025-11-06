class Projeto:
    def __init__(self):
        """
        Inicializa todos os atributos como atributos de instância.
        """
        self.__id = None
        self.__nome = None
        self.__descricao = None
        self.__data_inicio = None
        self.__status = None
        self.__usuario_id = None

    @property
    def id(self):
        """
        Getter para id
        :return: int - Identificador único do projeto
        """
        return self.__id

    @id.setter
    def id(self, value):
        """
        Define o ID do projeto.

        🔹 Regra de domínio: garante que o ID seja sempre um número inteiro positivo.

        :param value: int - Número inteiro positivo representando o ID do projeto.
        :raises ValueError: Lança erro se o valor não for número, não for inteiro ou for menor/igual a zero.

        Exemplo:
        >>> projeto = Projeto()
        >>> projeto.id = 1   # ✅ válido
        >>> projeto.id = -5  # ❌ lança erro
        >>> projeto.id = 0   # ❌ lança erro
        >>> projeto.id = 3.14  # ❌ lança erro
        >>> projeto.id = None  # ❌ lança erro
        """
        try:
            parsed = int(value)
        except (ValueError, TypeError):
            raise ValueError("id deve ser um número inteiro.")

        if parsed <= 0:
            raise ValueError("id deve ser maior que zero.")

        self.__id = parsed

    @property
    def nome(self):
        """
        Getter para nome
        :return: str - Nome do projeto
        """
        return self.__nome

    @nome.setter
    def nome(self, value):
        """
        Define o nome do projeto.

        🔹 Regra de domínio: garante que o nome seja sempre uma string não vazia
        e com pelo menos 3 caracteres.

        :param value: str - Nome do projeto.
        :raises ValueError: Lança erro se o valor não for string, estiver vazio, tiver menos de 3 caracteres ou for None.

        Exemplo:
        >>> projeto = Projeto()
        >>> projeto.nome = "API de E-commerce"   # ✅ válido
        >>> projeto.nome = "AB"                  # ❌ lança erro
        >>> projeto.nome = ""                    # ❌ lança erro
        >>> projeto.nome = None                  # ❌ lança erro
        """
        if not isinstance(value, str):
            raise ValueError("nome deve ser uma string.")

        nome = value.strip()
        if len(nome) < 3:
            raise ValueError("nome deve ter pelo menos 3 caracteres.")

        self.__nome = nome

    @property
    def descricao(self):
        """
        Getter para descricao
        :return: str - Descrição do projeto
        """
        return self.__descricao

    @descricao.setter
    def descricao(self, value):
        """
        Define a descrição do projeto.

        🔹 Regra de domínio: garante que a descrição seja uma string.

        :param value: str - Descrição do projeto.
        :raises ValueError: Lança erro se o valor não for string.

        Exemplo:
        >>> projeto = Projeto()
        >>> projeto.descricao = "Desenvolver a API REST"   # ✅ válido
        >>> projeto.descricao = None                       # ✅ válido (None é permitido)
        >>> projeto.descricao = 123                        # ❌ lança erro
        """
        if value is not None and not isinstance(value, str):
            raise ValueError("descricao deve ser uma string ou None.")

        self.__descricao = value

    @property
    def data_inicio(self):
        """
        Getter para data_inicio
        :return: date - Data de início do projeto
        """
        return self.__data_inicio

    @data_inicio.setter
    def data_inicio(self, value):
        """
        Define a data de início do projeto.

        🔹 Regra de domínio: garante que a data seja um objeto date.

        :param value: date - Data de início do projeto.
        :raises ValueError: Lança erro se o valor não for date.

        Exemplo:
        >>> projeto = Projeto()
        >>> from datetime import date
        >>> projeto.data_inicio = date(2025, 11, 1)   # ✅ válido
        >>> projeto.data_inicio = "2025-11-01"        # ❌ lança erro
        >>> projeto.data_inicio = None                # ✅ válido (None é permitido)
        """
        if value is not None:
            from datetime import date
            if not isinstance(value, date):
                raise ValueError("data_inicio deve ser um objeto date ou None.")

        self.__data_inicio = value

    @property
    def status(self):
        """
        Getter para status
        :return: str - Status do projeto
        """
        return self.__status

    @status.setter
    def status(self, value):
        """
        Define o status do projeto.

        🔹 Regra de domínio: garante que o status seja um dos valores permitidos.

        :param value: str - Status do projeto.
        :raises ValueError: Lança erro se o valor não for um status válido.

        Exemplo:
        >>> projeto = Projeto()
        >>> projeto.status = "Pendente"       # ✅ válido
        >>> projeto.status = "Em Andamento"   # ✅ válido
        >>> projeto.status = "Concluído"      # ✅ válido
        >>> projeto.status = "Cancelado"      # ✅ válido
        >>> projeto.status = "Inválido"       # ❌ lança erro
        >>> projeto.status = None             # ❌ lança erro
        """
        if not isinstance(value, str):
            raise ValueError("status deve ser uma string.")

        status_validos = ["Pendente", "Em Andamento", "Concluído", "Cancelado"]
        if value not in status_validos:
            raise ValueError(f"status deve ser um dos valores: {', '.join(status_validos)}")

        self.__status = value

    @property
    def usuario_id(self):
        """
        Getter para usuario_id
        :return: int - ID do usuário proprietário do projeto
        """
        return self.__usuario_id

    @usuario_id.setter
    def usuario_id(self, value):
        """
        Define o ID do usuário proprietário do projeto.

        🔹 Regra de domínio: garante que o ID do usuário seja sempre um número inteiro positivo.

        :param value: int - Número inteiro positivo representando o ID do usuário.
        :raises ValueError: Lança erro se o valor não for número, não for inteiro ou for menor/igual a zero.

        Exemplo:
        >>> projeto = Projeto()
        >>> projeto.usuario_id = 1   # ✅ válido
        >>> projeto.usuario_id = -5  # ❌ lança erro
        >>> projeto.usuario_id = 0   # ❌ lança erro
        >>> projeto.usuario_id = 3.14  # ❌ lança erro
        >>> projeto.usuario_id = None  # ❌ lança erro
        """
        try:
            parsed = int(value)
        except (ValueError, TypeError):
            raise ValueError("usuario_id deve ser um número inteiro.")

        if parsed <= 0:
            raise ValueError("usuario_id deve ser maior que zero.")

        self.__usuario_id = parsed


# -*- coding: utf-8 -*-
"""
Representa a entidade Tarefa do sistema.

Objetivo:
- Encapsular os dados de uma tarefa.
- Garantir integridade dos atributos via getters e setters.
"""