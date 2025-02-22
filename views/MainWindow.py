import tkinter as tk
from views.carrito_view import CarritoView

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mercado Inteligente")
        self.geometry("600x400")

        tk.Label(self, text="Bienvenido al Mercado Inteligente", font=("Arial", 16)).pack(pady=10)

        tk.Button(self, text="Agregar Producto", command=self.agregar_producto).pack(pady=5)
        tk.Button(self, text="Ver Carrito", command=self.ver_carrito).pack(pady=5)
        tk.Button(self, text="Salir", command=self.quit).pack(pady=5)

    def agregar_producto(self):
        # Aquí iría la lógica para abrir el formulario de productos
        print("Abrir formulario de productos")

    def ver_carrito(self):
        carrito_win = CarritoView(self)
        carrito_win.mainloop()

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
