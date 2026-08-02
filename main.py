import tkinter as tk
from tkinter import ttk, messagebox
import re
import os

# ----------
class Cliente: #Clase base
    def __init__(self, id_cliente, nombre, email, telefono, tipo, empresa =None):
        self.id_cliente = id_cliente
        self.__nombre = nombre # Se encapsulan datos
        self.__email = email # Se encapsulan datos
        self.__telefono = telefono # Se encapsulan datos
        self.tipo = tipo
        self.empresa = empresa

    @property #getter
    def nombre(self):
        return self.__nombre
    
    @property #getter
    def email(self):
        return self.__email
    
    @property #getter
    def telefono(self):
        return self.__telefono
    
# Validacion de datos CLIENTES
    def validar_email(self):
        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(patron, self.email) is not None

    def validar_telefono(self):
        patron = r'^\+?\d{7,15}$'
        return re.match(patron, self.telefono) is not None

    def validar_datos(self):
        if not self.nombre.strip():
            return False
        if not self.validar_email():
            return False
        if not self.validar_telefono():
            return False
        if self.tipo == "Corporativo" and not self.empresa.strip():
            return False
        return True

    def __str__(self):
        if self.tipo == "Corporativo":
            return f"{self.id_cliente},{self.nombre},{self.email},{self.telefono},{self.tipo},{self.empresa}"
        else:
            return f"{self.id_cliente},{self.nombre},{self.email},{self.telefono},{self.tipo}"

class ClienteRegular(Cliente): #Hereda de Cliente
    def __init__(self, id_cliente, nombre, email, telefono, tipo, empresa=None):
        super().__init__(id_cliente, nombre, email, telefono, tipo, empresa=None)

class ClientPremium(Cliente):#Hereda de Cliente
    def __init__(self, id_cliente, nombre, email, telefono, tipo, descuento):
        super().__init__(id_cliente, nombre, email, telefono, tipo)
        self.descuento = descuento

#METODO ESTATICO PARA VALIDAR SI CLIENTE CUNPLE CON EL REQUISITO PARA DESCUENTO (SER PREMIUM)
    @staticmethod
    def descuento(self, payment, descuento=0.05):
        if self.tipo == ClientPremium:
            return payment * descuento
        else:
            print(f'Cliente ({self.tipo}) no califica para descuento.')

class ClienteCorporativo(Cliente):#Hereda de Cliente
    def __init__(self, id_cliente, nombre, email, telefono, tipo, empresa=None):
        super().__init__(id_cliente, nombre, email, telefono, tipo)
        self.__empresa = empresa # Se encapsulan datos


# ------------------ PERSISTENCIA ------------------
class Datos:
    def __init__(self, archivo):
        self.archivo = archivo
        if not os.path.exists(self.archivo):
            with open(self.archivo, "w", encoding="utf-8") as f:
                f.write("")

    def guardar_cliente(self, cliente: Cliente):
        with open(self.archivo, "a", encoding="utf-8") as f:
            f.write(str(cliente) + "\n")

    def cargar_clientes(self):
        clientes = []
        if os.path.exists(self.archivo):
            with open(self.archivo, "r", encoding="utf-8") as f:
                for linea in f:
                    datos = linea.strip().split(",")
                    if len(datos) >= 5:
                        id_cliente = int(datos[0])
                        nombre, email, telefono, tipo = datos[1:5]
                        empresa = datos[5] if len(datos) == 6 else None
                        clientes.append(Cliente(id_cliente, nombre, email, telefono, tipo, empresa))
        return clientes

    def sobrescribir_clientes(self, clientes):
        with open(self.archivo, "w", encoding="utf-8") as f:
            for cliente in clientes:
                f.write(str(cliente) + "\n")

# ------------------ CONTROLADOR ------------------
class GestorClientes:
    def __init__(self, persistencia: Datos):
        self.persistencia = persistencia
        self.clientes = self.persistencia.cargar_clientes()
        self.next_id = self.obtener_next_id()

    def obtener_next_id(self):
        if not self.clientes:
            return 1
        return max(c.id_cliente for c in self.clientes) + 1

    def registrar_cliente(self, cliente: Cliente):
        if cliente.validar_datos():
            self.clientes.append(cliente)
            self.persistencia.guardar_cliente(cliente)
            self.next_id += 1
            return True
        return False

    def eliminar_cliente(self, id_cliente):
        self.clientes = [c for c in self.clientes if c.id_cliente != id_cliente]
        self.persistencia.sobrescribir_clientes(self.clientes)

    def editar_cliente(self, id_cliente, nuevo_cliente: Cliente):
        for i, c in enumerate(self.clientes):
            if c.id_cliente == id_cliente:
                self.clientes[i] = nuevo_cliente
                self.persistencia.sobrescribir_clientes(self.clientes)
                return True
        return False

# ------------------ VISTA ------------------
class ClienteApp:
    def __init__(self, root, gestor: GestorClientes):
        self.root = root
        self.gestor = gestor
        self.root.title("Gestor de Clientes")

        # Configurar expansión de filas y columnas
        self.root.rowconfigure(7, weight=1)   
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(1, weight=1)

        # Entradas
        tk.Label(root, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_nombre = tk.Entry(root)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="Correo:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_email = tk.Entry(root)
        self.entry_email.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="Teléfono:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_telefono = tk.Entry(root)
        self.entry_telefono.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(root, text="Tipo de Cliente:").grid(row=3, column=0, padx=5, pady=5)
        self.tipo_var = tk.StringVar()
        self.combo_tipo = ttk.Combobox(root, textvariable=self.tipo_var, 
                                    values=["Regular", "Premium", "Corporativo"], state="readonly")
        self.combo_tipo.grid(row=3, column=1, padx=5, pady=5)
        self.combo_tipo.bind("<<ComboboxSelected>>", self.mostrar_empresa)

        self.label_empresa = tk.Label(root, text="Empresa:")
        self.entry_empresa = tk.Entry(root)

        # Botones
        tk.Button(root, text="Registrar", command=self.registrar_cliente).grid(row=5, column=0, pady=10)
        tk.Button(root, text="Editar", command=self.editar_cliente).grid(row=5, column=1, pady=10)
        tk.Button(root, text="Eliminar", command=self.eliminar_cliente).grid(row=6, column=0, pady=10)
        tk.Button(root, text="Mostrar Lista", command=self.mostrar_clientes).grid(row=6, column=1, pady=10)

# Frame para tabla + scrollbars
        frame_tabla = tk.Frame(root)
        frame_tabla.grid(row=7, column=0, columnspan=2, sticky="nsew")

        # Scrollbars
        scrollbar_y = tk.Scrollbar(frame_tabla, orient="vertical")
        scrollbar_x = tk.Scrollbar(frame_tabla, orient="horizontal")

        # Tabla
        self.tree = ttk.Treeview(root, columns=("ID","Nombre","Correo","Teléfono","Tipo","Empresa"), show="headings")
        for col in ("ID","Nombre","Correo","Teléfono","Tipo","Empresa"):
            self.tree.heading(col, text=col)
        self.tree.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")  # Expande con la ventana


    def mostrar_empresa(self, event):
        if self.tipo_var.get() == "Corporativo":
            self.label_empresa.grid(row=4, column=0, padx=5, pady=5)
            self.entry_empresa.grid(row=4, column=1, padx=5, pady=5)
        else:
            self.label_empresa.grid_forget()
            self.entry_empresa.grid_forget()

    def registrar_cliente(self):
        cliente = Cliente(self.gestor.next_id,
                        self.entry_nombre.get(),
                        self.entry_email.get(),
                        self.entry_telefono.get(),
                        self.tipo_var.get(),
                        self.entry_empresa.get() if self.tipo_var.get()=="Corporativo" else None)
        if self.gestor.registrar_cliente(cliente):
            messagebox.showinfo("Éxito", "Cliente registrado correctamente.")
            self.limpiar_campos()
            self.mostrar_clientes()
        else:
            messagebox.showerror("Error", "Datos inválidos.")

    def eliminar_cliente(self):
        seleccionado = self.tree.selection()
        if seleccionado:
            id_cliente = int(self.tree.item(seleccionado)["values"][0])
            self.gestor.eliminar_cliente(id_cliente)
            messagebox.showinfo("Éxito", "Cliente eliminado.")
            self.mostrar_clientes()
        else:
            messagebox.showwarning("Atención", "Seleccione un cliente.")

    def editar_cliente(self):
        seleccionado = self.tree.selection()
        if seleccionado:
            id_cliente = int(self.tree.item(seleccionado)["values"][0])
            nuevo_cliente = Cliente(id_cliente,
                                    self.entry_nombre.get(),
                                    self.entry_email.get(),
                                    self.entry_telefono.get(),
                                    self.tipo_var.get(),
                                    self.entry_empresa.get() if self.tipo_var.get()=="Corporativo" else None)
            if self.gestor.editar_cliente(id_cliente, nuevo_cliente):
                messagebox.showinfo("Éxito", "Cliente editado.")
                self.mostrar_clientes()
            else:
                messagebox.showerror("Error", "No se pudo editar.")
        else:
            messagebox.showwarning("Atención", "Seleccione un cliente.")

    def mostrar_clientes(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for cliente in self.gestor.clientes:
            self.tree.insert("", "end", values=(cliente.id_cliente, cliente.nombre, cliente.email,
                                                cliente.telefono, cliente.tipo, cliente.empresa if cliente.empresa else ""))

    def limpiar_campos(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.combo_tipo.set("")
        self.entry_empresa.delete(0, tk.END)

# ------------------ MAIN ------------------
if __name__ == "__main__":
    persistencia = Datos("clientes.txt")
    gestor = GestorClientes(persistencia)

    root = tk.Tk()
    root.geometry("575x335")  # Tamaño fijo e la ventana
    root.resizable(True, True)  # Permite redimensionar si el usuario quiere

    app = ClienteApp(root, gestor)
    root.mainloop()
    
    app = ClienteApp(root, gestor)
    root.mainloop()