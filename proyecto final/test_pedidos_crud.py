from database import get_session, Base, engine
from crud.pedido_crud import PedidoCRUD
from crud.cliente_crud import ClienteCRUD

def test_pedido_crud():
    # Crear las tablas en caso de que no existan
    Base.metadata.create_all(bind=engine)

    # Crear una sesión de prueba
    session = next(get_session())

    # Crear un cliente de prueba para asociar pedidos
    cliente = ClienteCRUD.crear_cliente(session, "Carlos López", "carlos.lopez@example.com")
    if cliente:
        print(f"Cliente creado para pedidos: {cliente.nombre} - {cliente.email}")

    # Crear un pedido asociado al cliente
    print("\nCreando pedido...")
    pedido = PedidoCRUD.crear_pedido(session, "carlos.lopez@example.com", "Pedido de prueba")
    if pedido:
        print(f"Pedido creado: {pedido.descripcion}, Cliente ID: {pedido.cliente_id}")
    else:
        print("Fallo al crear el pedido (verifica si el cliente existe).")

    # Leer todos los pedidos
    print("\nLeyendo todos los pedidos...")
    pedidos = PedidoCRUD.leer_pedidos(session)
    for p in pedidos:
        print(f"- ID: {p.id}, Descripción: {p.descripcion}, Cliente ID: {p.cliente_id}")

    # Actualizar un pedido
    if pedido:
        print("\nActualizando pedido...")
        pedido_actualizado = PedidoCRUD.actualizar_pedido(session, pedido.id, "Nuevo pedido actualizado")
        if pedido_actualizado:
            print(f"Pedido actualizado: {pedido_actualizado.descripcion}")
        else:
            print("Fallo al actualizar el pedido.")

    # Borrar el pedido
    if pedido:
        print("\nEliminando pedido...")
        if PedidoCRUD.borrar_pedido(session, pedido.id):
            print(f"Pedido con ID {pedido.id} eliminado.")
        else:
            print("No se pudo eliminar el pedido.")

    # Verificar que no hay pedidos
    print("\nVerificando eliminación...")
    pedidos = PedidoCRUD.leer_pedidos(session)
    if not pedidos:
        print("No hay pedidos en la base de datos.")
    else:
        print("Quedan pedidos en la base de datos.")

    # Cerrar la sesión
    session.close()

if __name__ == "__main__":
    test_pedido_crud()
