from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import Ingrediente

class IngredienteCRUD:
    @staticmethod
    def crear_ingrediente(db: Session, nombre: str, tipo: str, cantidad: float, unidad: str):
        """
        Crea un nuevo ingrediente. Evita duplicados por nombre y tipo.
        """
        # Verificar si ya existe un ingrediente con el mismo nombre y tipo
        ingrediente_existente = db.query(Ingrediente).filter(Ingrediente.nombre == nombre, Ingrediente.tipo == tipo).first()
        if ingrediente_existente:
            print(f"El ingrediente {nombre} de tipo {tipo} ya existe en la base de datos.")
            return None  # Si el ingrediente ya existe, retorna None
        
        try:
            # Si no existe, crea un nuevo ingrediente
            nuevo_ingrediente = Ingrediente(nombre=nombre, tipo=tipo, cantidad=cantidad, unidad=unidad)
            db.add(nuevo_ingrediente)
            db.commit()
            db.refresh(nuevo_ingrediente)
            return nuevo_ingrediente
        except Exception as e:
            db.rollback()
            print(f"Ocurrió un error al intentar crear el ingrediente: {e}")
            return None

    @staticmethod
    def leer_ingredientes(db: Session):
        """
        Retorna todos los ingredientes de la base de datos.
        """
        return db.query(Ingrediente).all()

    @staticmethod
    def leer_ingrediente_por_nombre_y_tipo(db: Session, nombre: str, tipo: str):
        """
        Busca un ingrediente por su nombre y tipo.
        """
        return db.query(Ingrediente).filter(Ingrediente.nombre == nombre, Ingrediente.tipo == tipo).first()

    @staticmethod
    def actualizar_ingrediente(db: Session, ingrediente_id: int, nombre: str = None, tipo: str = None, cantidad: float = None, unidad: str = None):
        """
        Actualiza los atributos de un ingrediente existente.
        """
        ingrediente = db.query(Ingrediente).filter(Ingrediente.id == ingrediente_id).first()
        if not ingrediente:
            print(f"No se encontró el ingrediente con ID: {ingrediente_id}")
            return None
        
        if nombre:
            ingrediente.nombre = nombre
        if tipo:
            ingrediente.tipo = tipo
        if cantidad is not None:
            ingrediente.cantidad = cantidad
        if unidad:
            ingrediente.unidad = unidad
        
        try:
            db.commit()
            db.refresh(ingrediente)
            print(f"Ingrediente actualizado: {ingrediente.nombre}")
            return ingrediente
        except IntegrityError as e:
            db.rollback()
            print(f"Error de integridad al actualizar el ingrediente: {e}")
            return None  # Si hay duplicación, devuelve None
        except Exception as e:
            db.rollback()
            print(f"Ocurrió un error inesperado: {e}")
            return None

    @staticmethod
    def borrar_ingrediente(db: Session, ingrediente_id: int):
        """
        Elimina un ingrediente por su ID.
        """
        ingrediente = db.query(Ingrediente).filter(Ingrediente.id == ingrediente_id).first()
        if ingrediente:
            db.delete(ingrediente)
            db.commit()
            return True
        return False
