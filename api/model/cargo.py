# -*- coding: utf-8 -*-
"""
Representa a entidade Cargo do sistema.

Objetivo:
- Encapsular os dados de um cargo.
- Garantir integridade dos atributos via getters e setters.
"""
class Cargo:
    def __init__(self):
        """
        Inicializa todos os atributos como atributos de instância.
        """
        self.__idCargo = None
        self.__nomeCargo = None

    @property
    def idCargo(self):
        """
        Getter para idCargo
        :return: int - Identificador único do cargo
        """
        return self.__idCargo

    @idCargo.setter
    def idCargo(self, value):
        """
        Define o ID do cargo.

        🔹 Regra de domínio: garante que o ID seja sempre um número inteiro positivo.

        :param value: int - Número inteiro positivo representando o ID do cargo.
        :raises ValueError: Lança erro se o valor não for número, não for inteiro ou for menor/igual a zero.

        Exemplo:
        >>> cargo = Cargo()
        >>> cargo.idCargo = 1   # ✅ válido
        >>> cargo.idCargo = -5  # ❌ lança erro
        >>> cargo.idCargo = 0   # ❌ lança erro
        >>> cargo.idCargo = 3.14  # ❌ lança erro
        >>> cargo.idCargo = None  # ❌ lança erro
        """
        try:
            parsed = int(value)
        except (ValueError, TypeError):
            raise ValueError("idCargo deve ser um número inteiro.")

        if parsed <= 0:
            raise ValueError("idCargo deve ser maior que zero.")

        self.__idCargo = parsed

    @property
    def nomeCargo(self):
        """
        Getter para nomeCargo
        :return: str - Nome do cargo
        """
        return self.__nomeCargo

    @nomeCargo.setter
    def nomeCargo(self, value):
        """
        Define o nome do cargo.

        🔹 Regra de domínio: garante que o nome seja sempre uma string não vazia
        e com pelo menos 3 caracteres.

        :param value: str - Nome do cargo.
        :raises ValueError: Lança erro se o valor não for string, estiver vazio, tiver menos de 3 caracteres ou for None.

        Exemplo:
        >>> cargo = Cargo()
        >>> cargo.nomeCargo = "Gerente"   # ✅ válido
        >>> cargo.nomeCargo = "AB"        # ❌ lança erro
        >>> cargo.nomeCargo = ""          # ❌ lança erro
        >>> cargo.nomeCargo = None        # ❌ lança erro
        """
        if not isinstance(value, str):
            raise ValueError("nomeCargo deve ser uma string.")

        nome = value.strip()
        if len(nome) < 3:
            raise ValueError("nomeCargo deve ter pelo menos 3 caracteres.")

        self.__nomeCargo = nome
