# app/models.py

class Producto:
    def __init__(self, nombre, precio):
        self.__nombre = nombre  # Atributo privado
        self.__precio = precio

    @property
    def nombre(self):
        return self.__nombre

    @property
    def precio(self):
        return self.__precio

    def __str__(self):
        return f"{self.__nombre} - ${self.__precio:.2f}"


class Electronico(Producto):
    def __init__(self, nombre, precio, garantia_meses):
        super().__init__(nombre, precio)
        self.__garantia = garantia_meses

    @property
    def garantia(self):
        return self.__garantia

    def __str__(self):
        return f"{self.nombre} (Garantía: {self.garantia} meses) - ${self.precio:.2f}"


class Carrito:
    def __init__(self):
        self.__items = []  # Lista de tuplas (producto, cantidad)

    def agregar_producto(self, producto, cantidad):
        self.__items.append((producto, cantidad))

    def eliminar_producto(self, nombre_producto):
        self.__items = [(p, c) for (p, c) in self.__items if p.nombre != nombre_producto]

    def calcular_total(self):
        total = sum(p.precio * c for (p, c) in self.__items)
        descuento = self.aplicar_descuento(total)
        return total - descuento

    def aplicar_descuento(self, total):
        total_unidades = sum(c for (_, c) in self.__items)
        if total_unidades >= 3:
            return total * 0.10
        return 0

    def mostrar_ticket(self):
        ticket = "Ticket de Compra:\n"
        for p, c in self.__items:
            subtotal = p.precio * c
            ticket += f"- {p.nombre} x {c} = ${subtotal:.2f}\n"
        total = self.calcular_total()
        ticket += f"\nTotal a pagar (descuento incluido): ${total:.2f}"
        return ticket

    def get_items(self):
        return self.__items

    def limpiar(self):
        self.__items = []
