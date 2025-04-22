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

def obtener_info_personal(user_id):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT nombre_completo, altura, peso, sexo, edad FROM informacion_personal WHERE user_id = ?", (user_id,))
    info = cursor.fetchone()
    conn.close()
    if info:
        return {
            "nombre": info[0],
            "altura": info[1],
            "peso": info[2],
            "sexo": info[3],
            "edad": info[4]
        }
    else:
        return None

def crear_pagina_inicial(username):
    return ft.Container(
        content=ft.Column(
            [
                ft.Text(f"¡Bienvenido, {username}!", size=40, color="#FFFFFF", weight="bold", text_align=ft.TextAlign.CENTER),
                ft.Text("NutriMax - Tu aliado en salud y bienestar", size=28, color="#FFFFFF", weight="bold", text_align=ft.TextAlign.CENTER, font_family="Roboto"),
                ft.Text(
                    "Descubre planes personalizados de nutrición y entrenamiento diseñados para ti.",
                    size=20,
                    color="#E0F7FA",
                    text_align=ft.TextAlign.CENTER,
                    font_family="Roboto"
                ),
                ft.Text("¿Por qué elegir NutriMax?", size=26, color="#FFFFFF", weight="bold", text_align=ft.TextAlign.CENTER),
                ft.ListView(
                    controls=[
                        ft.Row([ft.Icon(ft.icons.FAVORITE, color="#FFCA28"), ft.Text("- Dietas adaptadas a tus metas.", size=18, color="#E0F7FA")]),
                        ft.Row([ft.Icon(ft.icons.FITNESS_CENTER, color="#FFCA28"), ft.Text("- Rutinas de ejercicio personalizadas.", size=18, color="#E0F7FA")]),
                        ft.Row([ft.Icon(ft.icons.TRENDING_UP, color="#FFCA28"), ft.Text("- Monitoreo de tu progreso en tiempo real.", size=18, color="#E0F7FA")]),
                    ],
                    spacing=15
                ),
                ft.ElevatedButton(
                    "Comienza tu viaje",
                    bgcolor="#FFCA28",
                    color="#1B5E20",
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
                    height=50,
                    width=200
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=25
        ),
        alignment=ft.alignment.center,
        expand=True,
        bgcolor="#1B5E20",
        border_radius=20,
        padding=40,
        shadow=ft.BoxShadow(spread_radius=10, blur_radius=20, color=ft.colors.with_opacity(0.4, "black"), offset=ft.Offset(0, 8)),
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
            colors=["#1B5E20", "#2E7D32"]
        )
    )

def crear_pagina_nutricion(user_id):
    info = obtener_info_personal(user_id)
    if info:
        texto = "Basado en tu información personal, te recomendamos una dieta balanceada adaptada a tus necesidades."
    else:
        texto = "Por favor, completa tu información personal para recibir recomendaciones."
    return ft.Container(
        content=ft.Text(texto, size=18, color="#262626"),
        alignment=ft.alignment.center,
        expand=True,
        bgcolor="#F5F5F5",
        border_radius=15,
        padding=20,
    )

def crear_pagina_gimnasio(user_id):
    info = obtener_info_personal(user_id)
    if info:
        texto = "Basado en tu información personal, te recomendamos una rutina de ejercicios personalizada."
    else:
        texto = "Por favor, completa tu información personal para recibir recomendaciones."
    return ft.Container(
        content=ft.Text(texto, size=18, color="#262626"),
        alignment=ft.alignment.center,
        expand=True,
        bgcolor="#F5F5F5",
        border_radius=15,
        padding=20,
    )

def crear_pagina_perfil(page: ft.Page, user_id):
    info = obtener_info_personal(user_id)
    if info:
        nombre_field = ft.TextField(label="Nombre completo", value=info["nombre"], width=300, text_size=16, text_style=ft.TextStyle(color="#262626"), label_style=ft.TextStyle(color="#666666"), border_radius=10, border_color="#2E7D32", focused_border_color="#2E7D32", content_padding=10)
        altura_field = ft.TextField(label="Altura (pies)", value=str(info["altura"]), width=300, keyboard_type=ft.KeyboardType.NUMBER, text_size=16, text_style=ft.TextStyle(color="#262626"), label_style=ft.TextStyle(color="#666666"), border_radius=10, border_color="#2E7D32", focused_border_color="#2E7D32", content_padding=10)
        peso_field = ft.TextField(label="Peso (lbs)", value=str(info["peso"]), width=300, keyboard_type=ft.KeyboardType.NUMBER, text_size=16, text_style=ft.TextStyle(color="#262626"), label_style=ft.TextStyle(color="#666666"), border_radius=10, border_color="#2E7D32", focused_border_color="#2E7D32", content_padding=10)
        sexo_field = ft.Dropdown(label="Sexo", value=info["sexo"], options=[ft.dropdown.Option("Masculino"), ft.dropdown.Option("Femenino"), ft.dropdown.Option("Otro")], width=300, text_size=16, text_style=ft.TextStyle(color="#262626"), label_style=ft.TextStyle(color="#666666"), border_radius=10, border_color="#2E7D32", focused_border_color="#2E7D32", content_padding=10)
        edad_field = ft.TextField(label="Edad", value=str(info["edad"]), width=300, keyboard_type=ft.KeyboardType.NUMBER, text_size=16, text_style=ft.TextStyle(color="#262626"), label_style=ft.TextStyle(color="#666666"), border_radius=10, border_color="#2E7D32", focused_border_color="#2E7D32", content_padding=10)
    else:
        nombre_field = ft.TextField(label="Nombre completo", width=300, text_size=16, text_style=ft.TextStyle(color="#262626"), label_style=ft.TextStyle(color="#666666"), border_radius=10, border_color="#2E7D32", focused_border_color="#2E7D32", content_padding=10)
        altura_field = ft.TextField(label="Altura (pies)", width=300, keyboard_type=ft.KeyboardType.NUMBER, text_size=16, text_style=ft.TextStyle(color="#262626"), label_style=ft.TextStyle(color="#666666"), border_radius=10, border_color="#2E7D32", focused_border_color="#2E7D32", content_padding=10)
        peso_field = ft.TextField(label="Peso (lbs)", width=300, keyboard_type=ft.KeyboardType.NUMBER, text_size=16, text_style=ft.TextStyle(color="#262626"), label_style=ft.TextStyle(color="#666666"), border_radius=10, border_color="#2E7D32", focused_border_color="#2E7D32", content_padding=10)
        sexo_field = ft.Dropdown(label="Sexo", options=[ft.dropdown.Option("Masculino"), ft.dropdown.Option("Femenino"), ft.dropdown.Option("Otro")], width=300, text_size=16, text_style=ft.TextStyle(color="#262626"), label_style=ft.TextStyle(color="#666666"), border_radius=10, border_color="#2E7D32", focused_border_color="#2E7D32", content_padding=10)
        edad_field = ft.TextField(label="Edad", width=300, keyboard_type=ft.KeyboardType.NUMBER, text_size=16, text_style=ft.TextStyle(color="#262626"), label_style=ft.TextStyle(color="#666666"), border_radius=10, border_color="#2E7D32", focused_border_color="#2E7D32", content_padding=10)
    
    def guardar_cambios(e, page):
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
        
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM informacion_personal WHERE user_id = ?", (user_id,))
        existe = cursor.fetchone()
        
        if existe:
            cursor.execute("UPDATE informacion_personal SET nombre_completo = ?, altura = ?, peso = ?, sexo = ?, edad = ? WHERE user_id = ?", (nombre, altura, peso, sexo, edad, user_id))
        else:
            cursor.execute("INSERT INTO informacion_personal (user_id, nombre_completo, altura, peso, sexo, edad) VALUES (?, ?, ?, ?, ?, ?)", (user_id, nombre, altura, peso, sexo, edad))
        conn.commit()
        conn.close()
        
        page.snack_bar = ft.SnackBar(ft.Text("Información actualizada correctamente", size=16), bgcolor="#2E7D32", duration=3000)
        page.snack_bar.open = True
        page.update()
    
    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Tu Información Personal", size=24, weight="bold", color="#2E7D32"),
                nombre_field,
                altura_field,
                peso_field,
                sexo_field,
                edad_field,
                ft.ElevatedButton("Actualizar", on_click=lambda e: guardar_cambios(e, page), bgcolor="#2E7D32", color="white", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)), height=50)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        ),
        alignment=ft.alignment.center,
        expand=True,
        bgcolor="#F5F5F5",
        border_radius=15,
        padding=20,
    )

def mostrar_pagina_principal(page: ft.Page, username: str, user_id: int):
    page.clean()
    pagina_inicial = crear_pagina_inicial(username)
    pagina_nutricion = crear_pagina_nutricion(user_id)
    pagina_gimnasio = crear_pagina_gimnasio(user_id)
    pagina_perfil = crear_pagina_perfil(page, user_id)
    contenido_actual = ft.Container(content=pagina_inicial, expand=True)
    
    def cambiar_pagina(index):
        if index == 0:
            contenido_actual.content = pagina_nutricion
        elif index == 1:
            contenido_actual.content = pagina_gimnasio
        elif index == 2:
            contenido_actual.content = pagina_perfil
        page.update()
    
    def volver_pagina_inicial(e):
        contenido_actual.content = pagina_inicial
        page.update()
    
    appbar = ft.AppBar(
        title=ft.Container(
            content=ft.Column([
                ft.TextButton(
                    content=ft.Text("NutriMax", size=24, weight="bold", color="white"),
                    on_click=volver_pagina_inicial,
                    style=ft.ButtonStyle(color="white")
                ),
                ft.Row([
                    ft.TextButton(
                        content=ft.Column(
                            [ft.Icon(ft.icons.RESTAURANT), ft.Text("Nutrición")],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=5
                        ),
                        on_click=lambda e: cambiar_pagina(0),
                        style=ft.ButtonStyle(color="white")
                    ),
                    ft.TextButton(
                        content=ft.Column(
                            [ft.Icon(ft.icons.FITNESS_CENTER), ft.Text("Gimnasio")],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=5
                        ),
                        on_click=lambda e: cambiar_pagina(1),
                        style=ft.ButtonStyle(color="white")
                    ),
                    ft.TextButton(
                        content=ft.Column(
                            [ft.Icon(ft.icons.PERSON), ft.Text("Perfil")],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=5
                        ),
                        on_click=lambda e: cambiar_pagina(2),
                        style=ft.ButtonStyle(color="white")
                    )
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=30)
            ], 
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=ft.padding.only(top=10),
        ),
        bgcolor="#2E7D32",
        toolbar_height=120,
        center_title=True
    )
    
    page.appbar = appbar
    page.bgcolor = "#E0F2E9"
    page.add(ft.Container(contenido_actual, expand=True))
    page.update()

def mostrar_pantalla_info_personal(page: ft.Page, username: str, user_id: int):
    page.clean()
    page.appbar = None
    page.navigation_bar = None
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
        mostrar_pagina_principal(page, username, user_id)
    
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
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM informacion_personal WHERE user_id = ?", (resultado["user_id"],))
            info = cursor.fetchone()
            conn.close()
            
            page.clean()
            
            if info:
                mostrar_pagina_principal(page, username, resultado["user_id"])
            else:
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