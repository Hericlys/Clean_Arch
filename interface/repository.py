from abc import ABC, abstractmethod
from entities.order import Order


class RepositoryOrder(ABC):
    @abstractmethod
    def save(self, order: Order):
        pass


