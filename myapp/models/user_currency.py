class UserCurrency:
    def __init__(self, uc_id: int, user_id: int, currency_id: int):
        self.__id = None
        self.__user_id = None
        self.__currency_id = None

        self.id = uc_id
        self.user_id = user_id
        self.currency_id = currency_id

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, value: int) -> None:
        if not isinstance(value, int) or value <= 0:
            raise ValueError("ID связи должен быть положительным целым числом")
        self.__id = value

    @property
    def user_id(self) -> int:
        return self.__user_id

    @user_id.setter
    def user_id(self, value: int) -> None:
        if not isinstance(value, int) or value <= 0:
            raise ValueError("user_id должен быть положительным целым числом")
        self.__user_id = value

    @property
    def currency_id(self) -> int:
        return self.__currency_id

    @currency_id.setter
    def currency_id(self, value: int) -> None:
        if not isinstance(value, int) or value <= 0:
            raise ValueError("currency_id должен быть положительным целым числом")
        self.__currency_id = value