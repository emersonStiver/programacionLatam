import tkinter as tk
from tkinter import messagebox, simpledialog
from app.config import BG_COLOR, FG_COLOR, BTN_BG, BTN_FG, ENTRY_BG, ENTRY_FG

class BaseView:
    def __init__(self, root, change_view_callback, controller):
        self.root = root
        self.change_view_callback = change_view_callback
        self.controller = controller
        self.frame = tk.Frame(self.root, padx=20, pady=20, bg=BG_COLOR)

    def show(self):
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        self.frame.pack_forget()


class AddProductView(BaseView):
    def __init__(self, root, change_view_callback, controller):
        super().__init__(root, change_view_callback, controller)
        tk.Label(self.frame, text="Agregar Producto", font=("Arial", 16), bg=BG_COLOR, fg=FG_COLOR).pack(pady=10)
        tk.Label(self.frame, text="Nombre del Producto", bg=BG_COLOR, fg=FG_COLOR).pack()
        self.name_entry = tk.Entry(self.frame, bg=ENTRY_BG, fg=ENTRY_FG, relief="solid", bd=1)
        self.name_entry.pack(pady=5)
        tk.Label(self.frame, text="Precio del Producto", bg=BG_COLOR, fg=FG_COLOR).pack()
        self.price_entry = tk.Entry(self.frame, bg=ENTRY_BG, fg=ENTRY_FG, relief="solid", bd=1)
        self.price_entry.pack(pady=5)
        tk.Button(self.frame, text="Agregar", command=self.add_product, bg=BTN_BG, fg=BTN_FG).pack(pady=10)
        tk.Button(self.frame, text="Volver", command=lambda: self.change_view_callback("all_products"), bg="red", fg="white").pack()

    def add_product(self):
        name = self.name_entry.get()
        price = self.price_entry.get()
        if not name or not price:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        try:
            price = float(price)
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número válido.")
            return
        self.controller.add_product(name, price)
        messagebox.showinfo("Éxito", "Producto agregado correctamente.")
        self.change_view_callback("all_products")


class AllProductsView(BaseView):
    def __init__(self, root, change_view_callback, controller):
        super().__init__(root, change_view_callback, controller)
        tk.Label(self.frame, text="Lista de Productos Disponibles", font=("Arial", 16), bg=BG_COLOR, fg=FG_COLOR).pack(pady=10)
        self.products_frame = tk.Frame(self.frame, bg=BG_COLOR)
        self.products_frame.pack(fill="both", expand=True)
        tk.Button(self.frame, text="Ver Carrito", command=lambda: self.change_view_callback("cart"), bg="blue", fg="white").pack(side="top", anchor="ne", pady=5)
        tk.Button(self.frame, text="Agregar Producto", command=lambda: self.change_view_callback("add_product"), bg="purple", fg="white").pack(side="top", anchor="ne", pady=5)

    def update_product_list(self):
        for widget in self.products_frame.winfo_children():
            widget.destroy()
        for producto in self.controller.get_products():
            prod_frame = tk.Frame(self.products_frame, bg=BG_COLOR)
            prod_frame.pack(pady=2, fill="x")
            tk.Label(prod_frame, text=str(producto), width=40, anchor="w", bg=BG_COLOR, fg=FG_COLOR).pack(side="left")
            tk.Button(prod_frame, text="Agregar", command=lambda p=producto: self.add_to_cart(p), bg="gray", fg="white").pack(side="right")

    def add_to_cart(self, producto):
        cantidad = simpledialog.askinteger("Cantidad", f"Ingrese cantidad para {producto.nombre}:", minvalue=1)
        if cantidad:
            self.controller.add_to_cart(producto, cantidad)
            messagebox.showinfo("Carrito", f"{producto.nombre} agregado al carrito.")

    def show(self):
        self.update_product_list()
        super().show()


class CartView(BaseView):
    def __init__(self, root, change_view_callback, controller):
        super().__init__(root, change_view_callback, controller)
        tk.Label(self.frame, text="Carrito de Compras", font=("Arial", 16), bg=BG_COLOR, fg=FG_COLOR).pack(pady=10)
        self.cart_frame = tk.Frame(self.frame, bg=BG_COLOR)
        self.cart_frame.pack(pady=10, fill="both", expand=True)
        tk.Button(self.frame, text="Comprar", command=self.go_to_summary, bg=BTN_BG, fg=BTN_FG).pack(pady=5)
        tk.Button(self.frame, text="Volver", command=lambda: self.change_view_callback("all_products"), bg="red", fg="white").pack(pady=5)
        tk.Button(self.frame, text="Mostrar Ticket", command=self.show_ticket, bg="orange", fg="white").pack(pady=5)

    def update_cart(self):
        for widget in self.cart_frame.winfo_children():
            widget.destroy()
        items = self.controller.cart.get_items()
        if not items:
            tk.Label(self.cart_frame, text="El carrito está vacío.", bg=BG_COLOR, fg=FG_COLOR).pack()
        else:
            for index, (producto, cantidad) in enumerate(items):
                item_frame = tk.Frame(self.cart_frame, bg=BG_COLOR)
                item_frame.pack(fill="x", pady=2)
                subtotal = producto.precio * cantidad
                tk.Label(
                    item_frame,
                    text=f"{producto.nombre} x {cantidad} - ${producto.precio:.2f} c/u (Subtotal: ${subtotal:.2f})",
                    anchor="w", bg=BG_COLOR, fg=FG_COLOR
                ).pack(side="left")
                tk.Button(item_frame, text="Quitar", command=lambda i=index: self.remove_item(i), bg="gray", fg="white").pack(side="right")

    def remove_item(self, index):
        items = self.controller.cart.get_items()
        if index < len(items):
            producto_a_eliminar = items[index][0].nombre
            self.controller.cart.eliminar_producto(producto_a_eliminar)
            self.update_cart()

    def go_to_summary(self):
        if not self.controller.cart.get_items():
            messagebox.showerror("Error", "El carrito está vacío.")
        else:
            self.change_view_callback("summary")

    def show_ticket(self):
        ticket = self.controller.cart.mostrar_ticket()
        messagebox.showinfo("Ticket de Compra", ticket)

    def show(self):
        self.update_cart()
        super().show()


class SummaryView(BaseView):
    def __init__(self, root, change_view_callback, controller):
        super().__init__(root, change_view_callback, controller)
        tk.Label(self.frame, text="Resumen de Compra", font=("Arial", 16), bg=BG_COLOR, fg=FG_COLOR).pack(pady=10)
        self.summary_frame = tk.Frame(self.frame, bg=BG_COLOR)
        self.summary_frame.pack(pady=10, fill="both", expand=True)
        self.total_label = tk.Label(self.frame, text="", bg=BG_COLOR, fg=FG_COLOR)
        self.total_label.pack(pady=5)
        tk.Button(self.frame, text="Confirmar Compra", command=self.confirm_purchase, bg=BTN_BG, fg=BTN_FG).pack(pady=5)
        tk.Button(self.frame, text="Volver", command=lambda: self.change_view_callback("cart"), bg="red", fg="white").pack(pady=5)

    def update_summary(self):
        for widget in self.summary_frame.winfo_children():
            widget.destroy()
        items = self.controller.cart.get_items()
        total = 0
        for producto, cantidad in items:
            subtotal = producto.precio * cantidad
            total += subtotal
            tk.Label(
                self.summary_frame,
                text=f"{producto.nombre} x {cantidad} - ${producto.precio:.2f} c/u (Subtotal: ${subtotal:.2f})",
                anchor="w", bg=BG_COLOR, fg=FG_COLOR
            ).pack(fill="x")
        descuento = self.controller.cart.aplicar_descuento(total)
        tk.Label(self.summary_frame, text=f"Descuento aplicado: ${descuento:.2f}", fg="blue", bg=BG_COLOR).pack(fill="x", pady=5)
        total_final = self.controller.cart.calcular_total()
        self.total_label.config(text=f"Total a pagar (con descuento): ${total_final:.2f}")

    def confirm_purchase(self):
        if not self.controller.cart.get_items():
            messagebox.showerror("Error", "El carrito está vacío.")
        else:
            messagebox.showinfo("Compra", "Compra realizada exitosamente.\n\n" + self.controller.cart.mostrar_ticket())
            self.controller.cart.limpiar()
            self.change_view_callback("all_products")

    def show(self):
        self.update_summary()
        super().show()


class MercadoApp:
    def __init__(self, root, controller):
        self.root = root
        self.root.title("Mercado Inteligente")
        self.root.configure(bg=BG_COLOR)
        self.controller = controller
        self.views = {
            "all_products": AllProductsView(root, self.change_view, self.controller),
            "add_product": AddProductView(root, self.change_view, self.controller),
            "cart": CartView(root, self.change_view, self.controller),
            "summary": SummaryView(root, self.change_view, self.controller)
        }
        self.current_view = None
        self.change_view("all_products")

    def change_view(self, view_name):
        if self.current_view:
            self.current_view.hide()
        self.current_view = self.views[view_name]
        self.current_view.show()
