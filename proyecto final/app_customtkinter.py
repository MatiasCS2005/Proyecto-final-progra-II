
import customtkinter as ctk
from tkinter import messagebox, ttk
from database import get_session
from crud.ingrediente_crud import *
from crud.cliente_crud import *
from crud.menu_crud import *
from crud.pedido_crud import *
from database import get_session, engine, Base

ctk.set_appearance_mode("dark")  # "light" or "dark"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

Base.metadata.create_all(bind=engine)

class RestaurantApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gestión de Restaurante")
        self.geometry("1000x700")
        
        # Crear el Tabview (pestañas)
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(pady=20, padx=20, fill="both", expand=True)

        # Pestaña de Ingrediente
        self.tab_Ingredientes = self.tabview.add("Ingredientes")
        self.crear_formulario_ingrediente(self.tab_Ingredientes)
        
        # Pestaña de Menu
        self.tab_Menu = self.tabview.add("Menu")
        self.crear_formulario_menu(self.tab_Menu)
        
        # Pestaña de Clientes
        self.tab_clientes = self.tabview.add("Clientes")
        self.crear_formulario_cliente(self.tab_clientes)

        # Pestaña de Pedidos
        self.tab_pedidos = self.tabview.add("Pedidos")
        self.crear_formulario_pedidos(self.tab_pedidos)
        
        # Revisar el cambio de pestaña periódicamente
        self.current_tab = self.tabview.get()  # Almacena la pestaña actual
        self.after(500, self.check_tab_change)  # Llama a check_tab_change cada 500 ms

    def check_tab_change(self):
        """Revisa si la pestaña activa cambió a 'Pedidos'."""
        new_tab = self.tabview.get()
        if new_tab != self.current_tab:
            self.current_tab = new_tab
            if new_tab == "Pedidos":
                self.actualizar_emails_combobox()
        self.after(500, self.check_tab_change)  # Vuelve a revisar cada 500 ms
    
    
    def crear_formulario_ingrediente(self, parent):
        
        frame_superior = ctk.CTkFrame(parent)
        frame_superior.pack(pady=10, padx=10, fill="x")
        
        ctk.CTkLabel(frame_superior, text="Nombre").grid(row=0, column=0, pady=10, padx=10)
        self.entry_nombre_ingrediente = ctk.CTkEntry(frame_superior)
        self.entry_nombre_ingrediente.grid(row=0, column=1, pady=10, padx=10)

        ctk.CTkLabel(frame_superior, text="Tipo").grid(row=0, column=2, pady=10, padx=10)
        self.entry_tipo = ctk.CTkEntry(frame_superior)
        self.entry_tipo.grid(row=0, column=3, pady=10, padx=10)
        
        ctk.CTkLabel(frame_superior, text="Cantidad").grid(row=0, column=4, pady=10, padx=10)
        self.entry_cantidad = ctk.CTkEntry(frame_superior)
        self.entry_cantidad.grid(row=0, column=5, pady=10, padx=10)

        ctk.CTkLabel(frame_superior, text="Unidad").grid(row=0, column=6, pady=10, padx=10)
        self.entry_unidad = ctk.CTkEntry(frame_superior)
        self.entry_unidad.grid(row=0, column=7, pady=10, padx=10)
        
        # Botones alineados horizontalmente en el frame superior
        self.btn_crear_ingrediente = ctk.CTkButton(frame_superior, text="Ingresar Ingrediente", command=self.crear_ingrediente)
        self.btn_crear_ingrediente.grid(row=1, column=0, pady=10, padx=10)

        self.btn_actualizar_ingrediente = ctk.CTkButton(frame_superior, text="Actualizar Ingrediente", command=self.actualizar_ingrediente)
        self.btn_actualizar_ingrediente.grid(row=1, column=1, pady=10, padx=10)

        self.btn_eliminar_ingrediente = ctk.CTkButton(frame_superior, text="Eliminar Ingrediente", command=self.eliminar_ingrediente)
        self.btn_eliminar_ingrediente.grid(row=1, column=2, pady=10, padx=10)
        
        # Frame inferior para el Treeview
        frame_inferior = ctk.CTkFrame(parent)
        frame_inferior.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Treeview para mostrar los Ingredientes
        self.treeview_ingredientes = ttk.Treeview(frame_inferior, columns=("ID", "Nombre", "Tipo", "Cantidad", "Unidad"), show="headings")
        self.treeview_ingredientes.heading("ID", text="ID")
        self.treeview_ingredientes.heading("Nombre", text="Nombre")
        self.treeview_ingredientes.heading("Tipo", text="Tipo")
        self.treeview_ingredientes.heading("Cantidad", text="Cantidad")
        self.treeview_ingredientes.heading("Unidad", text="Unidad")
        self.treeview_ingredientes.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.cargar_Ingredientes()

        

    def crear_formulario_menu(self, parent):
        frame_superior = ctk.CTkFrame(parent)
        frame_superior.pack(pady=10, padx=10, fill="x")

        # Campo Nombre del Menú
        ctk.CTkLabel(frame_superior, text="Nombre").grid(row=0, column=0, pady=10, padx=10)
        self.entry_menu_nombre = ctk.CTkEntry(frame_superior)
        self.entry_menu_nombre.grid(row=0, column=1, pady=10, padx=10)

        # Campo Descripción
        ctk.CTkLabel(frame_superior, text="Descripción").grid(row=0, column=2, pady=10, padx=10)
        self.entry_menu_descripcion = ctk.CTkEntry(frame_superior)
        self.entry_menu_descripcion.grid(row=0, column=3, pady=10, padx=10)

        # Botones
        self.btn_crear_menu = ctk.CTkButton(frame_superior, text="Crear Menú", command=self.crear_menu)
        self.btn_crear_menu.grid(row=1, column=0, pady=10, padx=10)

        self.btn_actualizar_menu = ctk.CTkButton(frame_superior, text="Actualizar Menú", command=self.actualizar_menu)
        self.btn_actualizar_menu.grid(row=1, column=1, pady=10, padx=10)

        self.btn_eliminar_menu = ctk.CTkButton(frame_superior, text="Eliminar Menú", command=self.eliminar_menu)
        self.btn_eliminar_menu.grid(row=1, column=2, pady=10, padx=10)

        # Frame inferior para el Treeview
        frame_inferior = ctk.CTkFrame(parent)
        frame_inferior.pack(pady=10, padx=10, fill="both", expand=True)

        # Treeview para mostrar los Menús
        self.treeview_menus = ttk.Treeview(frame_inferior, columns=("ID", "Nombre", "Descripción"), show="headings")
        self.treeview_menus.heading("ID", text="ID")
        self.treeview_menus.heading("Nombre", text="Nombre")
        self.treeview_menus.heading("Descripción", text="Descripción")
        self.treeview_menus.pack(pady=10, padx=10, fill="both", expand=True)

        self.cargar_menus()

        

    def crear_formulario_cliente(self, parent):
        """Crea el formulario en el Frame superior y el Treeview en el Frame inferior para la gestión de clientes."""
        # Frame superior para el formulario y botones
        frame_superior = ctk.CTkFrame(parent)
        frame_superior.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(frame_superior, text="Nombre").grid(row=0, column=0, pady=10, padx=10)
        self.entry_nombre = ctk.CTkEntry(frame_superior)
        self.entry_nombre.grid(row=0, column=1, pady=10, padx=10)

        ctk.CTkLabel(frame_superior, text="Email").grid(row=0, column=2, pady=10, padx=10)
        self.entry_email = ctk.CTkEntry(frame_superior)
        self.entry_email.grid(row=0, column=3, pady=10, padx=10)

        # Botones alineados horizontalmente en el frame superior
        self.btn_crear_cliente = ctk.CTkButton(frame_superior, text="Crear Cliente", command=self.crear_cliente)
        self.btn_crear_cliente.grid(row=1, column=0, pady=10, padx=10)

        self.btn_actualizar_cliente = ctk.CTkButton(frame_superior, text="Actualizar Cliente", command=self.actualizar_cliente)
        self.btn_actualizar_cliente.grid(row=1, column=1, pady=10, padx=10)

        self.btn_eliminar_cliente = ctk.CTkButton(frame_superior, text="Eliminar Cliente", command=self.eliminar_cliente)
        self.btn_eliminar_cliente.grid(row=1, column=2, pady=10, padx=10)

        # Frame inferior para el Treeview
        frame_inferior = ctk.CTkFrame(parent)
        frame_inferior.pack(pady=10, padx=10, fill="both", expand=True)

        # Treeview para mostrar los clientes
        self.treeview_clientes = ttk.Treeview(frame_inferior, columns=("ID","Email", "Nombre"), show="headings")
        self.treeview_clientes.heading("ID", text="ID")
        self.treeview_clientes.heading("Email", text="Email")
        self.treeview_clientes.heading("Nombre", text="Nombre")
        self.treeview_clientes.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.cargar_clientes()

    def crear_formulario_pedidos(self, parent):
        """Crea el formulario en el Frame superior y el Treeview en el Frame inferior para la gestión de pedidos."""
        # Frame superior para el formulario y botones
        frame_superior = ctk.CTkFrame(parent)
        frame_superior.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(frame_superior, text="Cliente Email").grid(row=0, column=0, pady=10, padx=10)
        
        # Combobox para seleccionar el email del cliente
        self.combobox_cliente_email = ttk.Combobox(frame_superior, state="readonly")
        self.combobox_cliente_email.grid(row=0, column=1, pady=10, padx=10)
        self.actualizar_emails_combobox()  # Llenar el combobox con emails de los clientes

        ctk.CTkLabel(frame_superior, text="Descripción").grid(row=0, column=2, pady=10, padx=10)
        self.entry_descripcion = ctk.CTkEntry(frame_superior)
        self.entry_descripcion.grid(row=0, column=3, pady=10, padx=10)

        # Botones alineados horizontalmente en el frame superior
        self.btn_crear_pedido = ctk.CTkButton(frame_superior, text="Crear Pedido", command=self.crear_pedido)
        self.btn_crear_pedido.grid(row=1, column=0, pady=10, padx=10)

        self.btn_actualizar_pedido = ctk.CTkButton(frame_superior, text="Actualizar Pedido", command=self.actualizar_pedido)
        self.btn_actualizar_pedido.grid(row=1, column=1, pady=10, padx=10)

        self.btn_eliminar_pedido = ctk.CTkButton(frame_superior, text="Eliminar Pedido", command=self.eliminar_pedido)
        self.btn_eliminar_pedido.grid(row=1, column=2, pady=10, padx=10)

        # Frame inferior para el Treeview
        frame_inferior = ctk.CTkFrame(parent)
        frame_inferior.pack(pady=10, padx=10, fill="both", expand=True)

        # Treeview para mostrar los pedidos
        self.treeview_pedidos = ttk.Treeview(frame_inferior, columns=("ID", "Cliente Email", "Descripción"), show="headings")
        self.treeview_pedidos.heading("ID", text="ID")
        self.treeview_pedidos.heading("Cliente Email", text="Cliente Email")
        self.treeview_pedidos.heading("Descripción", text="Descripción")
        self.treeview_pedidos.pack(pady=10, padx=10, fill="both", expand=True)

        self.cargar_pedidos()

    #def crear_formulario_graficos(self):
     #   tab = self.notebook.add("Gráficos")

        # Widgets for Graficos
      #  label = ctk.CTkLabel(tab, text="Gráficos Estadísticos", font=ctk.CTkFont(size=18, weight="bold"))
       # label.pack(pady=10)

        # Example: Add more widgets as needed

    # Método para actualizar los correos electrónicos en el Combobox
    
    def cargar_Ingredientes(self):
        db = next(get_session())
        self.treeview_ingredientes.delete(*self.treeview_ingredientes.get_children())
        ingredientes = IngredienteCRUD.leer_ingredientes(db)
        for ingrediente in ingredientes:
            self.treeview_ingredientes.insert("", "end", values=(ingrediente.id,ingrediente.nombre, ingrediente.tipo, ingrediente.cantidad, ingrediente.unidad))
        db.close()
    
    def crear_ingrediente(self):
        nombre = self.entry_nombre_ingrediente.get()
        tipo = self.entry_tipo.get()
        cantidad = self.entry_cantidad.get()
        unidad = self.entry_unidad.get()
        if nombre and tipo and cantidad and unidad:
            try:
                cantidad = float(cantidad)
                if cantidad <= 0:
                    messagebox.showwarning("Error", "La cantidad debe ser un número positivo.")
                    return
            except ValueError:
                messagebox.showwarning("Error", "La cantidad debe ser un número válido.")
                return
            
            db = next(get_session())
            ingrediente = IngredienteCRUD.crear_ingrediente(db, nombre, tipo, cantidad, unidad)
            
            if ingrediente:
                messagebox.showinfo("Éxito", "Cliente creado correctamente.")
                self.cargar_Ingredientes()
            else:
                messagebox.showwarning("Error", "El cliente ya existe.")
            db.close()  
        else:
            messagebox.showwarning("Campos Vacíos", "Por favor, ingrese todos los campos.")
                
    def actualizar_ingrediente(self):
        selected_item = self.treeview_ingredientes.selection()
        if not selected_item:
            messagebox.showwarning("Selección", "Por favor, seleccione un ingrediente.")
            return
        nombre = self.entry_nombre_ingrediente.get()
        tipo = self.entry_tipo.get()
        cantidad = self.entry_cantidad.get()
        unidad = self.entry_unidad.get()
        
        if not nombre.strip():
            messagebox.showwarning("Campo Vacío", "Por favor, ingrese un nombre.")
            return
        if not tipo.strip():
            messagebox.showwarning("Campo Vacío", "Por favor, ingrese un email.")
            return
        if not cantidad.strip():
            messagebox.showwarning("Campo Vacío", "Por favor, ingrese un email.")
            return
        if not unidad.strip():
            messagebox.showwarning("Campo Vacío", "Por favor, ingrese un email.")
            return
        ingrediente_id = self.treeview_ingredientes.item(selected_item)["values"][0]
        db = next(get_session())
        ingrediente_actualizado = IngredienteCRUD.actualizar_ingrediente(db, ingrediente_id, nombre, tipo, cantidad, unidad)
        
        if ingrediente_actualizado:
            messagebox.showinfo("Éxito", "Ingrediente actualizado correctamente.")
            self.cargar_Ingredientes()  # Recargar los ingredientes
        else:
            messagebox.showwarning("Error", "No se pudo actualizar el ingrediente.")
    
        db.close()
                
    def eliminar_ingrediente(self):
        selected_item = self.treeview_ingredientes.selection()
        if not selected_item:
            messagebox.showwarning("Selección", "Por favor, seleccione un ingrediente.")
            return
        ingrediente_id = self.treeview_ingredientes.item(selected_item)["values"][0]
        
        db = next(get_session())
        eliminado = IngredienteCRUD.borrar_ingrediente(db, ingrediente_id)  
        if eliminado:
            messagebox.showinfo("Éxito", "ingrediente eliminado correctamente.")
            self.cargar_Ingredientes()
        else:
            messagebox.showwarning("Error", "No se pudo eliminar el ingrediente. Verifique el ID.")
        db.close() 
    
    
    def actualizar_emails_combobox(self):
        """Llena el Combobox con los emails de los clientes."""
        db = next(get_session())
        emails = [cliente.email for cliente in ClienteCRUD.leer_clientes(db)]
        self.combobox_cliente_email['values'] = emails
        db.close()

    # Métodos CRUD para Clientes
    def cargar_clientes(self):
        db = next(get_session())
        self.treeview_clientes.delete(*self.treeview_clientes.get_children())
        clientes = ClienteCRUD.leer_clientes(db)
        for cliente in clientes:
            self.treeview_clientes.insert("", "end", values=(cliente.id, cliente.email, cliente.nombre))
        db.close()

    def crear_cliente(self):
        nombre = self.entry_nombre.get()
        email = self.entry_email.get()
        if nombre and email:
            db = next(get_session())
            cliente = ClienteCRUD.crear_cliente(db, nombre, email)
            if cliente:
                messagebox.showinfo("Éxito", "Cliente creado correctamente.")
                self.cargar_clientes()
                self.actualizar_emails_combobox()  # Actualizar el Combobox con el nuevo email
            else:
                messagebox.showwarning("Error", "El cliente ya existe.")
            db.close()
        else:
            messagebox.showwarning("Campos Vacíos", "Por favor, ingrese todos los campos.")

    def actualizar_cliente(self):
        selected_item = self.treeview_clientes.selection()
        if not selected_item:
            messagebox.showwarning("Selección", "Por favor, seleccione un cliente.")
            return
        nombre = self.entry_nombre.get()
        email = self.entry_email.get()
        if not nombre.strip():
            messagebox.showwarning("Campo Vacío", "Por favor, ingrese un nombre.")
            return
        if not email.strip():
            messagebox.showwarning("Campo Vacío", "Por favor, ingrese un email.")
            return
        
        cliente_id = self.treeview_clientes.item(selected_item)["values"][0]
        
        
        db = next(get_session())
        cliente_actualizado = ClienteCRUD.actualizar_cliente(db, cliente_id, nombre, email)
    
        # Mensajes de éxito o error
        if cliente_actualizado:
            messagebox.showinfo("Éxito", "Cliente actualizado correctamente.")
            self.cargar_clientes()  # Recargar los clientes
        else:
            messagebox.showwarning("Error", "No se pudo actualizar el cliente.")
    
        db.close()
    
    def eliminar_cliente(self):
        selected_item = self.treeview_clientes.selection()
        if not selected_item:
            messagebox.showwarning("Selección", "Por favor, seleccione un cliente.")
            return
        email = self.treeview_clientes.item(selected_item)["values"][1]
        db = next(get_session())
        ClienteCRUD.borrar_cliente(db, email)
        messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
        self.cargar_clientes()
        self.actualizar_emails_combobox()  # Actualizar el Combobox después de eliminar
        db.close()

    # Métodos CRUD para Pedidos
    def cargar_pedidos(self):
        db = next(get_session())
        self.treeview_pedidos.delete(*self.treeview_pedidos.get_children())
        pedidos = PedidoCRUD.leer_pedidos(db)
        for pedido in pedidos:
            self.treeview_pedidos.insert("", "end", values=(pedido.id, pedido.cliente_email, pedido.descripcion))
        db.close()

    def crear_pedido(self):
        cliente_email = self.combobox_cliente_email.get()
        descripcion = self.entry_descripcion.get()
        if cliente_email and descripcion:
            db = next(get_session())
            try:
                # Llamar al CRUD con cliente_email
                pedido = PedidoCRUD.crear_pedido(db, cliente_email, descripcion)
                if pedido:
                    messagebox.showinfo("Éxito", "Pedido creado correctamente.")
                    self.cargar_pedidos()
                else:
                    messagebox.showwarning("Error", "El cliente no existe o no se pudo crear el pedido.")
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error: {e}")
            finally:
                db.close()
        else:
            messagebox.showwarning("Campos Vacíos", "Por favor, ingrese todos los campos.")

    def actualizar_pedido(self):
        selected_item = self.treeview_pedidos.selection()
        if not selected_item:
            messagebox.showwarning("Selección", "Por favor, seleccione un pedido.")
            return
        pedido_id = self.treeview_pedidos.item(selected_item)["values"][0]
        descripcion = self.entry_descripcion.get()
        if descripcion:
            db = next(get_session())
            pedido_actualizado = PedidoCRUD.actualizar_pedido(db, pedido_id, descripcion)
            if pedido_actualizado:
                messagebox.showinfo("Éxito", "Pedido actualizado correctamente.")
                self.cargar_pedidos()
            else:
                messagebox.showwarning("Error", "No se pudo actualizar el pedido.")
            db.close()
        else:
            messagebox.showwarning("Campos Vacíos", "Por favor, ingrese la descripción.")

    def eliminar_pedido(self):
        selected_item = self.treeview_pedidos.selection()
        if not selected_item:
            messagebox.showwarning("Selección", "Por favor, seleccione un pedido.")
            return
        pedido_id = self.treeview_pedidos.item(selected_item)["values"][0]
        db = next(get_session())
        PedidoCRUD.borrar_pedido(db, pedido_id)
        messagebox.showinfo("Éxito", "Pedido eliminado correctamente.")
        self.cargar_pedidos()
        db.close()

    def cargar_menus(self):
        db = next(get_session())
        try:
            self.treeview_menus.delete(*self.treeview_menus.get_children())  # Limpia el Treeview
            menus = MenuCRUD.leer_menus(db)
            for menu in menus:
                self.treeview_menus.insert("", "end", values=(menu.id, menu.nombre, menu.descripcion))
        finally:
            db.close()

    def crear_menu(self):
        nombre = self.entry_menu_nombre.get().strip()
        descripcion = self.entry_menu_descripcion.get().strip()

        if not nombre or not descripcion:
            messagebox.showwarning("Campos Vacíos", "Por favor, ingrese todos los campos.")
            return

        db = next(get_session())
        try:
            nuevo_menu = MenuCRUD.crear_menu(db, nombre, descripcion, [])
            if nuevo_menu:
                messagebox.showinfo("Éxito", "Menú creado correctamente.")
                self.cargar_menus()  # Refrescar el Treeview
            else:
                messagebox.showerror("Error", "No se pudo crear el menú.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar el menú: {e}")
        finally:
            db.close()


    def actualizar_menu(self):
        selected_item = self.treeview_menus.selection()
        if not selected_item:
            messagebox.showwarning("Selección", "Por favor, seleccione un menú.")
            return

        menu_id = self.treeview_menus.item(selected_item)["values"][0]
        nombre = self.entry_menu_nombre.get().strip()
        descripcion = self.entry_menu_descripcion.get().strip()

        if not nombre or not descripcion:
            messagebox.showwarning("Campos Vacíos", "Por favor, ingrese todos los campos.")
            return

        db = next(get_session())
        try:
            menu_actualizado = MenuCRUD.actualizar_menu(db, menu_id, nombre, descripcion, [])
            if menu_actualizado:
                messagebox.showinfo("Éxito", "Menú actualizado correctamente.")
                self.cargar_menus()  # Actualiza el Treeview con los cambios
            else:
                messagebox.showwarning("Error", "No se pudo actualizar el menú.")
        finally:
            db.close()


    def eliminar_menu(self):
        selected_item = self.treeview_menus.selection()
        if not selected_item:
            messagebox.showwarning("Selección", "Por favor, seleccione un menú.")
            return

        menu_id = self.treeview_menus.item(selected_item)["values"][0]

        db = next(get_session())
        try:
            if MenuCRUD.borrar_menu(db, menu_id):
                messagebox.showinfo("Éxito", "Menú eliminado correctamente.")
                self.cargar_menus()  # Actualiza el Treeview tras la eliminación
            else:
                messagebox.showwarning("Error", "No se pudo eliminar el menú.")
        finally:
            db.close()
    


if __name__ == "__main__":
    app = RestaurantApp()
    app.mainloop()
