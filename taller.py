import os
import pymysql
import time

def limpiar():
    os.system('cls' if os.name == 'nt' else 'clear')

class Taller:
    def __init__(self):
        try:
            self.db = pymysql.connect(
                host="localhost",
                port=3306,
                user="root",
                password="root",
                database="taller_mecanico"
            )
            self.cursor = self.db.cursor()
            print("Conectado al taller. Todo listo para trabajar.\n")
            time.sleep(1)
        except Exception as e:
            print("No se pudo conectar a la base de datos. Revisar configuracion.")
            exit()

    def menu(self):
        limpiar()
        print("MENU PRINCIPAL")
        print("1. Clientes")
        print("2. Vehiculos")
        print("3. Mecanicos")
        print("4. Fichas tecnicas")
        print("5. Facturacion")
        print("6. Salir")

    # ----- clientes -----
    def menu_clientes(self):
        print("1. Ver todos los clientes")
        print("2. Agregar cliente")
        print("3. Buscar cliente por DNI")
        print("4. Eliminar cliente")
        print("5. Volver")

    def ver_clientes(self):
        limpiar()
        print("-- Lista de clientes --")
        self.cursor.execute("SELECT * FROM Clientes")
        lista = self.cursor.fetchall()
        if not lista:
            print("No hay clientes registrados por ahora.")
        else:
            for c in lista:
                print(f"DNI: {c[0]} | Nombre: {c[1]} {c[2]} | Direccion: {c[3]} | Telefono: {c[4]}")
        input("Presione Enter para volver...")

    def agregar_cliente(self):
        limpiar()
        print("Agregar nuevo cliente")
        dni = input("DNI: ")
        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        dire = input("Direccion: ")
        tel = input("Telefono: ")
        self.cursor.execute(
            "INSERT INTO Clientes (DNI, Nombre, Apellido, Direccion, Telefono) VALUES (%s,%s,%s,%s,%s)",
            (dni, nombre, apellido, dire, tel)
        )
        self.db.commit()
        print("Cliente agregado correctamente.")
        time.sleep(1)

    def buscar_cliente(self):
        limpiar()
        dni = input("Ingrese el DNI a buscar: ")
        self.cursor.execute("SELECT DNI, Nombre, Apellido, Telefono FROM Clientes WHERE DNI=%s", (dni,))
        cli = self.cursor.fetchone()
        if cli:
            print(f"DNI: {cli[0]} | Nombre: {cli[1]} | Apellido: {cli[2]} | Telefono: {cli[3]}")
        else:
            print("No se encontro un cliente con ese DNI.")
        input("Presione Enter para continuar...")

    def eliminar_cliente(self):
        limpiar()
        dni = input("DNI del cliente que se quiere eliminar: ")
        #eliminar datos asociados
        self.cursor.execute("DELETE FROM Facturacion WHERE DNI_Cliente=%s", (dni,))
        self.cursor.execute("DELETE FROM Vehiculos WHERE DNI=%s", (dni,))
        self.cursor.execute("DELETE FROM Ficha_tecnica WHERE dni_cliente=%s", (dni,))
        self.db.commit()
        #eliminar cliente
        self.cursor.execute("DELETE FROM Clientes WHERE DNI=%s", (dni,))
        self.db.commit()
        print("Operacion realizada. Si el cliente existia, ya fue eliminado.")
        time.sleep(1)

    # ----- vehiculos -----
    def menu_vehiculos(self):
        print("1. Ver todos los vehiculos")
        print("2. Agregar vehiculo")
        print("3. Buscar vehiculo por patente")
        print("4. Eliminar vehiculo")
        print("5. Volver")

    def ver_vehiculos(self):
        limpiar()
        print("-- Lista de vehiculos --")
        self.cursor.execute("SELECT * FROM Vehiculos")
        autos = self.cursor.fetchall()
        if not autos:
            print("No hay vehiculos cargados.")
        else:
            for a in autos:
                print(f"Patente: {a[0]} | DNI duenio: {a[1]} | Marca: {a[2]} | Modelo: {a[3]} | Color: {a[4]}")
        input("Presione Enter para continuar...")

    def agregar_auto(self):
        limpiar()
        print("Cargar nuevo vehiculo")
        patente = input("Patente: ")
        dni = input("DNI del duenio: ")
        marca = input("Marca: ")
        modelo = input("Modelo: ")
        color = input("Color: ")
        self.cursor.execute(
            "INSERT INTO Vehiculos (Patente, DNI, Marca, Modelo, Color) VALUES (%s,%s,%s,%s,%s)",
            (patente, dni, marca, modelo, color)
        )
        self.db.commit()
        print("Vehiculo registrado correctamente.")
        time.sleep(1)

    def buscar_auto(self):
        limpiar()
        patente = input("Ingrese la patente a buscar: ")
        self.cursor.execute("SELECT Patente, Marca, Modelo FROM Vehiculos WHERE Patente=%s", (patente,))
        auto = self.cursor.fetchone()
        if auto:
            print(f"Patente: {auto[0]} | Marca: {auto[1]} | Modelo: {auto[2]}")
        else:
            print("No se encontro ese vehiculo.")
        input("Presione Enter para continuar...")

    def eliminar_auto(self):
        limpiar()
        patente = input("Patente del vehiculo a eliminar: ")
        self.cursor.execute("DELETE FROM Vehiculos WHERE Patente=%s", (patente,))
        self.db.commit()
        print("Operacion realizada. Si el vehiculo existia, ya fue eliminado.")
        time.sleep(1)

    # ----- mecanicos -----
    def menu_mecanicos(self):
        print("1. Ver mecanicos")
        print("2. Agregar mecanico")
        print("3. Buscar mecanico")
        print("4. Eliminar mecanico")
        print("5. Volver")

    def ver_mecanicos(self):
        limpiar()
        print("-- Lista de mecanicos --")
        self.cursor.execute("SELECT * FROM Mecanicos")
        lista = self.cursor.fetchall()
        if not lista:
            print("No hay mecanicos registrados.")
        else:
            for m in lista:
                print(f"Legajo: {m[0]} | Nombre: {m[1]} {m[2]} | Rol: {m[3]} | Estado: {m[4]}")
        input("Presione Enter para continuar...")

    def agregar_mecanico(self):
        limpiar()
        print("Agregar nuevo mecanico")
        legajo = input("Legajo: ")
        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        rol = input("Rol: ")
        estado = ""
        while estado not in ["+","-"]:
            estado = input("Estado (+ para activo, - para inactivo): ")
        self.cursor.execute(
            "INSERT INTO Mecanicos (Legajo, Nombre, Apellido, Rol, Estado) VALUES (%s,%s,%s,%s,%s)",
            (legajo, nombre, apellido, rol, estado)
        )
        self.db.commit()
        print("Mecanico agregado correctamente.")
        time.sleep(1)

    def buscar_mecanico(self):
        limpiar()
        legajo = input("Ingrese el legajo a buscar: ")
        self.cursor.execute("SELECT Legajo, Nombre, Apellido, Rol, Estado FROM Mecanicos WHERE Legajo=%s", (legajo,))
        m = self.cursor.fetchone()
        if m:
            print(f"Legajo: {m[0]} | Nombre: {m[1]} | Apellido: {m[2]} | Rol: {m[3]} | Estado: {m[4]}")
        else:
            print("No se encontro ningun mecanico con ese legajo.")
        input("Presione Enter para continuar...")

    def eliminar_mecanico(self):
        limpiar()
        legajo = input("Legajo del mecanico a eliminar: ")
        self.cursor.execute("DELETE FROM Mecanicos WHERE Legajo=%s", (legajo,))
        self.db.commit()
        print("Operacion realizada. Si el mecanico existia, ya fue eliminado.")
        time.sleep(1)

    # ----- fichas tecnicas -----
    def menu_fichas(self):
        print("1. Crear ficha tecnica")
        print("2. Ver ficha(s) tecnica(s)")
        print("3. Modificar ficha tecnica")
        print("4. Volver")

    def crear_ficha(self):
        limpiar()
        print("Crear nueva ficha tecnica")
        idf = input("ID de ficha: ")
        dni = input("DNI del cliente: ")
        marca = input("Marca: ")
        modelo = input("Modelo: ")
        patente = input("Patente: ")
        motivo = input("Motivo de ingreso: ")
        fecha = input("Fecha de ingreso (YYYY-MM-DD): ")
        self.cursor.execute(
            "INSERT INTO Ficha_tecnica (id_ficha, dni_cliente, marca, modelo, patente, motivo_ingreso, fecha_ingreso) VALUES (%s,%s,%s,%s,%s,%s,%s)",
            (idf, dni, marca, modelo, patente, motivo, fecha)
        )
        self.db.commit()
        print("Ficha tecnica creada correctamente.")
        time.sleep(1)

    def ver_fichas(self):
        limpiar()
        idf = input("ID de ficha tecnica (dejar vacio para ver todas): ")
        if idf.strip() == "":
            self.cursor.execute("SELECT * FROM Ficha_tecnica")
            fichas = self.cursor.fetchall()
            if not fichas:
                print("No hay fichas tecnicas registradas.")
            else:
                for f in fichas:
                    print(f)
        else:
            self.cursor.execute("SELECT * FROM Ficha_tecnica WHERE id_ficha=%s", (idf,))
            ficha = self.cursor.fetchone()
            print(ficha if ficha else "No se encontro esa ficha tecnica.")
        input("Presione Enter para continuar...")

    def modificar_ficha(self):
        limpiar()
        idf = input("ID de la ficha tecnica a modificar: ")
        self.cursor.execute("SELECT * FROM Ficha_tecnica WHERE id_ficha=%s", (idf,))
        ficha = self.cursor.fetchone()
        if not ficha:
            print("No se encontro esa ficha tecnica.")
            time.sleep(1)
            return
        print("1. Cambiar datos del vehiculo (marca/modelo/patente)")
        print("2. Cambiar DNI del cliente")
        print("3. Cancelar")
        op = input("Opcion: ")
        if op == "1":
            campo = input("Indique que campo desea cambiar (marca/modelo/patente): ")
            if campo not in ["marca", "modelo", "patente"]:
                print("Campo incorrecto.")
                return
            nuevo = input(f"Ingrese el nuevo valor para {campo}: ")
            self.cursor.execute(f"UPDATE Ficha_tecnica SET {campo}=%s WHERE id_ficha=%s", (nuevo, idf))
        elif op == "2":
            nuevo = input("Nuevo DNI del cliente: ")
            self.cursor.execute("UPDATE Ficha_tecnica SET dni_cliente=%s WHERE id_ficha=%s", (nuevo, idf))
        else:
            print("No se realizaron cambios.")
            return
        self.db.commit()
        print("Ficha tecnica actualizada correctamente.")
        time.sleep(1)

    # ------ facturacion ------
    def menu_facturacion(self):
        print("1. Nueva factura")
        print("2. Anular factura")
        print("3. Ver facturas")
        print("4. Volver")

    def nueva_factura(self):
        limpiar()
        print("Registrar nueva factura")
        dni = input("DNI del cliente: ")
        fecha = input("Fecha (YYYY-MM-DD): ")
        monto = input("Monto: ")
        estado = "Emitida"
        self.cursor.execute(
            "INSERT INTO Facturacion (DNI_Cliente, Fecha_Factura, Monto, Estado) VALUES (%s,%s,%s,%s)",
            (dni, fecha, monto, estado)
        )
        self.db.commit()
        print("Factura registrada correctamente.")
        time.sleep(1)

    def anular_factura(self):
        limpiar()
        idf = input("ID de la factura a anular: ")
        self.cursor.execute("UPDATE Facturacion SET Estado='Anulada' WHERE id_factura=%s", (idf,))
        if self.cursor.rowcount == 0:
            print("No se encontro esa factura.")
        else:
            self.db.commit()
            print("Factura anulada correctamente.")
        time.sleep(1)

    def ver_facturas(self):
        limpiar()
        idf = input("ID de la factura (dejar vacio para ver todas): ")
        if idf.strip() == "":
            self.cursor.execute("SELECT * FROM Facturacion")
            facturas = self.cursor.fetchall()
            if not facturas:
                print("No hay facturas registradas.")
            else:
                for f in facturas:
                    print(f)
        else:
            self.cursor.execute("SELECT * FROM Facturacion WHERE id_factura=%s", (idf,))
            f = self.cursor.fetchone()
            print(f if f else "No se encontro esa factura.")
        input("Presione Enter para continuar...")

    def salir(self):
        print("Cerrando el programa. Hasta luego.")
        self.cursor.close()
        self.db.close()
        exit()

def main():
    taller = Taller()
    while True:
        taller.menu()
        op = input("Opcion: ")
        if op == "1":
            while True:
                limpiar()
                taller.menu_clientes()
                op2 = input("Opcion: ")
                if op2 == "1":
                    taller.ver_clientes()
                elif op2 == "2":
                    taller.agregar_cliente()
                elif op2 == "3":
                    taller.buscar_cliente()
                elif op2 == "4":
                    taller.eliminar_cliente()
                elif op2 == "5":
                    break
                else:
                    print("Opcion incorrecta, intenta de nuevo.")
                    time.sleep(1)
        elif op == "2":
            while True:
                limpiar()
                taller.menu_vehiculos()
                op2 = input("Opcion: ")
                if op2 == "1":
                    taller.ver_vehiculos()
                elif op2 == "2":
                    taller.agregar_auto()
                elif op2 == "3":
                    taller.buscar_auto()
                elif op2 == "4":
                    taller.eliminar_auto()
                elif op2 == "5":
                    break
                else:
                    print("Opcion incorrecta, intenta de nuevo.")
                    time.sleep(1)
        elif op == "3":
            while True:
                limpiar()
                taller.menu_mecanicos()
                op2 = input("Opcion: ")
                if op2 == "1":
                    taller.ver_mecanicos()
                elif op2 == "2":
                    taller.agregar_mecanico()
                elif op2 == "3":
                    taller.buscar_mecanico()
                elif op2 == "4":
                    taller.eliminar_mecanico()
                elif op2 == "5":
                    break
                else:
                    print("Opcion incorrecta, intenta de nuevo.")
                    time.sleep(1)
        elif op == "4":
            while True:
                limpiar()
                taller.menu_fichas()
                op2 = input("Opcion: ")
                if op2 == "1":
                    taller.crear_ficha()
                elif op2 == "2":
                    taller.ver_fichas()
                elif op2 == "3":
                    taller.modificar_ficha()
                elif op2 == "4":
                    break
                else:
                    print("Opcion incorrecta, intenta de nuevo.")
                    time.sleep(1)
        elif op == "5":
            while True:
                limpiar()
                taller.menu_facturacion()
                op2 = input("Opcion: ")
                if op2 == "1":
                    taller.nueva_factura()
                elif op2 == "2":
                    taller.anular_factura()
                elif op2 == "3":
                    taller.ver_facturas()
                elif op2 == "4":
                    break
                else:
                    print("Opcion incorrecta, intenta de nuevo.")
                    time.sleep(1)
        elif op == "6":
            taller.salir()
        else:
            print("Opcion incorrecta, intenta de nuevo.")
            time.sleep(1)

if __name__ == '__main__':
    main()
