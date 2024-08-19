import sqlite3

def create_connection():
    conn = sqlite3.connect('recetas.db')
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recetas (
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            ingredientes TEXT NOT NULL,
            pasos TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

create_table()


import sqlite3

def create_connection():
    conn = sqlite3.connect('recetas.db')
    return conn

def add_recipe(nombre, ingredientes, pasos):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO recetas (nombre, ingredientes, pasos)
        VALUES (?, ?, ?)
    ''', (nombre, ingredientes, pasos))
    conn.commit()
    conn.close()

def update_recipe(id, nombre, ingredientes, pasos):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE recetas
        SET nombre = ?, ingredientes = ?, pasos = ?
        WHERE id = ?
    ''', (nombre, ingredientes, pasos, id))
    conn.commit()
    conn.close()

def delete_recipe(id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM recetas WHERE id = ?', (id,))
    conn.commit()
    conn.close()

def list_recipes():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM recetas')
    rows = cursor.fetchall()
    conn.close()
    return rows

def search_recipe(term):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM recetas
        WHERE ingredientes LIKE ? OR pasos LIKE ?
    ''', ('%' + term + '%', '%' + term + '%'))
    rows = cursor.fetchall()
    conn.close()
    return rows

def print_menu():
    print("\n--- Menú del Libro de Recetas ---")
    print("a) Agregar nueva receta")
    print("b) Actualizar receta existente")
    print("c) Eliminar receta existente")
    print("d) Ver listado de recetas")
    print("e) Buscar ingredientes y pasos de una receta")
    print("f) Salir")

def main():
    create_table()  
    while True:
        print_menu()
        option = input("Seleccione una opción: ").strip().lower()
        
        if option == 'a':
            nombre = input("Nombre de la receta: ")
            ingredientes = input("Ingredientes (separados por coma): ")
            pasos = input("Pasos: ")
            add_recipe(nombre, ingredientes, pasos)
            print("Receta agregada con éxito.")
        
        elif option == 'b':
            id = int(input("ID de la receta a actualizar: "))
            nombre = input("Nuevo nombre de la receta: ")
            ingredientes = input("Nuevos ingredientes (separados por coma): ")
            pasos = input("Nuevos pasos: ")
            update_recipe(id, nombre, ingredientes, pasos)
            print("Receta actualizada con éxito.")
        
        elif option == 'c':
            id = int(input("ID de la receta a eliminar: "))
            delete_recipe(id)
            print("Receta eliminada con éxito.")
        
        elif option == 'd':
            recipes = list_recipes()
            if recipes:
                for recipe in recipes:
                    print(f"ID: {recipe[0]}, Nombre: {recipe[1]}")
            else:
                print("No hay recetas.")
        
        elif option == 'e':
            term = input("Ingrese el término para buscar: ")
            results = search_recipe(term)
            if results:
                for result in results:
                    print(f"ID: {result[0]}, Nombre: {result[1]}")
                    print(f"Ingredientes: {result[2]}")
                    print(f"Pasos: {result[3]}")
                    print()
            else:
                print("No se encontraron recetas que coincidan.")
        
        elif option == 'f':
            print("Saliendo del programa.")
            break
        
        else:
            print("Opción no válida. Inténtelo de nuevo.")

if __name__ == '__main__':
    main()
