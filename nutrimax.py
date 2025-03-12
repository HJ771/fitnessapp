import flet as ft
import sqlite3

def conectar_db():
    conn = sqlite3.connect("nutrimax.db")
    return conn

def registrar_usuario(username, password):
    if not username or not password:
        return "empty"
    username = username.lower()
    conn = conectar_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verificar_login(username, password):
    username = username.lower()
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM usuarios WHERE username = ?", (username,))
    usuario = cursor.fetchone()
    conn.close()
    if usuario:
        return usuario[0] == password
    return None

def main(page: ft.Page):
    page.title = "NutriMax - Login"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#f0f8ff"


    username_field = ft.TextField(
        label="Usuario",
        width=300,
        border_radius=10,
        border_color="#2E7D32",
        focused_border_color="#2E7D32",
        text_size=16,
        content_padding=10,
        text_style=ft.TextStyle(color="#262626"),
        label_style=ft.TextStyle(color="#666666"),
    )

    password_field = ft.TextField(
        label="Contraseña",
        width=300,
        border_radius=10,
        border_color="#2E7D32",
        focused_border_color="#2E7D32",
        password=True,
        can_reveal_password=True,
        text_size=16,
        content_padding=10,
        text_style=ft.TextStyle(color="#262626"),
        label_style=ft.TextStyle(color="#666666"),
    )

    error_message = ft.Text("", size=16, color="#D32F2F")

    def login_click(e):
        username = username_field.value
        password = password_field.value
        if not username or not password:
            page.snack_bar = ft.SnackBar(
                ft.Text("Completa todos los campos", size=16),
                bgcolor="#D32F2F",
                duration=3000
            )
            page.snack_bar.open = True
            page.update()
            return

        resultado = verificar_login(username, password)
        if resultado is None:
            error_message.value = "Usuario no existe"
            page.update()
            return
        elif resultado is False:
            error_message.value = "Contraseña incorrecta"
            page.update()
            return
        else:
            page.clean()
            page.add(
                ft.Column(
                    [
                        ft.Text(f"Bienvenido, {username}!", size=28, color="#2E7D32", weight="bold"),
                        ft.Text("Acceso concedido.", size=18, color="#262626"),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                )
            )
            return

    def register_click(e):
        username = username_field.value
        password = password_field.value
        if not username or not password:
            page.snack_bar = ft.SnackBar(
                ft.Text("Completa todos los campos", size=16),
                bgcolor="#D32F2F",
                duration=3000
            )
        else:
            resultado = registrar_usuario(username, password)
            if resultado == "empty":
                msg = "Completa todos los campos"
                color = "#D32F2F"
            elif resultado is False:
                msg = "Usuario ya existe"
                color = "#D32F2F"
            else:
                msg = "Usuario registrado"
                color = "#388E3C"

            page.snack_bar = ft.SnackBar(
                ft.Text(msg, size=16),
                bgcolor=color,
                duration=3000
            )
        page.snack_bar.open = True
        page.update()

    main_container = ft.Container(
        content=ft.Column(
            [
                ft.Text("NutriMax", size=40, weight="bold", color="#2E7D32"),
                ft.Text("Bienvenido a tu app de nutrición", size=18, color="#262626"),
                username_field,
                password_field,
                error_message,
                ft.Row(
                    [
                        ft.ElevatedButton(
                            "Iniciar Sesión",
                            on_click=login_click,
                            bgcolor="#2E7D32",
                            color="white",
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                            height=50
                        ),
                        ft.ElevatedButton(
                            "Crear Cuenta",
                            on_click=register_click,
                            bgcolor="#FFA000",
                            color="white",
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                            height=50
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        ),
        padding=20,
        border_radius=15,
        bgcolor="white",
        width=400,
        shadow=ft.BoxShadow(
            spread_radius=2,
            blur_radius=10,
            color=ft.Colors.with_opacity(0.1, "black"),
            offset=ft.Offset(0, 4),
        ),
    )

    page.add(main_container)

ft.app(target=main)
