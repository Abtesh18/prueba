import json
import os

DATA_FILE = 'presupuesto.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    else:
        return []

def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def add_item(data):
    nombre = input("Ingrese el nombre del artículo: ")
    cantidad = float(input("Ingrese la cantidad presupuestada: "))
    articulo = {'nombre': nombre, 'cantidad': cantidad}
    data.append(articulo)
    save_data(data)
    print("Artículo agregado con éxito.")

def search_item(data):
    nombre = input("Ingrese el nombre del artículo a buscar: ")
    for articulo in data:
        if articulo['nombre'].lower() == nombre.lower():
            print(f"Artículo encontrado: {articulo}")
            return
    print("Artículo no encontrado.")

def edit_item(data):
    nombre = input("Ingrese el nombre del artículo a editar: ")
    for articulo in data:
        if articulo['nombre'].lower() == nombre.lower():
            print(f"Artículo encontrado: {articulo}")
            nuevo_nombre = input("Ingrese el nuevo nombre (deje en blanco para no cambiar): ")
            nueva_cantidad = input("Ingrese la nueva cantidad (deje en blanco para no cambiar): ")
            if nuevo_nombre:
                articulo['nombre'] = nuevo_nombre
            if nueva_cantidad:
                articulo['cantidad'] = float(nueva_cantidad)
            save_data(data)
            print("Artículo actualizado con éxito.")
            return
    print("Artículo no encontrado.")

def delete_item(data):
    nombre = input("Ingrese el nombre del artículo a eliminar: ")
    for articulo in data:
        if articulo['nombre'].lower() == nombre.lower():
            data.remove(articulo)
            save_data(data)
            print("Artículo eliminado con éxito.")
            return
    print("Artículo no encontrado.")

def list_items(data):
    if data:
        for articulo in data:
            print(f"Nombre: {articulo['nombre']}, Cantidad: {articulo['cantidad']}")
    else:
        print("No hay artículos en el presupuesto.")

def main():
    data = load_data()

    while True:
        print("\nOpciones:")
        print("a) Agregar nuevo artículo")
        print("b) Buscar artículo")
        print("c) Editar artículo")
        print("d) Eliminar artículo")
        print("e) Listar todos los artículos")
        print("f) Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == 'a':
            add_item(data)
        elif opcion == 'b':
            search_item(data)
        elif opcion == 'c':
            edit_item(data)
        elif opcion == 'd':
            delete_item(data)
        elif opcion == 'e':
            list_items(data)
        elif opcion == 'f':
            print("Saliendo...")
            break
        else:
            print("Opción no válida, intente de nuevo.")

if __name__ == "__main__":
    main()
