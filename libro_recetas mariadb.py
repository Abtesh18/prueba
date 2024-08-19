from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DATABASE_URI = 'mysql+pymysql://root:julio06@localhost/libro_recetas_db'
engine = create_engine(DATABASE_URI)


Base = declarative_base()


class Receta(Base):
    __tablename__ = 'recetas'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    ingredientes = Column(String(500), nullable=False)
    pasos = Column(String(1000), nullable=False)


Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()

def agregar_receta():
    nombre = input("Nombre de la receta: ")
    ingredientes = input("Ingredientes (separados por comas): ")
    pasos = input("Pasos: ")

    nueva_receta = Receta(nombre=nombre, ingredientes=ingredientes, pasos=pasos)
    session.add(nueva_receta)
    session.commit()
    print("Receta agregada con éxito.")

def actualizar_receta():
    id_receta = input("ID de la receta a actualizar: ")
    receta = session.query(Receta).filter_by(id=id_receta).first()

    if receta:
        nombre = input("Nuevo nombre de la receta (dejar vacío si no deseas cambiar): ")
        ingredientes = input("Nuevos ingredientes (separados por comas, dejar vacío si no deseas cambiar): ")
        pasos = input("Nuevos pasos (dejar vacío si no deseas cambiar): ")

        if nombre:
            receta.nombre = nombre
        if ingredientes:
            receta.ingredientes = ingredientes
        if pasos:
            receta.pasos = pasos

        session.commit()
        print("Receta actualizada con éxito.")
    else:
        print("Receta no encontrada.")

def eliminar_receta():
    id_receta = input("ID de la receta a eliminar: ")
    receta = session.query(Receta).filter_by(id=id_receta).first()

    if receta:
        session.delete(receta)
        session.commit()
        print("Receta eliminada con éxito.")
    else:
        print("Receta no encontrada.")

def listar_recetas():
    recetas = session.query(Receta).all()
    for receta in recetas:
        print(f"ID: {receta.id}, Nombre: {receta.nombre}")

def buscar_receta():
    nombre_receta = input("Nombre de la receta a buscar: ")
    recetas = session.query(Receta).filter(Receta.nombre.like(f'%{nombre_receta}%')).all()

    if recetas:
        for receta in recetas:
            print(f"ID: {receta.id}, Nombre: {receta.nombre}")
            print(f"Ingredientes: {receta.ingredientes}")
            print(f"Pasos: {receta.pasos}")
            print("--------------------")
    else:
        print("No se encontraron recetas con ese nombre.")

def menu():
    while True:
        print("\nLibro de Recetas")
        print("a) Agregar nueva receta")
        print("b) Actualizar receta existente")
        print("c) Eliminar receta existente")
        print("d) Ver listado de recetas")
        print("e) Buscar ingredientes y pasos de receta")
        print("f) Salir")

        opcion = input("Elige una opción: ")

        if opcion.lower() == 'a':
            agregar_receta()
        elif opcion.lower() == 'b':
            actualizar_receta()
        elif opcion.lower() == 'c':
            eliminar_receta()
        elif opcion.lower() == 'd':
            listar_recetas()
        elif opcion.lower() == 'e':
            buscar_receta()
        elif opcion.lower() == 'f':
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    menu()

    
    session.close()