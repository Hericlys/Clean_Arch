from entities.order import Order
from entities.item import Item


def new_order(client: str, items_data: list, repository):
    order = Order(client)

    for item_data in items_data:
        item = Item(item_data["name"], item_data["price"])
        order.add_item(item)

    repository.save(order)

    return order
