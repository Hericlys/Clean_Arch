from interface.repository import RepositoryOrder

class RepositoryMemory(RepositoryOrder):
    def __init__(self):
        self.orders = []
        
    def save(self, order):
        self.orders.append(order)
        print(f'✅ Pedido salvo na memória: {order.client} - R$ {order.calculate_total():.2f}')