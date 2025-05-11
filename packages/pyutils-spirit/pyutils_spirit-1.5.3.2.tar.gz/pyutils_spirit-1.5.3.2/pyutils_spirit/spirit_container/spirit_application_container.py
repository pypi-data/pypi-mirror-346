from typing import Any

from pyutils_spirit.util.assemble import Assemble, HashAssemble

from pyutils_spirit.exception.exception import ArgumentException


class SpiritApplicationContainer:
    __instance: object = None

    __application_container: Assemble[str, Any] = None

    def __init__(self):
        if self.__application_container is None:
            self.__application_container = HashAssemble()

    def __new__(cls) -> object:
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def set_resource(self, signature: str, resource: Any):
        if signature in self.__application_container:
            raise ArgumentException(f"spirit_application_container: '{signature}' "
                                    f"Different resources cannot have the same signature")
        self.__application_container[signature] = resource

    def get_resource(self, signature: str) -> Any:
        return self.__application_container[signature]

    def remove_resource(self, signature: str) -> Any:
        return self.__application_container.remove(key=signature)

    def get_capacity(self):
        return len(self.__application_container)

    def __iter__(self):
        return iter(self.__application_container)

    def __next__(self):
        return next(self.__application_container)
