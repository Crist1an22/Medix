from utils.facial import registrar_miembro
from utils.productos import registrar_producto

def mostrar_menu_principal():
    while True:
        print("\n=== SISTEMA DE FARMACIA ===")
        print("1. Registrar miembro (detección facial)")
        print("2. Registrar producto (captura de objeto)")
        print("3. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            nombre = input("Nombre del miembro: ")
            registrar_miembro(nombre)
        elif opcion == '2':
            producto = input("Nombre del producto: ")
            registrar_producto(producto)
        elif opcion == '3':
            print("Cerrando sistema...")
            break
        else:
            print("Opción inválida.")
