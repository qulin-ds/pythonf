class Currency:
    def __init__(self, num_code: str, char_code: str, name: str, value: float, nominal: int):
        self.__num_code = num_code
        self.__char_code = None
        self.__name = None
        self.__value = None
        self.__nominal = None

        self.char_code = char_code
        self.name = name
        self.value = value
        self.nominal = nominal

    @property
    def num_code(self) -> str:
        return self.__num_code

    @property
    def char_code(self) -> str:
        return self.__char_code

    @char_code.setter
    def char_code(self, val: str) -> None:
        if not isinstance(val, str) or len(val) != 3:
            raise ValueError("Код валюты должен состоять из 3 символов")
        self.__char_code = val.upper()

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str) or len(value.strip()) < 1:
            raise ValueError("Название валюты не может быть пустым")
        self.__name = value.strip()

    @property
    def value(self) -> float:
        return self.__value

    @value.setter
    def value(self, val: float) -> None:
        if not isinstance(val, (int, float)) or val < 0:
            raise ValueError("Курс валюты не может быть отрицательным")
        self.__value = float(val)

    @property
    def nominal(self) -> int:
        return self.__nominal

    @nominal.setter
    def nominal(self, val: int) -> None:
        if not isinstance(val, int) or val <= 0:
            raise ValueError("Номинал должен быть положительным целым числом")
        self.__nominal = val