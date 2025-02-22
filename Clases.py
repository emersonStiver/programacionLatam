

#Ingreso se datos de nombre y costos de produto 

class Producto:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio
    
    def __str__(self):
        return(f"Ingrese el nombre {self.nombre} Precio del producto - $ {self.precio:.2f}")
    
 #Modificaciones dentro del carrito de compra
 
class carrito:
    
    def __init__(self):
        self.productos = []
    
    def agregar_producto(self, producto):
        self.productoappend(producto)
        
    def eliminarproducto(self, nombre_producto):
        self.nombre_producto = [p for p in self.productos if p.nombre != nombre_producto]
    
    #Se calcula el total menos el descuento si cumple la condición aplicada al descuento 
    def calculartotal(self):
        total = sum([producto.precio for producto in self.productos])
        descuento = self.aplicar_descuento(total)
        return total - descuento
    
    #Se aplica un 10% como porcentaje de descaunto sobre los proctos selecionados
    def aplicar_decuento(self, total):
        if len(self.productos) >= 3:
            return total * 0.10
        return 0  
    
    #Mostrar los productos en una lista con nombre y precio
    def lista_productos(self):
        return [(producto.nombre, producto.precio) for producto in self.productos]
        
    #Genera un tikect de compra con los productos y el total final incluyendo sigenera algun descuento
    
    def mostrar_ticket(self):
        ticket = "Ticket de Compra:\n"
        for producto in self.productos:
            ticket += f"- {producto.nombre}: ${producto.precio:.2f}\n"
        total = self.calcular_total()
        ticket += f"\nTotal a pagar (descuento incluido): ${total:.2f}"
        return ticket

    
        
    
        
    
      
 
 
    
    
    
    