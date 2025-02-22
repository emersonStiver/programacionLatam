import tkinter as tk
from app.controllers import Controller
from app.views import MercadoApp


def main():
    root = tk.Tk()
    controller = Controller()
    app = MercadoApp(root, controller)
    root.mainloop()


if __name__ == "__main__":
    main()
