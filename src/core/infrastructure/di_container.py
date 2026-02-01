from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Type


class IDIContainer(ABC):
    @abstractmethod
    def register(
        self,
        interface: Type,
        implementation: Callable[..., Any],
        singleton: bool = False,
    ) -> None:
        pass

    @abstractmethod
    def resolve(self, interface: Type) -> Any:
        pass

    @abstractmethod
    def register_instance(self, interface: Type, instance: Any) -> None:
        pass


class SimpleDIContainer(IDIContainer):
    def __init__(self):
        self._services: Dict[Type, Callable[..., Any]] = {}
        self._singletons: Dict[Type, Any] = {}
        self._is_singleton: Dict[Type, bool] = {}

    def register(
        self,
        interface: Type,
        implementation: Callable[..., Any],
        singleton: bool = False,
    ) -> None:
        self._services[interface] = implementation
        self._is_singleton[interface] = singleton

    def register_instance(self, interface: Type, instance: Any) -> None:
        self._singletons[interface] = instance
        self._is_singleton[interface] = True

    def resolve(self, interface: Type) -> Any:
        if interface in self._singletons:
            return self._singletons[interface]

        if interface not in self._services:
            raise ValueError(f"Service {interface} not registered")

        factory = self._services[interface]
        instance = factory(self)

        if self._is_singleton.get(interface, False):
            self._singletons[interface] = instance

        return instance
