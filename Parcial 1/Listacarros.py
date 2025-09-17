import tkinter as tk
from tkinter import ttk, messagebox

Ruta_del_logo = "lambo.ico"

# Clases para almacenar los datos.

class Vehiculo:
    def __init__(self, marca, modelo, año, kilometraje, precio):
        self.marca = marca
        self.modelo = modelo
        self.año = año
        self.kilometraje = kilometraje
        self.precio = precio

class Coche(Vehiculo):
    def __init__(self, marca, modelo, año, kilometraje, precio, num_puertas):
        super().__init__(marca, modelo, año, kilometraje, precio)
        self.num_puertas = num_puertas

class Moto(Vehiculo):
    def __init__(self, marca, modelo, año, kilometraje, precio, cilindrada):
        super().__init__(marca, modelo, año, kilometraje, precio)
        self.cilindrada = cilindrada

class Camioneta(Vehiculo):
    def __init__(self, marca, modelo, año, kilometraje, precio, capacidad_carga):
        super().__init__(marca, modelo, año, kilometraje, precio)
        self.capacidad_carga = capacidad_carga

# Clase para gestionar la lista de vehículos
class GestorCarros:
    def __init__(self):
        self.vehiculos = []

    def agregar_vehiculo(self, vehiculo):
        self.vehiculos.append(vehiculo)

    def eliminar_vehiculo(self, indice):
        self.vehiculos.pop(indice)

# Clase principal de la aplicación

class CarrosApp:
    def __init__(self,master):
        self.master = master
        master.title("App de Carros")
        master.geometry("400x400")

        # Configuracion de logo.

        try:
            master.iconbitmap(Ruta_del_logo)
        except tk.TclError:
            print(f"No se pudo cargar el logo o icono desde la ruta {Ruta_del_logo}")

        # Gestor 

        self.gestor = GestorCarros()

        # Creacion del menu

        barra_menu = tk.Menu(master)
        master.config(menu=barra_menu)

        # Menu de ayuda

        menu_ayuda = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="Ayuda", menu=menu_ayuda)
        menu_ayuda.add_command(label="Acerca de", command=self.mostrar_acerca_de)
        menu_ayuda.add_separator()
        menu_ayuda.add_command(label="Información del Autor", command=self.mostrar_info_autor)

        # Creacion de widgets.
        # Frame principal

        main_frame = ttk.Frame(master, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Etiquetas y entradas para el nombre y los componentes.

        ttk.Label(main_frame, text="Marca:").grid(row=0, column=0, sticky=tk.W)
        self.marca_entry = ttk.Entry(main_frame)
        self.marca_entry.grid(row=0, column=1)

        ttk.Label(main_frame, text="Modelo:").grid(row=1, column=0, sticky=tk.W)
        self.modelo_entry = ttk.Entry(main_frame)
        self.modelo_entry.grid(row=1, column=1)

        ttk.Label(main_frame, text="Año:").grid(row=2, column=0, sticky=tk.W)
        self.año_entry = ttk.Entry(main_frame)
        self.año_entry.grid(row=2, column=1)

        ttk.Label(main_frame, text="Kilometraje:").grid(row=3, column=0, sticky=tk.W)
        self.kilometraje_entry = ttk.Entry(main_frame)
        self.kilometraje_entry.grid(row=3, column=1)

        ttk.Label(main_frame, text="Precio:").grid(row=4, column=0, sticky=tk.W)
        self.precio_entry = ttk.Entry(main_frame)
        self.precio_entry.grid(row=4, column=1)

        ttk.Label(main_frame, text="Capacidad de carga:").grid(row=5, column=0, sticky=tk.W)
        self.capacidad_carga_entry = ttk.Entry(main_frame)
        self.capacidad_carga_entry.grid(row=5, column=1)

        #Boton para agregar Vehiculo
        self.btn_agregar = ttk.Button(main_frame, text="Agregar Vehiculo", command=self.agregar_vehiculo)
        self.btn_agregar.grid(row=6, columnspan=2, pady=10)

        #List box para mostrar los vehiculos guardados.

        self.lista_vehiculos = tk.Listbox(main_frame, width=50)
        self.lista_vehiculos.grid(row=7, column=0, columnspan=2, sticky="ew", pady=5)

        # Botones para ver y eliminar vehiculos.
        self.btn_ver = ttk.Button(main_frame, text="Ver Vehiculo", command=self.ver_vehiculo)
        self.btn_ver.grid(row=8, columnspan=2, pady=5)

        self.btn_eliminar = ttk.Button(main_frame, text="Eliminar Vehiculo", command=self.eliminar_vehiculo)
        self.btn_eliminar.grid(row=9, columnspan=2, pady=5)

    def agregar_vehiculo(self):
        marca = self.marca_entry.get()
        modelo = self.modelo_entry.get()
        año_str = self.año_entry.get()
        kilometraje_str = self.kilometraje_entry.get()
        precio_str = self.precio_entry.get()
        capacidad_carga_str = self.capacidad_carga_entry.get()

        if not all([marca, modelo, año_str, kilometraje_str, precio_str, capacidad_carga_str]):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            año = int(año_str)
            kilometraje = int(kilometraje_str)
            precio = float(precio_str)
            capacidad_carga = float(capacidad_carga_str)
        except ValueError:
            messagebox.showerror("Error de validación", "Año, Kilometraje, Precio y Capacidad de carga deben ser números.")
            return

        # Como la UI solo tiene campo para capacidad de carga, creamos una Camioneta.
        vehiculo = Camioneta(marca, modelo, año, kilometraje, precio, capacidad_carga)
        self.gestor.agregar_vehiculo(vehiculo)
        self.actualizar_lista()

        # Limpiar entradas
        self.marca_entry.delete(0, tk.END)
        self.modelo_entry.delete(0, tk.END)
        self.año_entry.delete(0, tk.END)
        self.kilometraje_entry.delete(0, tk.END)
        self.precio_entry.delete(0, tk.END)
        self.capacidad_carga_entry.delete(0, tk.END)

    def actualizar_lista(self):
        self.lista_vehiculos.delete(0, tk.END)
        for vehiculo in self.gestor.vehiculos:
            self.lista_vehiculos.insert(tk.END, f"{vehiculo.marca} {vehiculo.modelo} ({vehiculo.año})")

    def ver_vehiculo(self):
        seleccionado = self.lista_vehiculos.curselection()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un vehículo de la lista.")
            return
        indice = seleccionado[0]
        vehiculo = self.gestor.vehiculos[indice]
        info = (f"Marca: {vehiculo.marca}\n"
                f"Modelo: {vehiculo.modelo}\n"
                f"Año: {vehiculo.año}\n"
                f"Kilometraje: {vehiculo.kilometraje} km\n"
                f"Precio: ${vehiculo.precio:,.2f}\n"
                f"Capacidad de Carga: {vehiculo.capacidad_carga} kg")
        messagebox.showinfo("Detalles del Vehículo", info)

    def eliminar_vehiculo(self):
        seleccionado = self.lista_vehiculos.curselection()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un vehículo para eliminar.")
            return
        indice = seleccionado[0]
        self.gestor.eliminar_vehiculo(indice)
        self.actualizar_lista()

    def mostrar_acerca_de(self):
        messagebox.showinfo("Acerca de", "App de Carros v1.0\nCreado para gestionar una lista de vehículos.")

    def mostrar_info_autor(self):
        messagebox.showinfo("Información del Autor", "Emmanuel Granados P.\n Ing Informatica.\n Parcial number one.")  

if __name__ == "__main__":
    root = tk.Tk()
    app = CarrosApp(root)
    root.mainloop()