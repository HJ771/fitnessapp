import flet as ft
import sqlite3

def conectar_db():
    conn = sqlite3.connect("nutrimax.db")
    return conn

def registrar_usuario(username, password):
    if not username or not password:
        return {"status": "error", "message": "Completa todos los campos"}
    username = username.lower()
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE username = ?", (username,))
    existe = cursor.fetchone()
    if existe:
        conn.close()
        return {"status": "error", "message": "Este usuario ya existe"}
    try:
        cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return {"status": "success", "message": "Usuario registrado exitosamente"}
    except sqlite3.IntegrityError:
        conn.close()
        return {"status": "error", "message": "Error al registrar el usuario"}

def verificar_login(username, password):
    username = username.lower()
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, password FROM usuarios WHERE username = ?", (username,))
    usuario = cursor.fetchone()
    conn.close()
    if usuario:
        user_id, stored_password = usuario
        if stored_password == password:
            return {"status": "success", "user_id": user_id}
        else:
            return {"status": "error", "message": "Contraseña incorrecta"}
    else:
        return {"status": "error", "message": "Usuario no existe"}

def mostrar_pantalla_info_personal(page: ft.Page, username: str, user_id: int):
    nombre_field = ft.TextField(label="Nombre completo", width=300, text_size=16, text_style=ft.TextStyle(color="#262626"), label_style=ft.TextStyle(color="#666666"), border_radius=10, border_color="#2E7D32", focused_border_color="#2E7D32", content_padding=10)
    altura_field = ft.TextField(label="Altura (pies)", width=300, keyboard_type=ft.KeyboardType.NUMBER, text_size=16, text_style=ft.TextStyle(color="#262626"), label_style=ft.TextStyle(color="#666666"), border_radius=10, border_color="#2E7D32", focused_border_color="#2E7D32", content_padding=10)
    peso_field = ft.TextField(label="Peso (lbs)", width=300, keyboard_type=ft.KeyboardType.NUMBER, text_size=16, text_style=ft.TextStyle(color="#262626"), label_style=ft.TextStyle(color="#666666"), border_radius=10, border_color="#2E7D32", focused_border_color="#2E7D32", content_padding=10)
    sexo_field = ft.Dropdown(label="Sexo", width=300, options=[ft.dropdown.Option("Masculino"), ft.dropdown.Option("Femenino"), ft.dropdown.Option("Otro")], text_size=16, text_style=ft.TextStyle(color="#262626"), label_style=ft.TextStyle(color="#666666"), border_radius=10, border_color="#2E7D32", focused_border_color="#2E7D32", content_padding=10)
    edad_field = ft.TextField(label="Edad", width=300, keyboard_type=ft.KeyboardType.NUMBER, text_size=16, text_style=ft.TextStyle(color="#262626"), label_style=ft.TextStyle(color="#666666"), border_radius=10, border_color="#2E7D32", focused_border_color="#2E7D32", content_padding=10)

    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT nombre_completo, altura, peso, sexo, edad FROM informacion_personal WHERE user_id = ?", (user_id,))
    info = cursor.fetchone()
    conn.close()

    if info:
        nombre_field.value = info[0]
        altura_field.value = str(info[1])
        peso_field.value = str(info[2])
        sexo_field.value = info[3]
        edad_field.value = str(info[4])

    def guardar_info(e):
        nombre = nombre_field.value
        altura = altura_field.value
        peso = peso_field.value
        sexo = sexo_field.value
        edad = edad_field.value

        if not all([nombre, altura, peso, sexo, edad]):
            page.snack_bar = ft.SnackBar(ft.Text("Completa todos los campos", size=16), bgcolor="#D32F2F", duration=3000)
            page.snack_bar.open = True
            page.update()
            return

        try:
            altura = float(altura)
            peso = float(peso)
            edad = int(edad)
        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("Altura, peso y edad deben ser números", size=16), bgcolor="#D32F2F", duration=3000)
            page.snack_bar.open = True
            page.update()
            return

        try:
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM informacion_personal WHERE user_id = ?", (user_id,))
            existe = cursor.fetchone()

            if existe:
                cursor.execute("UPDATE informacion_personal SET nombre_completo = ?, altura = ?, peso = ?, sexo = ?, edad = ? WHERE user_id = ?", (nombre, altura, peso, sexo, edad, user_id))
            else:
                cursor.execute("INSERT INTO informacion_personal (user_id, nombre_completo, altura, peso, sexo, edad) VALUES (?, ?, ?, ?, ?, ?)", (user_id, nombre, altura, peso, sexo, edad))
            conn.commit()
        except sqlite3.Error as e:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error al guardar la información: {e}", size=16), bgcolor="#D32F2F", duration=3000)
            page.snack_bar.open = True
            page.update()
            return
        finally:
            conn.close()

        page.clean()
        exito_container = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Información guardada exitosamente", size=28, color="#2E7D32", weight="bold"),
                    ft.ElevatedButton("Volver", on_click=lambda e: mostrar_pantalla_info_personal(page, username, user_id), bgcolor="#FFA000", color="white", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)), height=50)
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            ),
            padding=20,
            border_radius=15,
            bgcolor="white",
            width=400,
            shadow=ft.BoxShadow(spread_radius=2, blur_radius=10, color=ft.colors.with_opacity(0.1, "black"), offset=ft.Offset(0, 4))
        )
        page.add(exito_container)
        page.update()

    info_container = ft.Container(
        content=ft.Column(
            [
                ft.Text(f"Bienvenido, {username}!", size=28, color="#2E7D32", weight="bold"),
                ft.Text("Por favor, completa tu información personal:", size=18, color="#262626"),
                nombre_field,
                altura_field,
                peso_field,
                sexo_field,
                edad_field,
                ft.ElevatedButton("Guardar", on_click=guardar_info, bgcolor="#2E7D32", color="white", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)), height=50)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        ),
        padding=20,
        border_radius=15,
        bgcolor="white",
        width=400,
        shadow=ft.BoxShadow(spread_radius=2, blur_radius=10, color=ft.colors.with_opacity(0.1, "black"), offset=ft.Offset(0, 4))
    )
    page.add(info_container)
    page.update()

def main(page: ft.Page):    

    page.title = "NutriMax - Login"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#f0f8ff"

    username_field = ft.TextField(label="Usuario", width=300, border_radius=10, border_color="#2E7D32", focused_border_color="#2E7D32", text_size=16, content_padding=10, text_style=ft.TextStyle(color="#262626"), label_style=ft.TextStyle(color="#666666"))
    password_field = ft.TextField(label="Contraseña", width=300, border_radius=10, border_color="#2E7D32", focused_border_color="#2E7D32", password=True, can_reveal_password=True, text_size=16, content_padding=10, text_style=ft.TextStyle(color="#262626"), label_style=ft.TextStyle(color="#666666"))
    error_message = ft.Text("", size=16, color="#D32F2F")

    def login_click(e):
        username = username_field.value
        password = password_field.value

        if not username or not password:
            error_message.value = "Completa todos los campos"
            page.update()
            return

        resultado = verificar_login(username, password)
        if resultado["status"] == "success":
            page.clean()
            mostrar_pantalla_info_personal(page, username, resultado["user_id"])
        else:
            error_message.value = resultado["message"]
            page.update()

    def register_click(e):
        username = username_field.value
        password = password_field.value

        if not username or not password:
            error_message.value = "Completa todos los campos"
            page.update()
            return

        resultado = registrar_usuario(username, password)
        if resultado["status"] == "success":
            error_message.value = resultado["message"]
        else:
            error_message.value = resultado["message"]
        page.update()

    main_container = ft.Container(
        content=ft.Column(
            [
                ft.Text("NutriMax", size=40, weight="bold", color="#2E7D32"),
                ft.Text("Bienvenido a tu app de nutrición y entrenamiento", size=18, color="#262626"),
                username_field,
                password_field,
                error_message,
                ft.Row(
                    [
                        ft.ElevatedButton("Iniciar Sesión", on_click=login_click, bgcolor="#2E7D32", color="white", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)), height=50),
                        ft.ElevatedButton("Crear Cuenta", on_click=register_click, bgcolor="#FFA000", color="white", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)), height=50)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        ),
        padding=20,
        border_radius=15,
        bgcolor="white",
        width=400,
        shadow=ft.BoxShadow(spread_radius=2, blur_radius=10, color=ft.colors.with_opacity(0.1, "black"), offset=ft.Offset(0, 4))
    )
    page.add(main_container)
    page.update()

ft.app(target=main)