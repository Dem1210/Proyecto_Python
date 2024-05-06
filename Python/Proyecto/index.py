import os
import re
import tkinter as tk
from tkinter import simpledialog, messagebox

class Usuario:
    def __init__(self, nombre, apellido, correo, telefono):
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.telefono = telefono

class SistemaUsuarios:
    def __init__(self):
        self.usuarios = []
        self.cargar_usuarios()

    def cargar_usuarios(self):
        if os.path.exists('usuarios.txt'):
            with open('usuarios.txt', 'r') as file:
                for line in file:
                    datos = line.strip().split(',')
                    usuario = Usuario(datos[0], datos[1], datos[2], datos[3])
                    self.usuarios.append(usuario)

    def agregar_usuario(self, usuario):
        self.usuarios.append(usuario)
        with open('usuarios.txt', 'a') as file:
            file.write(f"{usuario.nombre},{usuario.apellido},{usuario.correo},{usuario.telefono}\n")

    def listar_usuarios(self):
        return self.usuarios

    def buscar_usuario_por_correo(self, correo):
        for usuario in self.usuarios:
            if usuario.correo == correo:
                return usuario
        return None

    def eliminar_usuario_por_correo(self, correo):
        for usuario in self.usuarios:
            if usuario.correo == correo:
                self.usuarios.remove(usuario)
                self.actualizar_archivo()
                return True
        return False

    def actualizar_archivo(self):
        with open('usuarios.txt', 'w') as file:
            for usuario in self.usuarios:
                file.write(f"{usuario.nombre},{usuario.apellido},{usuario.correo},{usuario.telefono}\n")

class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master=None, placeholder="", *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = 'grey'
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self.config(fg=self.placeholder_color)

    def on_focus_in(self, event):
        if self['fg'] == self.placeholder_color:
            self.delete(0, "end")
            self.config(fg=self.default_fg_color)

    def on_focus_out(self, event):
        if not self.get():
            self.put_placeholder()

class Interfaz(tk.Tk):
    def __init__(self):
        super().__init__()
        self.sistema = SistemaUsuarios()
        self.title("Gestión de Usuarios")
        self.geometry("400x300")
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="Menú")
        self.label.pack()

        self.agregar_btn = tk.Button(
            self, text="Agregar Usuario", command=self.agregar_usuario)
        self.agregar_btn.pack()

        self.listar_btn = tk.Button(
            self, text="Listar Usuarios", command=self.listar_usuarios)
        self.listar_btn.pack()

        self.buscar_btn = tk.Button(
            self, text="Buscar Usuario por Correo", command=self.buscar_usuario)
        self.buscar_btn.pack()

        self.eliminar_btn = tk.Button(
            self, text="Eliminar Usuario por Correo", command=self.eliminar_usuario)
        self.eliminar_btn.pack()

        self.detener_btn = tk.Button(
            self, text="Detener Programa", command=self.destroy)
        self.detener_btn.pack()

    def agregar_usuario(self):
        ventana_agregar = tk.Toplevel(self)
        ventana_agregar.title("Agregar Usuario")

        nombre_label = tk.Label(ventana_agregar, text="Nombre:")
        nombre_label.grid(row=0, column=0)
        self.nombre_entry = EntryWithPlaceholder(ventana_agregar, placeholder="Ej: Juan")
        self.nombre_entry.grid(row=0, column=1)

        apellido_label = tk.Label(ventana_agregar, text="Apellido:")
        apellido_label.grid(row=1, column=0)
        self.apellido_entry = EntryWithPlaceholder(ventana_agregar, placeholder="Ej: Lopez")
        self.apellido_entry.grid(row=1, column=1)

        correo_label = tk.Label(ventana_agregar, text="Correo:")
        correo_label.grid(row=2, column=0)
        self.correo_entry = EntryWithPlaceholder(ventana_agregar, placeholder="Ej: usuario@gmail.com")
        self.correo_entry.grid(row=2, column=1)

        telefono_label = tk.Label(ventana_agregar, text="Teléfono:")
        telefono_label.grid(row=3, column=0)
        self.telefono_entry = EntryWithPlaceholder(ventana_agregar, placeholder="Ej:04121234678")
        self.telefono_entry.grid(row=3, column=1)

        agregar_btn = tk.Button(ventana_agregar, text="Agregar", command=self.guardar_usuario)
        agregar_btn.grid(row=4, columnspan=2)

    def guardar_usuario(self):
        nombre = self.nombre_entry.get()
        apellido = self.apellido_entry.get()
        correo = self.correo_entry.get()
        telefono = self.telefono_entry.get()

        if not self.validar_correo(correo):
            messagebox.showerror("Error", "Dirección de correo no válida.")
            return

        if not self.validar_telefono(telefono):
            messagebox.showerror("Error", "Número de teléfono no válido.")
            return

        if self.sistema.buscar_usuario_por_correo(correo):
            messagebox.showerror("Error", "El correo ya está registrado.")
            return

        nuevo_usuario = Usuario(nombre, apellido, correo, telefono)
        self.sistema.agregar_usuario(nuevo_usuario)
        messagebox.showinfo("Éxito", "Usuario registrado exitosamente.")

    def validar_correo(self, correo):
        return re.match(r"[^@]+@[^@]+\.[^@]+", correo)

    def validar_telefono(self, telefono):
        return telefono.isdigit() and len(telefono) == 10

    def listar_usuarios(self):
        lista_usuarios = "\n".join([f"{usuario.nombre} {usuario.apellido} - {usuario.correo}" for usuario in self.sistema.listar_usuarios()])
        messagebox.showinfo("Lista de Usuarios", lista_usuarios)

    def buscar_usuario(self):
        correo = simpledialog.askstring(
            "Buscar Usuario", "Ingrese el correo del usuario:")
        usuario = self.sistema.buscar_usuario_por_correo(correo)
        if usuario:
            messagebox.showinfo("Usuario Encontrado", f"Nombre: {usuario.nombre}\nApellido: {usuario.apellido}\nCorreo: {usuario.correo}\nTeléfono: {usuario.telefono}")
        else:
            messagebox.showerror("Error", "Usuario no encontrado.")

    def eliminar_usuario(self):
        correo = simpledialog.askstring(
            "Eliminar Usuario", "Ingrese el correo del usuario a eliminar:")
        if self.sistema.eliminar_usuario_por_correo(correo):
            messagebox.showinfo("Éxito", "Usuario eliminado exitosamente.")
        else:
            messagebox.showerror("Error", "Usuario no encontrado.")

if __name__ == "__main__":
    app = Interfaz()
    app.mainloop()
