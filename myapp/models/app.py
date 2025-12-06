from .author import Author


class App:
    def __init__(self, name: str, version: str, author: Author):
        self.__name = None
        self.__version = None
        self.__author = None

        self.name = name
        self.version = version
        self.author = author

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str) or len(value.strip()) < 1:
            raise ValueError("Название приложения не может быть пустым")
        self.__name = value.strip()

    @property
    def version(self) -> str:
        return self.__version

    @version.setter
    def version(self, value: str) -> None:
        if not isinstance(value, str) or len(value.strip()) < 1:
            raise ValueError("Версия приложения не может быть пустой")
        self.__version = value.strip()

    @property
    def author(self) -> Author:
        return self.__author

    @author.setter
    def author(self, value: Author) -> None:
        if not isinstance(value, Author):
            raise TypeError("author должен быть экземпляром Author")
        self.__author = value