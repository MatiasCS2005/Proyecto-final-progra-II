from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import Cliente

class ClienteCRUD:
    @staticmethod
    def crear_cliente(db: Session, nombre: str, email: str) -> Cliente:
        """
        Crea un nuevo cliente si el correo no existe ya en la base de datos.
        """
        # Verificar si el correo ya existe
        cliente_existente = db.query(Cliente).filter(Cliente.email == email).first()
        if cliente_existente:
            print(f"Cliente con email {email} ya existe.")
            return None  # El cliente ya existe

        # Crear un nuevo cliente
        nuevo_cliente = Cliente(nombre=nombre, email=email)
        db.add(nuevo_cliente)
        db.commit()
        db.refresh(nuevo_cliente)  # Refrescar para obtener la información del cliente creado
        return nuevo_cliente

    @staticmethod
    def leer_clientes(db: Session):
        """Obtiene todos los clientes en la base de datos."""
        return db.query(Cliente).all()

    @staticmethod
    def actualizar_cliente(db: Session, cliente_id: int, nuevo_nombre: str, nuevo_email: str) -> Cliente:
        """
        Actualiza los datos de un cliente existente.
        """
        cliente = db.query(Cliente).filter(Cliente.email == cliente_id).first()
        if not cliente:
            print(f"No se encontró el cliente con ID: {cliente_id}")
            return None  # Cliente no encontrado

        # Actualizar los campos
        cliente.nombre = nuevo_nombre
        cliente.email = nuevo_email
        db.commit()
        db.refresh(cliente)  # Refrescar para obtener los datos actualizados
        return cliente

    @staticmethod
    def borrar_cliente(db: Session, email: str) -> bool:
        """
        Elimina un cliente por su ID.
        """
        cliente = db.query(Cliente).filter(Cliente.email == email).first()
        if not cliente:
            return False  # Cliente no encontrado

        db.delete(cliente)
        db.commit()
        return True
