from sqlalchemy.orm import Session
from models import Pedido, Cliente, Menu
from sqlalchemy.exc import IntegrityError

class PedidoCRUD:
    @staticmethod
    def crear_pedido(db: Session, cliente_email: str, descripcion: str, menu_nombre: str):
        """
        Crea un nuevo pedido en la base de datos.

        :param db: Sesión de la base de datos.
        :param cliente_email: Email del cliente que realiza el pedido.
        :param descripcion: Descripción del pedido.
        :param menu_nombre: Nombre del menú asociado al pedido.
        :return: Pedido creado o None si ocurre un error.
        """
        try:
            # Obtener el cliente por email
            cliente = db.query(Cliente).filter(Cliente.email == cliente_email).first()
            if not cliente:
                raise ValueError(f"Cliente con email {cliente_email} no encontrado")

            # Obtener el menú por nombre
            menu = db.query(Menu).filter(Menu.nombre == menu_nombre).first()
            if not menu:
                raise ValueError(f"Menú con nombre {menu_nombre} no encontrado")

            # Crear el pedido
            pedido = Pedido(cliente_id=cliente.id, descripcion=descripcion, menu_id=menu.id)
            db.add(pedido)
            db.commit()
            db.refresh(pedido)
            return pedido

        except IntegrityError:
            db.rollback()
            return None
        except ValueError as e:
            db.rollback()
            print(e)
            return None

    @staticmethod
    def leer_pedidos(db: Session):
        """
        Obtiene todos los pedidos de la base de datos.

        :param db: Sesión de la base de datos.
        :return: Lista de pedidos.
        """
        return db.query(Pedido).all()

    @staticmethod
    def actualizar_pedido(db: Session, pedido_id: int, descripcion: str = None, menu_nombre: str = None):
        """
        Actualiza los datos de un pedido.

        :param db: Sesión de la base de datos.
        :param pedido_id: ID del pedido a actualizar.
        :param descripcion: Nueva descripción del pedido (opcional).
        :param menu_nombre: Nuevo nombre del menú asociado al pedido (opcional).
        :return: Pedido actualizado o None si ocurre un error.
        """
        try:
            pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
            if not pedido:
                return None

            if descripcion:
                pedido.descripcion = descripcion
            if menu_nombre:
                # Obtener el nuevo menú
                menu = db.query(Menu).filter(Menu.nombre == menu_nombre).first()
                if not menu:
                    raise ValueError(f"Menú con nombre {menu_nombre} no encontrado")
                pedido.menu_id = menu.id

            db.commit()
            db.refresh(pedido)
            return pedido
        except IntegrityError:
            db.rollback()
            return None
        except ValueError as e:
            db.rollback()
            print(e)
            return None

    @staticmethod
    def borrar_pedido(db: Session, pedido_id: int):
        """
        Elimina un pedido de la base de datos.

        :param db: Sesión de la base de datos.
        :param pedido_id: ID del pedido a eliminar.
        :return: True si se eliminó correctamente, False si no.
        """
        try:
            pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
            if not pedido:
                return False
            db.delete(pedido)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(e)
            return False
