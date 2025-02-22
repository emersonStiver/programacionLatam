# Mercado Inteligente

Mercado Inteligente es una aplicación de escritorio desarrollada en Python que simula un sistema de gestión de carrito de compras con una interfaz gráfica basada en Tkinter. La aplicación utiliza Programación Orientada a Objetos (POO) para gestionar productos, aplicar descuentos y generar tickets de compra.

## Características

- **Gestión de Productos:**  
  Permite visualizar una lista de productos (incluyendo subclases como Electrónicos) y agregar nuevos productos al catálogo.

- **Carrito de Compras:**  
  Los usuarios pueden agregar productos al carrito, especificar la cantidad y calcular el total de la compra con descuentos automáticos (10% de descuento si se agregan 3 o más unidades en total).

- **Interfaz Gráfica Light:**  
  La aplicación cuenta con una interfaz moderna con un tema light, en el que se utilizan colores claros para garantizar la visibilidad de los inputs y otros elementos.

- **Modularidad y Escalabilidad:**  
  La aplicación se ha estructurado de forma modular, separando modelos, controladores, vistas y configuraciones, lo que facilita su mantenimiento y futuras ampliaciones.

## Estructura del Proyecto

```
mercado_inteligente/
├── README.md
├── requirements.txt
├── main.py
└── app/
├── __init__.py
├── config.py         # Configuraciones (colores, estilos, etc.)
├── controllers.py    # Lógica de negocio y controlador
├── models.py         # Definición de las clases del dominio (Producto, Electronico, Carrito)
└── views.py          # Vistas de la interfaz gráfica (Tkinter)
```

## Requisitos

- **Python 3.x:**  
  La aplicación está desarrollada en Python 3. Se recomienda tener instalado Python 3.6 o superior.

- **Tkinter:**  
  Tkinter viene incluido con la mayoría de las distribuciones de Python. Si por algún motivo no lo tienes instalado, consulta la [documentación oficial](https://docs.python.org/3/library/tkinter.html) para instalarlo en tu sistema.

## Instalación

1. **Clonar el repositorio:**

   ```bash
   git clone https://github.com/tu_usuario/mercado_inteligente.git
   cd mercado_inteligente
   ```

2. **Crear y activar un entorno virtual (opcional, recomendado):**

   ```bash
   python -m venv venv
   # En Windows
   venv\Scripts\activate
   # En Linux/Mac
   source venv/bin/activate
   ```

3. **Instalar dependencias:**

   En este caso, la única dependencia extra podría ser algún paquete adicional que decidas usar. Si no hay dependencias externas (Tkinter está incluido), puedes dejar el archivo `requirements.txt` vacío o con comentarios.

   ```bash
   pip install -r requirements.txt
   ```

## Ejecución

Para ejecutar la aplicación, simplemente corre el archivo `main.py`:

```bash
python main.py
```

Al iniciar, se abrirá una ventana con la lista de productos disponibles. Podrás navegar entre las vistas para agregar productos, ver el carrito, eliminar productos, confirmar la compra y ver el ticket de compra generado.



# Implementación de la Programación Orientada a Objetos (POO) en Mercado Inteligente

El proyecto "Mercado Inteligente" está diseñado utilizando los principios fundamentales de la Programación Orientada a Objetos (POO). A continuación se explica cómo se implementaron cada uno de los pilares:

## 1. Abstracción

Se han creado clases que representan conceptos del dominio del problema, permitiendo trabajar con objetos que encapsulan datos y comportamientos sin exponer detalles internos.

- **Ejemplo:**  
  La clase `Producto` abstrae la idea de un producto, encapsulando atributos como el nombre y el precio, y proporcionando un método `__str__` para obtener una representación en cadena.  
  Además, la clase `Controller` sirve de interfaz entre la "base de datos" simulada (una lista de objetos) y la interfaz gráfica, ofreciendo métodos para obtener productos y gestionar el carrito.

## 2. Encapsulamiento

El encapsulamiento se logra mediante la definición de atributos privados (usando el prefijo `__`) y el acceso a ellos a través de métodos (getters). Esto protege la integridad de los datos y evita modificaciones directas desde fuera de la clase.

- **Ejemplo:**  
  En la clase `Producto`:
  ```python
  class Producto:
      def __init__(self, nombre, precio):
          self.__nombre = nombre   # Atributo privado
          self.__precio = precio

      @property
      def nombre(self):
          return self.__nombre

      @property
      def precio(self):
          return self.__precio
  ```
Los atributos `__nombre` y `__precio` son privados, y se accede a ellos mediante las propiedades `nombre` y `precio`.

## 3. Herencia

La herencia permite crear nuevas clases que extienden o especializan el comportamiento de clases existentes. Esto favorece la reutilización del código y la extensión de funcionalidades.

- **Ejemplo:**  
  La clase `Electronico` hereda de `Producto` y añade un atributo adicional para la garantía:
  ```python
  class Electronico(Producto):
      def __init__(self, nombre, precio, garantia_meses):
          super().__init__(nombre, precio)
          self.__garantia = garantia_meses

      @property
      def garantia(self):
          return self.__garantia

      def __str__(self):
          return f"{self.nombre} (Garantía: {self.garantia} meses) - ${self.precio:.2f}"
  ```
  Aquí, `Electronico` reutiliza la estructura de `Producto` y sobrescribe el método `__str__` para incluir información adicional (la garantía).

## 4. Polimorfismo

El polimorfismo se consigue mediante la sobrescritura de métodos en las clases hijas, permitiendo que se comporten de manera distinta cuando se invocan métodos con el mismo nombre.

- **Ejemplo:**  
  El método `__str__` en la clase `Producto` es sobrescrito en `Electronico`:
    - En `Producto`, `__str__` devuelve una cadena simple con el nombre y precio.
    - En `Electronico`, `__str__` devuelve la cadena con información adicional de la garantía.

  Esto significa que, al imprimir un objeto, el método correcto se ejecuta según el tipo de objeto:
  ```python
  producto = Producto("Tablet", 300.0)
  electronico = Electronico("Teléfono", 500.0, garantia_meses=24)
  print(producto)      # Muestra: Tablet - $300.00
  print(electronico)   # Muestra: Teléfono (Garantía: 24 meses) - $500.00
  ```

## Resumen de la Organización del Proyecto

- **Modelos (`app/models.py`):**
    - `Producto` y `Electronico` encapsulan los datos y comportamientos de los productos.
    - `Carrito` gestiona la lógica del carrito de compras (agregar productos, calcular totales, aplicar descuentos).

- **Controlador (`app/controllers.py`):**
    - La clase `Controller` centraliza la lógica de negocio, conectando los modelos con la interfaz gráfica.

- **Vistas (`app/views.py`):**
    - Las vistas se encargan de la interacción con el usuario a través de Tkinter, utilizando la abstracción y encapsulamiento para comunicarse con el controlador sin conocer detalles internos de los modelos.



## Consideraciones

- La aplicación utiliza una "base de datos" simulada (listas en memoria) para gestionar los productos y el carrito de compras.
- La estructura modular permite ampliar la aplicación fácilmente, por ejemplo, integrando una base de datos real o nuevas funcionalidades en el futuro.

## Contribuciones

¡Las contribuciones son bienvenidas! Si deseas mejorar la aplicación, por favor, crea un *fork* del repositorio, haz tus cambios y envía un *pull request*.

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.
