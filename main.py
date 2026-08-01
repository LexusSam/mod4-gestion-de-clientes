#IMPORTAR LAS LIBRERIAS
from tkinter import messagebox # Para mostrar los usuarios
import tkinter as tk # Para hacer la interfaz
import re # Para usar las expresiones regulares y validar

#CREAR OBJETOS Y HERENCIAS
class Cliente: #Clase base
    def __init__(self, id_cliente, nombre, email, telefono, tipo):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.tipo = tipo

class ClienteRegular(Cliente): #Hereda de Cliente
    def __init__(self, id_cliente, nombre, email, telefono, tipo, empresa=None):
        super().__init__(id_cliente, nombre, email, telefono, tipo, empresa=None)

class ClientPremium(Cliente):#Hereda de Cliente
    def __init__(self, id_cliente, nombre, email, telefono, tipo, descuento):
        super().__init__(id_cliente, nombre, email, telefono, tipo)
        self.descuento = descuento

class ClienteCorporativo(Cliente):#Hereda de Cliente
    def __init__(self, id_cliente, nombre, email, telefono, tipo, empresa=None):
        super().__init__(id_cliente, nombre, email, telefono, tipo)
        self.empresa = empresa