from app.models import Producto, Electronico, Carrito

class Controller:
    def __init__(self):
        self.__productos = [
            Producto("Laptop", 1000.0),
            Electronico("Teléfono", 500.0, garantia_meses=24),
            Producto("Tablet", 300.0)
        ]
        self.cart = Carrito()

    def get_products(self):
        return self.__productos

    def add_product(self, name, price):
        self.__productos.append(Producto(name, price))

    def add_to_cart(self, producto, cantidad):
        self.cart.agregar_producto(producto, cantidad)
