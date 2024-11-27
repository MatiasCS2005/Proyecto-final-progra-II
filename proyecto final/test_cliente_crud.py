from database import get_session, Base, engine 
from models import Cliente
from crud.cliente_crud import ClienteCRUD

def test_cliente_crud():
    # Crear tablas en caso de que no existan
    Base.metadata.create_all(bind=engine)

    # Crear una sesión de prueba
    session = next(get_session())

    # 1. Probar creación de cliente
    print("\nProbando creación de cliente...")
    cliente_nuevo = ClienteCRUD.crear_cliente(session, "Juan Pérez", "juan.perez@example.com")
    if cliente_nuevo:
        print(f"Cliente creado exitosamente: {cliente_nuevo.nombre} - {cliente_nuevo.email}")
    else:
        print("Fallo al crear cliente (puede ser que el correo ya exista).")

    # 2. Probar lectura de clientes
    print("\nLeyendo todos los clientes...")
    clientes = ClienteCRUD.leer_clientes(session)
    for cliente in clientes:
        print(f"- {cliente.id}: {cliente.nombre} ({cliente.email})")

    # 3. Probar lectura por ID
    if cliente_nuevo:
        print("\nLeyendo cliente por ID...")
        cliente_por_id = ClienteCRUD.leer_cliente_por_id(session, cliente_nuevo.id)
        if cliente_por_id:
            print(f"Cliente encontrado: {cliente_por_id.nombre} - {cliente_por_id.email}")
        else:
            print("No se encontró cliente con ese ID.")

    # 4. Probar actualización de cliente
    if cliente_nuevo:
        print("\nActualizando cliente...")
        cliente_actualizado = ClienteCRUD.actualizar_cliente(session, cliente_nuevo.id, "Juan Gómez", "juan.gomez@example.com")
        if cliente_actualizado:
            print(f"Cliente actualizado: {cliente_actualizado.nombre} - {cliente_actualizado.email}")
        else:
            print("No se pudo actualizar el cliente.")

    # 5. Probar eliminación de cliente
    if cliente_nuevo:
        print("\nEliminando cliente...")
        cliente_eliminado = ClienteCRUD.borrar_cliente(session, cliente_nuevo.id)
        if cliente_eliminado:
            print(f"Cliente con ID {cliente_nuevo.id} eliminado exitosamente.")
        else:
            print("No se pudo eliminar el cliente.")

    # Verificar que el cliente ha sido eliminado
    print("\nVerificando eliminación...")
    clientes = ClienteCRUD.leer_clientes(session)
    for cliente in clientes:
        print(f"- {cliente.id}: {cliente.nombre} ({cliente.email})")
    if not clientes:
        print("No hay clientes en la base de datos.")

    # Cerrar la sesión
    session.close()

if __name__ == "__main__":
    test_cliente_crud()
