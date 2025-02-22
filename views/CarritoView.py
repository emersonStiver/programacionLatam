import tkinter as tk
from tkinter import messagebox

class CarritoView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Carrito de Compras")
        self.geometry("500x300")

        tk.Label(self, text="Carrito de Compras", font=("Arial", 14)).pack(pady=10)

        # Aquí se mostraría la lista de productos en el carrito
        self.lista_productos = tk.Listbox(self)
        self.lista_productos.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Botón para finalizar la compra
        tk.Button(self, text="Finalizar Compra", command=self.finalizar_compra).pack(pady=5)

    def finalizar_compra(self):
        messagebox.showinfo("Compra Finalizada", "Gracias por tu compra")
        self.destroy()
