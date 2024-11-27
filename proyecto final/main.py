from database import get_session, Base, engine
from crud.cliente_crud import ClienteCRUD
from crud.ingrediente_crud import IngredienteCRUD
from crud.menu_crud import MenuCRUD
from crud.pedido_crud import PedidoCRUD
from models import Cliente, Ingrediente, Menu, Pedido

def test_pedido_crud(session):
    print("\n--- Probar CRUD de Pedidos ---")

    # Crear un cliente y un menú de prueba
    cliente = ClienteCRUD.crear_cliente(session, "juan@dominio.com", "Juan Perez")
    if cliente:
        print(f"Cliente creado: {cliente.nombre}")

    # Verificar si hay ingredientes, y si no, crear algunos ingredientes
    ingredientes = IngredienteCRUD.leer_ingredientes(session)
    if len(ingredientes) < 1:
        print("No hay ingredientes suficientes, creando algunos ingredientes de prueba...")
        ingrediente1 = IngredienteCRUD.crear_ingrediente(session, "Carne", "Proteína", "kg", 10.0)
        ingrediente2 = IngredienteCRUD.crear_ingrediente(session, "Pan", "Carbohidrato", "unidad", 50.0)
        if ingrediente1 and ingrediente2:
            print("Ingredientes creados: Carne, Pan")

        ingredientes = [ingrediente1, ingrediente2]  # Actualizamos la lista de ingredientes

    # Crear el menú con los ingredientes disponibles
    menu = MenuCRUD.crear_menu(session, "Hamburguesa Completa", "Menú con carne, pan y vegetales", [{"id": ingredientes[0].id, "cantidad": 1.0}, {"id": ingredientes[1].id, "cantidad": 2.0}])
    if menu:
        print(f"Menú creado: {menu.nombre}")

    # Crear un pedido asociado al cliente y al menú
    pedido = PedidoCRUD.crear_pedido(session, "juan@dominio.com", "Pedido con menú completo", "Hamburguesa Completa")
    if pedido:
        print(f"Pedido creado: {pedido.descripcion}, Menú: {pedido.menu_nombre}")

    # Leer pedidos
    pedidos = PedidoCRUD.leer_pedidos(session)
    for p in pedidos:
        print(f"- Pedido: Cliente: {p.cliente_nombre}, Menú: {p.menu_nombre}, Descripción: {p.descripcion}")

    # Actualizar pedido
    if pedido:
        actualizado = PedidoCRUD.actualizar_pedido(session, pedido.id, descripcion="Pedido actualizado")
        if actualizado:
            print(f"Pedido actualizado: {actualizado.descripcion}")

    # Borrar pedido
    if pedido:
        if PedidoCRUD.borrar_pedido(session, pedido.id):
            print(f"Pedido con ID {pedido.id} eliminado.")
