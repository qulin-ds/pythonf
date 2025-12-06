class User:
    def __init__(self, user_id: int, name: str):
        self.__id = None
        self.__name = None

        self.id = user_id
        self.name = name

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, value: int) -> None:
        if not isinstance(value, int) or value <= 0:
            raise ValueError("ID пользователя должен быть положительным целым числом")
        self.__id = value

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str) or len(value.strip()) < 1:
            raise ValueError("Имя пользователя не может быть пустым")
        self.__name = value.strip()