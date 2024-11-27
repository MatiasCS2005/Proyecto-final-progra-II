from database import get_session, Base, engine
from models import Ingrediente
from crud.ingrediente_crud import IngredienteCRUD

def test_ingrediente_crud():
    Base.metadata.create_all(bind=engine)
    
    session = next(get_session())

    # Verificar si el ingrediente ya existe
    ingrediente = IngredienteCRUD.leer_ingrediente_por_nombre_y_tipo(session, "Tomate", "Vegetal")
    
    if not ingrediente:
        # Crear un ingrediente si no existe
        print("\n--- Crear Ingrediente ---")
        ingrediente = IngredienteCRUD.crear_ingrediente(session, "Tomate", "Vegetal", 10, "kg")
        if ingrediente:
            print(f"Ingrediente creado: {ingrediente}")
        else:
            print("No se pudo crear el ingrediente (posible duplicación).")
    else:
        print(f"El ingrediente {ingrediente.nombre} ya existe en la base de datos.")

    # Leer todos los ingredientes
    print("\n--- Leer Ingredientes ---")
    ingredientes = IngredienteCRUD.leer_ingredientes(session)
    for ing in ingredientes:
        print(f"- {ing}")

    # Actualizar un ingrediente
    if ingrediente:
        print("\n--- Actualizar Ingrediente ---")
        ingrediente_actualizado = IngredienteCRUD.actualizar_ingrediente(session, ingrediente.id, cantidad=15)
        if ingrediente_actualizado:
            print(f"Ingrediente actualizado: {ingrediente_actualizado}")
        else:
            print("No se pudo actualizar el ingrediente.")

        # Borrar un ingrediente
        print("\n--- Borrar Ingrediente ---")
        if IngredienteCRUD.borrar_ingrediente(session, ingrediente.id):
            print(f"Ingrediente con ID {ingrediente.id} eliminado.")
        else:
            print("No se pudo eliminar el ingrediente.")
    else:
        print("No se puede actualizar ni borrar el ingrediente porque no se creó correctamente.")

    session.close()

if __name__ == "__main__":
    test_ingrediente_crud()
