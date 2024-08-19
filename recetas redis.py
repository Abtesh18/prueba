import redis
import json

def connect_to_redis():
    client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
    return client

def add_recipe(client):
    nombre = input("Ingrese el nombre de la receta: ")
    ingredientes = input("Ingrese los ingredientes separados por coma: ").split(',')
    pasos = input("Ingrese los pasos separados por punto y coma: ").split(';')
    
    receta = {
        'nombre': nombre,
        'ingredientes': [i.strip() for i in ingredientes],
        'pasos': [p.strip() for p in pasos if p.strip()] 
    }
    
    # Guardar la receta en Redis
    client.hset('recetas', nombre, json.dumps(receta))
    print("Receta añadida con éxito.")

def update_recipe(client):
    nombre = input("Ingrese el nombre de la receta a actualizar: ")
    receta = client.hget('recetas', nombre)
    
    if receta:
        receta = json.loads(receta)
        print(f"Receta encontrada: {receta}")
        
        nuevo_nombre = input("Ingrese el nuevo nombre de la receta (deje en blanco para no cambiar): ")
        nuevos_ingredientes = input("Ingrese los nuevos ingredientes separados por coma (deje en blanco para no cambiar): ")
        nuevos_pasos = input("Ingrese los nuevos pasos separados por punto y coma (deje en blanco para no cambiar): ")
        
        if nuevo_nombre:
            client.hdel('recetas', nombre)
            nombre = nuevo_nombre
        if nuevos_ingredientes:
            receta['ingredientes'] = [i.strip() for i in nuevos_ingredientes.split(',')]
        if nuevos_pasos:
            receta['pasos'] = [p.strip() for p in nuevos_pasos.split(';') if p.strip()]
        
        client.hset('recetas', nombre, json.dumps(receta))
        print("Receta actualizada con éxito.")
    else:
        print("Receta no encontrada.")

def delete_recipe(client):
    nombre = input("Ingrese el nombre de la receta a eliminar: ")
    if client.hdel('recetas', nombre) > 0:
        print("Receta eliminada con éxito.")
    else:
        print("Receta no encontrada.")

def list_recipes(client):
    recetas = client.hgetall('recetas')
    if recetas:
        for nombre, receta in recetas.items():
            print(f"{nombre}: {json.loads(receta)}")
    else:
        print("No hay recetas en la base de datos.")

def search_recipe(client):
    nombre = input("Ingrese el nombre de la receta para buscar: ")
    receta = client.hget('recetas', nombre)
    if receta:
        print(f"Receta encontrada: {json.loads(receta)}")
    else:
        print("Receta no encontrada.")

def main():
    client = connect_to_redis()

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
            add_recipe(client)
        elif opcion == 'c':
            update_recipe(client)
        elif opcion == 'd':
            delete_recipe(client)
        elif opcion == 'e':
            list_recipes(client)
        elif opcion == 'f':
            search_recipe(client)
        elif opcion == 'g':
            print("Saliendo...")
            break
        else:
            print("Opción no válida, intente de nuevo.")

if __name__ == "__main__":
    main()
