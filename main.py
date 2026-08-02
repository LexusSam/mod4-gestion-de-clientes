#IMPORTAR LAS LIBRERIAS
from tkinter import messagebox # Para mostrar los usuarios
import tkinter as tk # Para hacer la interfaz
import re # Para usar las expresiones regulares y validar

#CREAR OBJETOS Y HERENCIAS
class Cliente: #Clase base
    def __init__(self, id_cliente, nombre, email, telefono, tipo):
        self.id_cliente = id_cliente
        self.__nombre = nombre # Se encapsulan datos
        self.__email = email # Se encapsulan datos
        self.__telefono = telefono # Se encapsulan datos
        self.tipo = tipo

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

#SE INGRESAN Y ALMACENAN LOS DATOS DE LOS CLIENTES

class Datos:
    def __init__ (self, archivo):
        self.archivo = archivo
        pass #AGREGAR CONDICIONAL

    def guardar_cliente(self, cliente, Cliente):
        #AGREGAR EXPRESIOIN PARA AGREWGAR EL CLIENTE AL .TXT
        pass
    
    def cargar_clientes(self):
        clientes = [] #AGREGAR EXPRESION PARA TOMAR DATOS Y MOSTRALROS
        pass
    
    def sobrescribir_clientes(self, clientes):
        pass #AGREGAR EXPRESION PARA EDITAR CLIENTE

#SE INGRESAN Y ALMACENAN LOS DATOS DE LOS CLIENTES
class GestorClientes:
    def __init__():
        pass

    def obtener_next_id(self):
        pass

    def registrar_cliente(elf, cliente: Cliente):
        pass

    def eliminar_cliente():
        pass

    def editar_cliente():
        pass