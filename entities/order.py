from entities.item import Item


class Order:
    def __init__(self, client: str):
        self.client = client
        self.items:list = []

    def add_item(self, item: Item):
        self.items.append(item)

    def calculate_total(self) -> float:
        return sum(item.price for item in self.items)
