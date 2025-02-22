import tkinter as tk

class TicketView(tk.Toplevel):
    def __init__(self, parent, carrito):
        super().__init__(parent)
        self.title("Ticket de Compra")
        self.geometry("400x300")

        tk.Label(self, text="Ticket de Compra", font=("Arial", 14)).pack(pady=10)

        # Mostrar resumen del pedido
        for producto in carrito:
            tk.Label(self, text=f"{producto['nombre']} - ${producto['precio']} x {producto['cantidad']}").pack()

        total = sum(p["precio"] * p["cantidad"] for p in carrito)
        tk.Label(self, text=f"Total a Pagar: ${total:.2f}", font=("Arial", 12, "bold")).pack(pady=10)

        tk.Button(self, text="Cerrar", command=self.destroy).pack(pady=5)
