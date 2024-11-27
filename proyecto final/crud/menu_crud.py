from sqlalchemy.orm import Session
from models import Menu, Ingrediente, menu_ingrediente_table  # Asegúrate de importar la tabla intermedia
from sqlalchemy.exc import IntegrityError

class MenuCRUD:
    @staticmethod
    def crear_menu(db: Session, nombre: str, descripcion: str, ingredientes: list[dict]):
        """
        Crea un nuevo menú en la base de datos.

        :param db: Sesión de la base de datos.
        :param nombre: Nombre del menú.
        :param descripcion: Descripción del menú.
        :param ingredientes: Lista de ingredientes con formato:
                             [{"id": 1, "cantidad": 1.0}, {"id": 2, "cantidad": 0.5}]
        :return: Menú creado o None si ocurre un error.
        """
        try:
            # Verificar que todos los ingredientes existen
            ingredientes_objs = []
            for item in ingredientes:
                ingrediente = db.query(Ingrediente).filter(Ingrediente.id == item["id"]).first()
                if not ingrediente:
                    raise ValueError(f"Ingrediente con ID {item['id']} no encontrado")
                ingredientes_objs.append({"ingrediente": ingrediente, "cantidad": item["cantidad"]})

            # Crear el menú
            menu = Menu(nombre=nombre, descripcion=descripcion)
            for ing in ingredientes_objs:
                menu.ingredientes.append(ing["ingrediente"])  # Agregar el ingrediente al menú

            db.add(menu)
            db.commit()
            db.refresh(menu)
            return menu
        except IntegrityError:
            db.rollback()
            return None
        except ValueError as e:
            db.rollback()
            print(e)
            return None

    @staticmethod
    def leer_menus(db: Session):
        """
        Obtiene todos los menús de la base de datos.

        :param db: Sesión de la base de datos.
        :return: Lista de menús.
        """
        return db.query(Menu).all()

    @staticmethod
    def actualizar_menu(db: Session, menu_id: int, nombre: str = None, descripcion: str = None, ingredientes: list[dict] = None):
        """
        Actualiza los datos de un menú.

        :param db: Sesión de la base de datos.
        :param menu_id: ID del menú a actualizar.
        :param nombre: Nuevo nombre del menú (opcional).
        :param descripcion: Nueva descripción del menú (opcional).
        :param ingredientes: Nueva lista de ingredientes (opcional).
        :return: Menú actualizado o None si ocurre un error.
        """
        try:
            menu = db.query(Menu).filter(Menu.id == menu_id).first()
            if not menu:
                return None

            if nombre:
                menu.nombre = nombre
            if descripcion:
                menu.descripcion = descripcion
            if ingredientes is not None:
                # Limpiar ingredientes actuales
                menu.ingredientes.clear()
                for item in ingredientes:
                    ingrediente = db.query(Ingrediente).filter(Ingrediente.id == item["id"]).first()
                    if not ingrediente:
                        raise ValueError(f"Ingrediente con ID {item['id']} no encontrado")
                    menu.ingredientes.append(ingrediente)

            db.commit()
            db.refresh(menu)
            return menu
        except IntegrityError:
            db.rollback()
            return None
        except ValueError as e:
            db.rollback()
            print(e)
            return None

    @staticmethod
    def borrar_menu(db: Session, menu_id: int):
        """
        Elimina un menú de la base de datos.

        :param db: Sesión de la base de datos.
        :param menu_id: ID del menú a eliminar.
        :return: True si se eliminó correctamente, False si no.
        """
        try:
            menu = db.query(Menu).filter(Menu.id == menu_id).first()
            if not menu:
                return False
            db.delete(menu)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(e)
            return False
