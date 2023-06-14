import os
import json
from json import JSONEncoder
import pyinputplus as pyip


class Estudiante:
    def __init__(estudiante, cedula, nombre, edad, sexo, telefono, direccion):
        estudiante.cedula = cedula
        estudiante.nombre = nombre
        estudiante.edad = edad
        estudiante.sexo = sexo
        estudiante.telefono = telefono
        estudiante.direccion = direccion
        estudiante.creditos = 30
        estudiante.pedidos = []

    def hacer_pedido(self, alimento, cantidad, valor):
        pedido = {
            'alimento': alimento,
            'cantidad': cantidad,
            'valor': valor
        }
        self.pedidos.append(pedido)
        self.creditos = self.creditos - cantidad*valor

    def mostrar_comprobante(self):
            for pedido in self.pedidos:
                print("Alimento: ", pedido['alimento'])
                print("Cantidad: ", pedido['cantidad'])
                print("Valor: ", pedido['valor'])
            print("Crédito final: ", self.creditos)

            input("ingrese para continuar....")

    def abonar_credito(self, monto):
        self.creditos += monto

    def actualizar_datos_personales(self, direccion=None, telefono=None):
        if direccion:
            self.direccion = direccion
        if telefono:
            self.telefono = telefono

class EstudianteEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__

def menu():
    estudiante = None

    while True:
        os.system ("cls")
        print("\n--- Menú Principal ---")
        print("1. Registrar datos personales del estudiante")
        print("2. Realizar pedido")
        print("3. Abonar crédito")
        print("4. Salir")

        opcion = input("Ingrese el número de opción: ")

        if opcion == "1":
            estudiante = registrar_datos_personales()
        elif opcion == "2":
            realizar_pedido(estudiante)
        elif opcion == "3":
            abonar_credito(estudiante)
        elif opcion == "4":
            break
        else:
            print("Opción inválida. Por favor, ingrese nuevamente.")

def registrar_datos_personales():
    os.system ("cls")
    cedula = input("Ingrese su cedula: ")
    nombre = input("Ingrese su nombre: ")
    edad = int(pyip.inputNum("Ingrese su edad: ", allowRegexes=[r'^[0-9]+$'], blockRegexes=[(r'.*','¡Debe ingresar un número entero!')]))
    sexo = input("Ingrese su sexo: ")
    telefono = input("Ingrese su teléfono: ")
    direccion = input("Ingrese su dirección: ")

    estudiante = Estudiante(cedula, nombre, edad, sexo, telefono, direccion)
    jsonString = json.dumps(estudiante, indent=4, cls=EstudianteEncoder)
    jsonFile = open("data.json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()

    print("Datos personales registrados correctamente.")
    return estudiante 
    

def realizar_pedido(estudiante):
    os.system ("cls")

    while True:
        print("\n--- Lista de alimentos disponibles ---")
        print("1. hamburguesa ------ 5.0")
        print("2. Arepa ------------ 2.0")
        print("3. Jugo de naranja -- 3.5")

        opcion = input("Ingrese el número de opción: ")
        if opcion == "1":
            alimento = "hamburguesa"
            valor = 5.0
            break

        elif opcion == "2":
            alimento = "Arepa"
            valor = 2.0
            break

        elif opcion == "3":
            alimento = "Jugo de naranja"
            valor = 3.5
            break
            

    cantidad = int(pyip.inputNum("Ingrese la cantidad que desea pedir: ", allowRegexes=[r'^[0-9]+$'], blockRegexes=[(r'.*','¡Debe ingresar un número entero!')]))

    if(estudiante.creditos < cantidad*valor):
        input("No tiene saldo suficiente.")
        return

    estudiante.hacer_pedido(alimento, cantidad, valor)

    with open("data.json","r") as jsonFile:
        data = json.load(jsonFile)

    data["pedidos"] = estudiante.pedidos
    data["creditos"] = estudiante.creditos

    with open("data.json", "w") as jsonFile:
        json.dump(data, jsonFile,indent=4)

    print("Pedido registrado correctamente.")
    input()

def abonar_credito(estudiante):
    os.system ("cls")
    monto = float(pyip.inputNum("Ingrese el monto que desea abonar: ",allowRegexes=[r'^\d*\.?\d*$'], blockRegexes=[(r'.*','¡Debe ingresar un número!')]))

    if(monto < 30 - estudiante.creditos):
        estudiante.abonar_credito(monto)
        print("Crédito abonado correctamente.")

        with open("data.json","r") as jsonFile:
            data = json.load(jsonFile)

        data["creditos"] = estudiante.creditos

        with open("data.json", "w") as jsonFile:
            json.dump(data, jsonFile,indent=4)

        input()
    else:
        print("El monto ingresado es mayor al saldo pendiente.")
        input()


menu()