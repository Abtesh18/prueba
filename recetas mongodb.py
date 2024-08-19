from pymongo import MongoClient

def connect_to_mongo():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['recetasDB']
    return db['recetas']

def add_recipe(coleccion):
    nombre = input("Ingrese el nombre de la receta: ")
    ingredientes = input("Ingrese los ingredientes separados por coma: ").split(',')
    pasos = input("Ingrese los pasos separados por punto y coma: ").split(';')
    receta = {
        'nombre': nombre,
        'ingredientes': [i.strip() for i in ingredientes],
        'pasos': [p.strip() for p in pasos if p.strip()]  
    }
    coleccion.insert_one(receta)
    print("Receta añadida con éxito.")

def update_recipe(coleccion):
    nombre = input("Ingrese el nombre de la receta a actualizar: ")
    receta = coleccion.find_one({'nombre': nombre})
    if receta:
        print(f"Receta encontrada: {receta}")
        nuevo_nombre = input("Ingrese el nuevo nombre de la receta (deje en blanco para no cambiar): ")
        nuevos_ingredientes = input("Ingrese los nuevos ingredientes separados por coma (deje en blanco para no cambiar): ")
        nuevos_pasos = input("Ingrese los nuevos pasos separados por punto y coma (deje en blanco para no cambiar): ")
        
        update_fields = {}
        if nuevo_nombre:
            update_fields['nombre'] = nuevo_nombre
        if nuevos_ingredientes:
            update_fields['ingredientes'] = [i.strip() for i in nuevos_ingredientes.split(',')]
        if nuevos_pasos:
            update_fields['pasos'] = [p.strip() for p in nuevos_pasos.split(';') if p.strip()]
        
        if update_fields:
            coleccion.update_one({'nombre': nombre}, {'$set': update_fields})
            print("Receta actualizada con éxito.")
        else:
            print("No se realizaron cambios.")
    else:
        print("Receta no encontrada.")

def delete_recipe(coleccion):
    nombre = input("Ingrese el nombre de la receta a eliminar: ")
    result = coleccion.delete_one({'nombre': nombre})
    if result.deleted_count > 0:
        print("Receta eliminada con éxito.")
    else:
        print("Receta no encontrada.")

def list_recipes(coleccion):
    count = coleccion.count_documents({})
    if count > 0:
        for receta in coleccion.find():
            print(receta)
    else:
        print("No hay recetas en la base de datos.")

def search_recipe(coleccion):
    nombre = input("Ingrese el nombre de la receta para buscar: ")
    receta = coleccion.find_one({'nombre': nombre})
    if receta:
        print(f"Receta encontrada: {receta}")
    else:
        print("Receta no encontrada.")

def main():
    coleccion = connect_to_mongo()

    while True:
        print("\nOpciones:")
        print("a) Agregar nueva receta")
        print("c) Actualizar receta existente")
        print("d) Eliminar receta existente")
        print("e) Ver listado de recetas")
        print("f) Buscar ingredientes y pasos de receta")
        print("g) Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == 'a':
            add_recipe(coleccion)
        elif opcion == 'c':
            update_recipe(coleccion)
        elif opcion == 'd':
            delete_recipe(coleccion)
        elif opcion == 'e':
            list_recipes(coleccion)
        elif opcion == 'f':
            search_recipe(coleccion)
        elif opcion == 'g':
            print("Saliendo...")
            break
        else:
            print("Opción no válida, intente de nuevo.")

if __name__ == "__main__":
    main()
