import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
from crud.cliente_crud import *
from crud.pedido_crud import *
from crud.ingrediente_crud import *
from crud.menu_crud import *
from sqlalchemy.orm import sessionmaker
from database import get_session, engine, Base

Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Gestión de Compras")
        self.geometry("900x600")
        
        # Obtener la sesión para interactuar con la base de datos
        self.session = get_session()

        # Crear Tabview (pestañas)
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)

        # Crear las pestañas
        self.session = SessionLocal()  # Esto asume que estás usando SQLAlchemy
        self.crear_pestaña_clientes()
        self.crear_pestaña_ingredientes()
        self.crear_pestaña_menus()

    ### Pestaña Clientes ###
    def crear_pestaña_clientes(self):
        self.tabview.add("Clientes")
        parent = self.tabview.tab("Clientes")
        self.crear_formulario_y_treeview(parent, "Clientes", self.agregar_cliente, self.actualizar_cliente, self.eliminar_cliente)

    ### Pestaña Ingredientes ###
    def crear_pestaña_ingredientes(self):
        self.tabview.add("Ingredientes")
        parent = self.tabview.tab("Ingredientes")
        self.crear_formulario_y_treeview(parent, "Ingredientes", self.agregar_ingrediente, self.actualizar_ingrediente, self.borrar_ingrediente)

    ### Pestaña Menús ###
    def crear_pestaña_menus(self):
        self.tabview.add("Menús")
        parent = self.tabview.tab("Menús")
        self.crear_formulario_y_treeview(parent, "Menús", self.agregar_menu, self.actualizar_menu, self.eliminar_menu)

    ### Función Genérica para Formulario y Treeview ###
    def crear_formulario_y_treeview(self, parent, entidad, agregar_func, actualizar_func, eliminar_func):
        """Crea un formulario, botones y Treeview genérico para gestionar datos."""
        # Frame superior para formulario y botones
        frame_superior = ctk.CTkFrame(parent)
        frame_superior.pack(padx=10, pady=10, fill="x")

        # Etiqueta y entrada de texto
        ctk.CTkLabel(frame_superior, text=f"{entidad}").grid(row=0, column=0, pady=10, padx=10)
        entry = ctk.CTkEntry(frame_superior)
        entry.grid(row=0, column=1, pady=10, padx=10)

        # Botones CRUD
        ctk.CTkButton(frame_superior, text=f"Añadir {entidad}", command=lambda: agregar_func(entry.get())).grid(row=1, column=0, pady=10, padx=10)
        ctk.CTkButton(frame_superior, text=f"Actualizar {entidad}", command=lambda: actualizar_func(entry.get())).grid(row=1, column=1, pady=10, padx=10)
        ctk.CTkButton(frame_superior, text=f"Eliminar {entidad}", command=lambda: eliminar_func(entry.get())).grid(row=1, column=2, pady=10, padx=10)

        # Frame inferior para Treeview
        frame_inferior = ctk.CTkFrame(parent)
        frame_inferior.pack(padx=10, pady=10, fill="both", expand=True)

        # Treeview
        treeview = ttk.Treeview(frame_inferior, columns=("ID", "Nombre"), show="headings")
        treeview.heading("ID", text="ID")
        treeview.heading("Nombre", text="Nombre")
        treeview.pack(padx=10, pady=10, fill="both", expand=True)

        # Guardar el Treeview en un atributo para usar en las funciones CRUD
        setattr(self, f"treeview_{entidad.lower()}", treeview)

        # Cargar los datos iniciales
        self.cargar_datos_iniciales(treeview, entidad)

    ### Funciones CRUD (Clientes, Ingredientes, Menús) ###
    def cargar_datos_iniciales(self, treeview, entidad):
        """Carga los datos iniciales en el Treeview según la entidad."""
        crud_class = {
            "Clientes": ClienteCRUD,
            "Ingredientes": IngredienteCRUD,
            "Menús": MenuCRUD,
        }.get(entidad)

        if crud_class:
            items = crud_class.leer_clientes(self.session)
            for item in items:
                treeview.insert("", "end", values=(item.id, item.nombre))

    def agregar_cliente(self, nombre):
        try:
            ClienteCRUD.agregar_cliente(self.session, nombre)
            messagebox.showinfo("Éxito", "Cliente agregado.")
            self.actualizar_treeview(self.treeview_clientes, ClienteCRUD)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def actualizar_cliente(self, nombre):
        # Similar a agregar_cliente, pero actualiza un registro
        pass

    def eliminar_cliente(self, nombre):
        # Similar a agregar_cliente, pero elimina un registro
        pass
    
    def actualizar_ingrediente(self):
        pass
    
    def borrar_ingrediente(self):
        pass
    
    def actualizar_menu(self):
        pass
    
    def eliminar_menu(self):
        pass

    def agregar_ingrediente(self, nombre):
        try:
            IngredienteCRUD.agregar_ingrediente(self.session, nombre)
            messagebox.showinfo("Éxito", "Ingrediente agregado.")
            self.actualizar_treeview(self.treeview_ingredientes, IngredienteCRUD)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def agregar_menu(self, nombre):
        try:
            MenuCRUD.agregar_menu(self.session, nombre)
            messagebox.showinfo("Éxito", "Menú agregado.")
            self.actualizar_treeview(self.treeview_menus, MenuCRUD)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def actualizar_treeview(self, treeview, crud_class):
        """Actualiza el Treeview con los datos del CRUD correspondiente."""
        for item in treeview.get_children():
            treeview.delete(item)
        items = crud_class.leer_clientes(self.session)
        for item in items:
            treeview.insert("", "end", values=(item.id, item.nombre))


# Ejecutar la aplicación
if __name__ == "__main__":
    app = App()
    app.mainloop()
