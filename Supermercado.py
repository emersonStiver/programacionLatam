import tkinter as tk
from tkinter import messagebox

# Clase base para las vistas
class BaseView:
    def __init__(self, root, change_view_callback, controller):
        self.root = root
        self.change_view_callback = change_view_callback
        self.controller = controller
        self.frame = tk.Frame(self.root, padx=20, pady=20)

    def show(self):
        self.frame.pack()

    def hide(self):
        self.frame.pack_forget()

# Vista para el login
class LoginView(BaseView):
    def __init__(self, root, change_view_callback, controller):
        super().__init__(root, change_view_callback, controller)
        tk.Label(self.frame, text="Iniciar Sesión", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.frame, text="Nombre de Usuario").pack()
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.pack(pady=5)
        tk.Button(self.frame, text="Ingresar", command=self.login, bg="blue", fg="white").pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        if self.controller.authenticate_user(username):
            messagebox.showinfo("Bienvenido", f"Bienvenido, {username}")
            self.change_view_callback("all_products")
        else:
            messagebox.showerror("Error", "Usuario no válido.")

# Vista para agregar nuevos productos (solo admin)
class AddProductView(BaseView):
    def __init__(self, root, change_view_callback, controller):
        super().__init__(root, change_view_callback, controller)
        tk.Label(self.frame, text="Agregar Producto", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.frame, text="Nombre del Producto").pack()
        self.name_entry = tk.Entry(self.frame)
        self.name_entry.pack(pady=5)
        tk.Label(self.frame, text="Precio del Producto").pack()
        self.price_entry = tk.Entry(self.frame)
        self.price_entry.pack(pady=5)
        tk.Button(self.frame, text="Agregar", command=self.add_product, bg="green", fg="white").pack(pady=10)
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

# Vista para mostrar todos los productos
class AllProductsView(BaseView):
    def __init__(self, root, change_view_callback, controller):
        super().__init__(root, change_view_callback, controller)
        tk.Label(self.frame, text="Lista de Productos Disponibles", font=("Arial", 16)).pack(pady=10)
        self.products_frame = tk.Frame(self.frame)
        self.products_frame.pack()

        # Se creará o eliminará según el usuario admin
        self.admin_button = None

        # Botones fijos en la vista
        tk.Button(self.frame, text="Ver Carrito", command=lambda: self.change_view_callback("cart"), bg="blue", fg="white").pack(side="top", anchor="ne", pady=5)
        tk.Button(self.frame, text="Cerrar Sesión", command=self.logout, bg="red", fg="white").pack(side="top", anchor="ne", pady=5)

    def update_product_list(self):
        for widget in self.products_frame.winfo_children():
            widget.destroy()

        for product in self.controller.get_products():
            frame = tk.Frame(self.products_frame)
            frame.pack(pady=2, fill='x')
            tk.Label(frame, text=f"{product['name']} - ${product['price']}", width=20).pack(side="left")
            tk.Button(frame, text="Agregar", command=lambda p=product: self.add_to_cart(p), bg="gray", fg="white").pack(side="right")

    def add_to_cart(self, product):
        self.controller.add_to_cart(product)
        messagebox.showinfo("Carrito", f"{product['name']} agregado al carrito")

    def logout(self):
        self.controller.logout_user()
        self.change_view_callback("login")

    def show(self):
        self.update_product_list()
        # Mostrar botón de "Agregar Producto" solo si el usuario es admin
        if self.controller.user == "admin":
            if self.admin_button is None:
                self.admin_button = tk.Button(self.frame, text="Agregar Producto", command=lambda: self.change_view_callback("add_product"),
                                              bg="purple", fg="white")
                self.admin_button.pack(pady=5)
        else:
            if self.admin_button is not None:
                self.admin_button.destroy()
                self.admin_button = None
        super().show()

# Vista para el carrito de compras
class CartView(BaseView):
    def __init__(self, root, change_view_callback, controller):
        super().__init__(root, change_view_callback, controller)
        tk.Label(self.frame, text="Carrito de Compras", font=("Arial", 16)).pack(pady=10)
        self.cart_frame = tk.Frame(self.frame)
        self.cart_frame.pack(pady=10)
        tk.Button(self.frame, text="Comprar", command=self.go_to_summary, bg="green", fg="white").pack(pady=5)
        tk.Button(self.frame, text="Volver", command=lambda: self.change_view_callback("all_products"), bg="red", fg="white").pack(pady=5)

    def update_cart(self):
        for widget in self.cart_frame.winfo_children():
            widget.destroy()

        cart_items = self.controller.cart
        if not cart_items:
            tk.Label(self.cart_frame, text="El carrito está vacío.").pack()
        else:
            for index, product in enumerate(cart_items):
                product_frame = tk.Frame(self.cart_frame)
                product_frame.pack(fill='x', pady=2)
                tk.Label(product_frame, text=f"{product['name']} - ${product['price']}").pack(side="left")
                tk.Button(product_frame, text="Quitar", command=lambda i=index: self.remove_item(i), bg="gray", fg="white").pack(side="right")

    def remove_item(self, index):
        del self.controller.cart[index]
        self.update_cart()

    def go_to_summary(self):
        if not self.controller.cart:
            messagebox.showerror("Error", "El carrito está vacío.")
        else:
            self.change_view_callback("summary")

    def show(self):
        self.update_cart()
        super().show()

# Vista para el resumen de la compra
class SummaryView(BaseView):
    def __init__(self, root, change_view_callback, controller):
        super().__init__(root, change_view_callback, controller)
        tk.Label(self.frame, text="Resumen de Compra", font=("Arial", 16)).pack(pady=10)
        self.summary_frame = tk.Frame(self.frame)
        self.summary_frame.pack(pady=10)
        self.total_label = tk.Label(self.frame, text="")
        self.total_label.pack(pady=5)
        tk.Button(self.frame, text="Confirmar Compra", command=self.confirm_purchase, bg="green", fg="white").pack(pady=5)
        tk.Button(self.frame, text="Volver", command=lambda: self.change_view_callback("cart"), bg="red", fg="white").pack(pady=5)

    def update_summary(self):
        for widget in self.summary_frame.winfo_children():
            widget.destroy()

        cart_items = self.controller.cart
        total = 0
        for product in cart_items:
            tk.Label(self.summary_frame, text=f"{product['name']} - ${product['price']}").pack()
            total += product['price']
        self.total_label.config(text=f"Total: ${total}")

    def confirm_purchase(self):
        if not self.controller.cart:
            messagebox.showerror("Error", "El carrito está vacío.")
        else:
            messagebox.showinfo("Compra", "Compra realizada exitosamente.")
            self.controller.cart.clear()
            self.change_view_callback("all_products")

    def show(self):
        self.update_summary()
        super().show()

# Controlador de la aplicación
class Controller:
    def __init__(self):
        self.user = None
        # Definición de usuarios: admin y guest
        self.users = {"admin": "admin", "guest": "guest"}
        self.products = [
            {"name": "Laptop", "price": 1000},
            {"name": "Teléfono", "price": 500},
            {"name": "Tablet", "price": 300}
        ]
        self.cart = []

    def authenticate_user(self, username):
        if username in self.users:
            self.user = username
            return True
        return False

    def logout_user(self):
        self.user = None

    def get_products(self):
        return self.products

    def add_product(self, name, price):
        self.products.append({"name": name, "price": price})

    def add_to_cart(self, product):
        self.cart.append(product)

# Clase principal de la aplicación
class MercadoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mercado Inteligente")
        self.controller = Controller()

        # Se agregan todas las vistas
        self.views = {
            "login": LoginView(root, self.change_view, self.controller),
            "all_products": AllProductsView(root, self.change_view, self.controller),
            "add_product": AddProductView(root, self.change_view, self.controller),
            "cart": CartView(root, self.change_view, self.controller),
            "summary": SummaryView(root, self.change_view, self.controller)
        }

        self.current_view = None
        self.change_view("login")

    def change_view(self, view_name):
        # Validación para que solo admin acceda a la vista de agregar productos
        if view_name == "add_product" and self.controller.user != "admin":
            messagebox.showerror("Acceso Denegado", "Solo usuarios admin pueden acceder a esta vista.")
            view_name = "all_products"
        if self.current_view:
            self.current_view.hide()
        self.current_view = self.views[view_name]
        self.current_view.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = MercadoApp(root)
    root.mainloop()
