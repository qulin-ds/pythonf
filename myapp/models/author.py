class Author:
    def __init__(self, name: str, group: str = "P3122"):
        self.__name = None
        self.__group = None
        self.name = name
        self.group = group

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str) or len(value.strip()) < 1:
            raise ValueError("Имя автора не может быть пустым")
        self.__name = value.strip()

    @property
    def group(self) -> str:
        return self.__group

    @group.setter
    def group(self, value: str) -> None:
        if not isinstance(value, str) or len(value.strip()) < 1:
            raise ValueError("Группа не может быть пустой")
        self.__group = value.strip()