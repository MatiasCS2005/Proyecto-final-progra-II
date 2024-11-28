from sqlalchemy import Column, Integer, String, Float, Table, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base

# Modelo Cliente
class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    pedidos = relationship("Pedido", back_populates="cliente", cascade="all, delete")

    def __repr__(self):
        return f"<Cliente(nombre={self.nombre}, email={self.email})>"

# Modelo Pedido
class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String, nullable=False)
    cliente_email = Column(String, ForeignKey('clientes.email', onupdate="CASCADE"), nullable=False)
    cliente = relationship("Cliente", back_populates="pedidos")

    def __repr__(self):
        return f"<Pedido(id={self.id}, descripcion={self.descripcion}, cliente_email={self.cliente_email})>"

# Modelo Ingrediente
class Ingrediente(Base):
    __tablename__ = "ingrediente"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    tipo = Column(String, nullable=False)  # Ejemplo: Vegetal, Proteína
    cantidad = Column(Float, nullable=False, default=0.0)
    unidad = Column(String, nullable=False)  # Ejemplo: "kg", "litros", "unidades"
    
    def __repr__(self):
        return f"{self.nombre}, {self.tipo}, {self.cantidad} {self.unidad}"

    # Evitar duplicados de nombre y tipo
    __table_args__ = (UniqueConstraint("nombre", "tipo", name="unique_nombre_tipo"),)

    # Relación inversa con la tabla Menu (relación many-to-many)
    menus = relationship("Menu", secondary="menu_ingrediente", back_populates="ingredientes")
    
# Tabla intermedia para relacionar Menús e Ingredientes
menu_ingrediente_table = Table(
    "menu_ingrediente",
    Base.metadata,
    Column("menu_id", Integer, ForeignKey("menu.id"), primary_key=True),
    Column("ingrediente_id", Integer, ForeignKey("ingrediente.id"), primary_key=True),
    Column("cantidad", Float, nullable=False)  # Cantidad requerida del ingrediente
)

# Modelo Menu
class Menu(Base):
    __tablename__ = "menu"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)
    descripcion = Column(String(255), nullable=False)

    # Relación con ingredientes
    ingredientes = relationship("Ingrediente", secondary=menu_ingrediente_table, back_populates="menus")

    def __repr__(self):
        return f"<Menu(id={self.id}, nombre={self.nombre}, descripcion={self.descripcion})>"
    
