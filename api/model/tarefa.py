class Tarefa:
    def __init__(self):
        """
        Inicializa todos os atributos como atributos de instância.
        """
        self.__id = None
        self.__titulo = None
        self.__concluida = False
        self.__data_limite = None
        self.__projeto_id = None

    @property
    def id(self):
        """
        Getter para id
        :return: int - Identificador único da tarefa
        """
        return self.__id

    @id.setter
    def id(self, value):
        """
        Define o ID da tarefa.

        🔹 Regra de domínio: garante que o ID seja sempre um número inteiro positivo.

        :param value: int - Número inteiro positivo representando o ID da tarefa.
        :raises ValueError: Lança erro se o valor não for número, não for inteiro ou for menor/igual a zero.

        Exemplo:
        >>> tarefa = Tarefa()
        >>> tarefa.id = 1   # ✅ válido
        >>> tarefa.id = -5  # ❌ lança erro
        >>> tarefa.id = 0   # ❌ lança erro
        >>> tarefa.id = 3.14  # ❌ lança erro
        >>> tarefa.id = None  # ❌ lança erro
        """
        try:
            parsed = int(value)
        except (ValueError, TypeError):
            raise ValueError("id deve ser um número inteiro.")

        if parsed <= 0:
            raise ValueError("id deve ser maior que zero.")

        self.__id = parsed

    @property
    def titulo(self):
        """
        Getter para titulo
        :return: str - Título da tarefa
        """
        return self.__titulo

    @titulo.setter
    def titulo(self, value):
        """
        Define o título da tarefa.

        🔹 Regra de domínio: garante que o título seja sempre uma string não vazia
        e com pelo menos 3 caracteres.

        :param value: str - Título da tarefa.
        :raises ValueError: Lança erro se o valor não for string, estiver vazio, tiver menos de 3 caracteres ou for None.

        Exemplo:
        >>> tarefa = Tarefa()
        >>> tarefa.titulo = "Definir endpoints"   # ✅ válido
        >>> tarefa.titulo = "AB"                  # ❌ lança erro
        >>> tarefa.titulo = ""                    # ❌ lança erro
        >>> tarefa.titulo = None                  # ❌ lança erro
        """
        if not isinstance(value, str):
            raise ValueError("titulo deve ser uma string.")

        titulo = value.strip()
        if len(titulo) < 3:
            raise ValueError("titulo deve ter pelo menos 3 caracteres.")

        self.__titulo = titulo

    @property
    def concluida(self):
        """
        Getter para concluida
        :return: bool - Status de conclusão da tarefa
        """
        return self.__concluida

    @concluida.setter
    def concluida(self, value):
        """
        Define o status de conclusão da tarefa.

        🔹 Regra de domínio: garante que o valor seja booleano.

        :param value: bool - Status de conclusão da tarefa.
        :raises ValueError: Lança erro se o valor não for booleano.

        Exemplo:
        >>> tarefa = Tarefa()
        >>> tarefa.concluida = True    # ✅ válido
        >>> tarefa.concluida = False   # ✅ válido
        >>> tarefa.concluida = 1       # ❌ lança erro
        >>> tarefa.concluida = "Sim"   # ❌ lança erro
        >>> tarefa.concluida = None    # ❌ lança erro
        """
        if not isinstance(value, bool):
            raise ValueError("concluida deve ser um valor booleano.")

        self.__concluida = value

    @property
    def data_limite(self):
        """
        Getter para data_limite
        :return: date - Data limite da tarefa
        """
        return self.__data_limite

    @data_limite.setter
    def data_limite(self, value):
        """
        Define a data limite da tarefa.

        🔹 Regra de domínio: garante que a data seja um objeto date.

        :param value: date - Data limite da tarefa.
        :raises ValueError: Lança erro se o valor não for date.

        Exemplo:
        >>> tarefa = Tarefa()
        >>> from datetime import date
        >>> tarefa.data_limite = date(2025, 11, 5)   # ✅ válido
        >>> tarefa.data_limite = "2025-11-05"        # ❌ lança erro
        >>> tarefa.data_limite = None                # ✅ válido (None é permitido)
        """
        if value is not None:
            from datetime import date
            if not isinstance(value, date):
                raise ValueError("data_limite deve ser um objeto date ou None.")

        self.__data_limite = value

    @property
    def projeto_id(self):
        """
        Getter para projeto_id
        :return: int - ID do projeto ao qual a tarefa pertence
        """
        return self.__projeto_id

    @projeto_id.setter
    def projeto_id(self, value):
        """
        Define o ID do projeto ao qual a tarefa pertence.

        🔹 Regra de domínio: garante que o ID do projeto seja sempre um número inteiro positivo.

        :param value: int - Número inteiro positivo representando o ID do projeto.
        :raises ValueError: Lança erro se o valor não for número, não for inteiro ou for menor/igual a zero.

        Exemplo:
        >>> tarefa = Tarefa()
        >>> tarefa.projeto_id = 1   # ✅ válido
        >>> tarefa.projeto_id = -5  # ❌ lança erro
        >>> tarefa.projeto_id = 0   # ❌ lança erro
        >>> tarefa.projeto_id = 3.14  # ❌ lança erro
        >>> tarefa.projeto_id = None  # ❌ lança erro
        """
        try:
            parsed = int(value)
        except (ValueError, TypeError):
            raise ValueError("projeto_id deve ser um número inteiro.")

        if parsed <= 0:
            raise ValueError("projeto_id deve ser maior que zero.")

        self.__projeto_id = parsed