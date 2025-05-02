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

def calcular_imc(peso_kg, altura_m):
    imc = peso_kg / (altura_m ** 2)
    return imc

def clasificar_imc(imc):
    if imc < 18.5:
        return "Bajo peso", "Aumentar peso con superávit calórico + proteínas."
    elif 18.5 <= imc < 25:
        return "Peso saludable", "Mantenimiento o recomposición corporal (ganar músculo/perder grasa)."
    elif 25 <= imc < 30:
        return "Sobrepeso", "Déficit calórico + ejercicio cardiovascular."
    else:
        return "Obesidad", "Déficit controlado + apoyo profesional."

def calcular_tmb(sexo, peso_kg, altura_cm, edad):
    if sexo.lower() == "masculino":
        tmb = 88.362 + (13.397 * peso_kg) + (4.799 * altura_cm) - (5.677 * edad)
    elif sexo.lower() == "femenino":
        tmb = 447.593 + (9.247 * peso_kg) + (3.098 * altura_cm) - (4.330 * edad)
    else:
        tmb = (88.362 + (13.397 * peso_kg) + (4.799 * altura_cm) - (5.677 * edad) + 447.593 + (9.247 * peso_kg) + (3.098 * altura_cm) - (4.330 * edad)) / 2
    return tmb

def calcular_calorias_diarias(tmb, factor_actividad=1.55):
    return tmb * factor_actividad

def distribucion_macros(objetivo="mantenimiento"):
    if objetivo == "bajar de peso":
        return {"proteinas": 0.30, "grasas": 0.30, "carbohidratos": 0.40}
    elif objetivo == "ganar musculo":
        return {"proteinas": 0.35, "grasas": 0.25, "carbohidratos": 0.40}
    else:
        return {"proteinas": 0.25, "grasas": 0.30, "carbohidratos": 0.45}

def generar_dieta(objetivo, calorias_diarias, macros):
    dietas = {
        "ganar musculo": {
            "Lunes": {
                "desayuno": "Avena con leche entera, plátano y almendras",
                "almuerzo": "Pechuga de pollo con arroz blanco y aguacate",
                "cena": "Carne de res magra con camote y espárragos"
            },
            "Martes": {
                "desayuno": "Huevos revueltos con queso y pan integral",
                "almuerzo": "Salmón a la parrilla con quinoa y brócoli",
                "cena": "Pavo con puré de papa y ensalada de espinacas"
            },
            "Miércoles": {
                "desayuno": "Batido de proteína con avena y mantequilla de maní",
                "almuerzo": "Filete de ternera con arroz integral y calabacín",
                "cena": "Pollo al horno con lentejas y zanahorias"
            },
            "Jueves": {
                "desayuno": "Yogur griego con frutas y nueces",
                "almuerzo": "Atún con pasta integral y espinacas",
                "cena": "Cerdo magro con batata y judías verdes"
            },
            "Viernes": {
                "desayuno": "Tortilla de huevos con jamón y aguacate",
                "almuerzo": "Pollo con couscous y brócoli",
                "cena": "Pescado blanco con arroz salvaje y espárragos"
            },
            "Sábado": {
                "desayuno": "Pan integral con mantequilla de almendra y plátano",
                "almuerzo": "Ternera a la plancha con quinoa y coliflor",
                "cena": "Salmón con puré de camote y ensalada"
            },
            "Domingo": {
                "desayuno": "Avena con proteína en polvo y frutos secos",
                "almuerzo": "Pavo al horno con arroz blanco y vegetales",
                "cena": "Carne magra con patatas asadas y brócoli"
            }
        },
        "bajar de peso": {
            "Lunes": {
                "desayuno": "Claras de huevo con espinacas y tomate",
                "almuerzo": "Ensalada de pollo con lechuga y pepino",
                "cena": "Pescado al vapor con calabacín"
            },
            "Martes": {
                "desayuno": "Yogur natural bajo en grasa con fresas",
                "almuerzo": "Pavo a la plancha con espárragos",
                "cena": "Sopa de verduras sin carbohidratos"
            },
            "Miércoles": {
                "desayuno": "Té verde con tostada integral y queso fresco",
                "almuerzo": "Atún con ensalada verde y limón",
                "cena": "Pollo al horno con brócoli"
            },
            "Jueves": {
                "desayuno": "Batido de espinacas con manzana y semillas de chía",
                "almuerzo": "Salmón a la plancha con judías verdes",
                "cena": "Tortilla de claras con calabacín"
            },
            "Viernes": {
                "desayuno": "Café solo con una rebanada de pan integral",
                "almuerzo": "Ensalada de pavo con rúcula y aguacate",
                "cena": "Pescado blanco con espinacas al vapor"
            },
            "Sábado": {
                "desayuno": "Yogur bajo en grasa con arándanos",
                "almuerzo": "Pollo a la parrilla con coliflor",
                "cena": "Ensalada de atún con pepino y tomate"
            },
            "Domingo": {
                "desayuno": "Té con tostada integral y huevo cocido",
                "almuerzo": "Pavo al horno con brócoli",
                "cena": "Sopa de calabaza baja en calorías"
            }
        },
        "mantenimiento": {
            "Lunes": {
                "desayuno": "Avena con leche descremada y frutas",
                "almuerzo": "Pollo con arroz integral y ensalada",
                "cena": "Pescado blanco con quinoa y espárragos"
            },
            "Martes": {
                "desayuno": "Pan integral con aguacate y huevo",
                "almuerzo": "Pavo con batata y brócoli",
                "cena": "Ensalada de atún con garbanzos"
            },
            "Miércoles": {
                "desayuno": "Yogur griego con miel y nueces",
                "almuerzo": "Salmón con pasta integral y espinacas",
                "cena": "Pollo al horno con calabacín"
            },
            "Jueves": {
                "desayuno": "Batido de proteína con plátano y avena",
                "almuerzo": "Ternera magra con arroz blanco y judías",
                "cena": "Tortilla de huevos con ensalada verde"
            },
            "Viernes": {
                "desayuno": "Tostada integral con queso fresco y tomate",
                "almuerzo": "Pescado con quinoa y coliflor",
                "cena": "Pavo con puré de camote y espinacas"
            },
            "Sábado": {
                "desayuno": "Avena con frutos secos y canela",
                "almuerzo": "Pollo a la plancha con arroz integral y brócoli",
                "cena": "Salmón con ensalada de vegetales"
            },
            "Domingo": {
                "desayuno": "Huevos revueltos con espinacas y pan integral",
                "almuerzo": "Carne magra con batata y zanahorias",
                "cena": "Pescado blanco con arroz salvaje y judías"
            }
        }
    }
    
    dieta_objetivo = dietas.get(objetivo, dietas["mantenimiento"])
    texto_dieta = f"Plan de alimentación para {objetivo} ({calorias_diarias:.0f} kcal diarias):\n\n"
    for dia, comidas in dieta_objetivo.items():
        texto_dieta += f"{dia}:\n"
        for comida, descripcion in comidas.items():
            texto_dieta += f"  - {comida.capitalize()}: {descripcion}\n"
        texto_dieta += "\n"
    return texto_dieta

def generar_rutina(imc):
    if imc < 18.5:
        rutina = """
        Día 1 – Pecho + tríceps
        • 5 min caminata inclinada (nivel 6, velocidad baja)
        • Press banca plano – 4x8
        • Press inclinado con mancuernas – 3x10
        • Aperturas en banco plano – 3x12
        • Fondos o patadas de tríceps – 3x10
        • Rompecráneo con barra o mancuernas – 3x10
        • 5 min caminata inclinada + estiramiento

        Día 2 – Piernas (fuerza)
        • Sentadillas con barra – 4x6
        • Peso muerto rumano – 3x8
        • Prensa de piernas – 3x10
        • Curl femoral – 3x12
        • Elevación de talones (pantorrillas) – 4x15

        Día 3 – Espalda + bíceps
        • Peso muerto – 4x6
        • Remo con barra – 3x8
        • Jalón al pecho – 3x10
        • Curl bíceps con barra – 3x10
        • Curl martillo – 3x12
        • Caminata inclinada suave (5 min)

        Día 4 – Piernas (glúteos + cuadriceps)
        • Zancadas con mancuernas – 3x10 por pierna
        • Sentadilla frontal – 3x8
        • Extensión de piernas – 3x12
        • Hip thrust – 4x10
        • Caminata inclinada (opcional)

        Día 5 – Hombros + core
        • Press militar con barra – 4x8
        • Elevaciones laterales – 3x12
        • Elevaciones frontales – 3x10
        • Encogimientos de hombros – 3x12
        • Plancha + crunch abdominal – 3x30 seg + 20 reps
        """
    elif 18.5 <= imc < 25:
        rutina = """
        Día 1 – Full Body (fuerza)
        • Sentadillas – 4x6
        • Press banca – 4x8
        • Peso muerto – 3x6
        • Remo con barra – 3x8
        • Caminata inclinada – 10 min

        Día 2 – Pierna y glúteos
        • Prensa – 4x10
        • Hip thrust – 3x10
        • Curl femoral – 3x12
        • Zancadas caminando – 3x10 por pierna
        • Elevación de talones – 3x20

        Día 3 – Pecho + tríceps
        • Press inclinado – 4x8
        • Aperturas – 3x12
        • Fondos – 3x10
        • Extensiones de tríceps – 3x10

        Día 4 – Espalda + bíceps
        • Dominadas asistidas – 3x8
        • Jalón al pecho – 3x10
        • Remo – 3x10
        • Curl bíceps alterno – 3x12
        • Caminata inclinada – 10 min

        Día 5 – Hombros + core
        • Press militar – 4x10
        • Elevaciones laterales – 3x12
        • Plancha – 3x30 seg
        • Ab roll-outs o crunches – 3x15
        """
    elif 25 <= imc < 30:
        rutina = """
        Día 1 – Tren inferior
        • Sentadillas con barra – 4x8
        • Prensa – 3x10
        • Curl femoral – 3x12
        • Caminata inclinada – 15 min (moderado)

        Día 2 – Pecho + espalda
        • Superset: Press banca + remo – 3x10 cada uno
        • Superset: Aperturas + jalón al pecho – 3x12 cada uno
        • Core: Crunch + plancha – 3x20 + 30 seg

        Día 3 – Piernas + glúteos
        • Hip thrust – 4x12
        • Sentadilla frontal – 3x10
        • Zancadas – 3x12
        • Elevación de talones – 4x15

        Día 4 – Hombros + brazos
        • Press militar – 3x10
        • Elevaciones laterales – 3x12
        • Curl bíceps + extensión tríceps – 3x12 cada uno
        • Caminata inclinada – 15 min

        Día 5 – Full Body + cardio leve
        • Peso muerto – 3x8
        • Press banca – 3x10
        • Remo – 3x10
        • Caminata inclinada – 15-20 min
        """
    else:
        rutina = """
        Día 1 – Tren inferior (asistido si es necesario)
        • Sentadillas con TRX o banca – 3x10
        • Peso muerto con mancuernas – 3x10
        • Step-ups – 3x10
        • Caminata inclinada – 10 min suave

        Día 2 – Tren superior básico
        • Press con mancuernas sentado – 3x10
        • Jalón al pecho – 3x10
        • Remo en máquina – 3x10
        • Curl bíceps – 3x12

        Día 3 – Piernas y glúteos
        • Prensa – 3x10
        • Hip thrust con banda – 3x12
        • Curl femoral – 3x12
        • Caminata inclinada – 10-15 min

        Día 4 – Full Body liviano
        • Sentadilla con mancuernas – 3x10
        • Press en máquina – 3x10
        • Remo con banda – 3x12
        • Plancha con rodillas apoyadas – 3x20 seg

        Día 5 – Repetición del día con mejor rendimiento + caminata más larga (15-20 min inclinada)
        """
    return rutina.strip()

def crear_pagina_inicial(username, user_id, cambiar_pagina):
    info = obtener_info_personal(user_id)
    if info:
        peso = info["peso"]
        altura = info["altura"]
        imc = calcular_imc(peso, altura)
        clasificacion, _ = clasificar_imc(imc)
        imc_text = ft.Text(f"Tu IMC: {imc:.2f} ({clasificacion})", size=24, color="#FFFFFF", weight="bold", text_align=ft.TextAlign.CENTER)
    else:
        imc_text = ft.Text("Por favor, completa tu información personal para ver tu IMC.", size=18, color="#FFCA28", text_align=ft.TextAlign.CENTER)
    
    rangos_imc = [
        ft.Text("- Bajo peso: IMC < 18.5", size=18, color="#E0F7FA"),
        ft.Text("- Peso saludable: 18.5 ≤ IMC < 25", size=18, color="#E0F7FA"),
        ft.Text("- Sobrepeso: 25 ≤ IMC < 30", size=18, color="#E0F7FA"),
        ft.Text("- Obesidad: IMC ≥ 30", size=18, color="#E0F7FA")
    ]
    
    return ft.Container(
        content=ft.Column(
            [
                ft.Text(f"¡Bienvenido, {username}!", size=40, color="#FFFFFF", weight="bold", text_align=ft.TextAlign.CENTER),
                imc_text,
                ft.Text("Rangos de IMC:", size=20, color="#FFFFFF", weight="bold", text_align=ft.TextAlign.CENTER),
                ft.Column(rangos_imc, alignment=ft.MainAxisAlignment.CENTER),
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
                    on_click=lambda e: cambiar_pagina(0),
                    bgcolor="#FFCA28",
                    color="#1B5E20",
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
                    height=50,
                    width=200
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=25,
            scroll=ft.ScrollMode.AUTO
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

def crear_login_container(page):
    username_field = ft.TextField(
        label="Usuario",
        width=350,
        text_size=16,
        text_style=ft.TextStyle(color="#FFFFFF"),
        label_style=ft.TextStyle(color="#E0F7FA"),
        border_radius=12,
        border_color="#FFCA28",
        focused_border_color="#FFCA28",
        content_padding=15,
        bgcolor=ft.colors.with_opacity(0.1, "#FFFFFF")
    )
    password_field = ft.TextField(
        label="Contraseña",
        width=350,
        text_size=16,
        text_style=ft.TextStyle(color="#FFFFFF"),
        label_style=ft.TextStyle(color="#E0F7FA"),
        border_radius=12,
        border_color="#FFCA28",
        focused_border_color="#FFCA28",
        password=True,
        can_reveal_password=True,
        content_padding=15,
        bgcolor=ft.colors.with_opacity(0.1, "#FFFFFF")
    )
    error_message = ft.Text("", size=16, color="#D32F2F", font_family="Roboto")

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
                ft.Text("NutriMax", size=48, weight="bold", color="#FFFFFF", font_family="Roboto"),
                ft.Text("Tu compañero de salud y fitness", size=20, color="#E0F7FA", font_family="Roboto"),
                username_field,
                password_field,
                error_message,
                ft.Row(
                    [
                        ft.ElevatedButton(
                            "Iniciar Sesión",
                            on_click=login_click,
                            bgcolor="#FFCA28",
                            color="#1B5E20",
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
                            height=50,
                            width=150
                        ),
                        ft.ElevatedButton(
                            "Crear Cuenta",
                            on_click=register_click,
                            bgcolor="#FFCA28",
                            color="#1B5E20",
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
                            height=50,
                            width=150
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=25
        ),
        padding=40,
        border_radius=20,
        bgcolor="#1B5E20",
        width=450,
        shadow=ft.BoxShadow(spread_radius=2, blur_radius=10, color=ft.colors.with_opacity(0.1, "black"), offset=ft.Offset(0, 4)),
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
            colors=["#1B5E20", "#2E7D32"]
        )
    )
    return main_container

def logout(page):
    page.appbar = None  
    page.clean()  
    page.title = "NutriMax - Login"  
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = None  
    login_container = crear_login_container(page)  
    page.add(login_container)  
    page.update()  

def crear_pagina_nutricion(user_id):
    info = obtener_info_personal(user_id)
    if info:
        nombre, altura_m, peso_kg, sexo, edad = info["nombre"], info["altura"], info["peso"], info["sexo"], info["edad"]
        imc = calcular_imc(peso_kg, altura_m)
        clasificacion, recomendacion = clasificar_imc(imc)
        
        altura_cm = altura_m * 100
        tmb = calcular_tmb(sexo, peso_kg, altura_cm, edad)
        calorias_diarias = calcular_calorias_diarias(tmb)
        
        if clasificacion == "Bajo peso":
            objetivo = "ganar musculo"
            calorias_ajustadas = calorias_diarias + 350
        elif clasificacion in ["Sobrepeso", "Obesidad"]:
            objetivo = "bajar de peso"
            calorias_ajustadas = calorias_diarias - 400
        else:
            objetivo = "mantenimiento"
            calorias_ajustadas = calorias_diarias
        
        macros = distribucion_macros(objetivo)
        proteinas = (macros["proteinas"] * calorias_ajustadas) / 4
        grasas = (macros["grasas"] * calorias_ajustadas) / 9
        carbohidratos = (macros["carbohidratos"] * calorias_ajustadas) / 4
        
        texto_dieta = generar_dieta(objetivo, calorias_ajustadas, macros)
        
        texto = f"""
        Hola {nombre},
        
        Tu IMC es {imc:.2f} ({clasificacion}).
        Recomendación: {recomendacion}
        
        Requerimiento calórico diario: {calorias_ajustadas:.0f} kcal ({objetivo}).
        
        Macronutrientes:
        - Proteínas: {proteinas:.0f} g
        - Grasas: {grasas:.0f} g
        - Carbohidratos: {carbohidratos:.0f} g
        
        {texto_dieta}
        """
    else:
        texto = "Por favor, completa tu información personal para recibir recomendaciones."
    return ft.Container(
        content=ft.Column(
            [ft.Text(texto, size=18, color="#262626")],
            scroll=ft.ScrollMode.AUTO,
            expand=True
        ),
        alignment=ft.alignment.center,
        bgcolor="#F5F5F5",
        border_radius=15,
        padding=20,
    )

def crear_pagina_gimnasio(user_id):
    info = obtener_info_personal(user_id)
    if info:
        imc = calcular_imc(info["peso"], info["altura"])
        rutina = generar_rutina(imc)
        texto = f"Tu IMC: {imc:.2f}\nRecomendación:\n{rutina}"
    else:
        texto = "Por favor, completa tu información personal para recibir recomendaciones."
    return ft.Container(
        content=ft.Column(
            controls=[ft.Text(texto, size=18, color="#262626")],
            scroll=ft.ScrollMode.AUTO,
            expand=True
        ),
        alignment=ft.alignment.center,
        bgcolor="#F5F5F5",
        border_radius=15,
        padding=20,
    )

def crear_pagina_perfil(page: ft.Page, user_id):
    info = obtener_info_personal(user_id)
    if info:
        nombre_field = ft.TextField(
            label="Nombre completo",
            value=info["nombre"],
            width=350,
            text_size=16,
            text_style=ft.TextStyle(color="#FFFFFF"),
            label_style=ft.TextStyle(color="#E0F7FA"),
            border_radius=12,
            border_color="#FFCA28",
            focused_border_color="#FFCA28",
            content_padding=15,
            bgcolor=ft.colors.with_opacity(0.1, "#FFFFFF")
        )
        altura_field = ft.TextField(
            label="Altura (m)",
            value=str(info["altura"]),
            width=350,
            keyboard_type=ft.KeyboardType.NUMBER,
            text_size=16,
            text_style=ft.TextStyle(color="#FFFFFF"),
            label_style=ft.TextStyle(color="#E0F7FA"),
            border_radius=12,
            border_color="#FFCA28",
            focused_border_color="#FFCA28",
            content_padding=15,
            bgcolor=ft.colors.with_opacity(0.1, "#FFFFFF")
        )
        peso_field = ft.TextField(
            label="Peso (kg)",
            value=str(info["peso"]),
            width=350,
            keyboard_type=ft.KeyboardType.NUMBER,
            text_size=16,
            text_style=ft.TextStyle(color="#FFFFFF"),
            label_style=ft.TextStyle(color="#E0F7FA"),
            border_radius=12,
            border_color="#FFCA28",
            focused_border_color="#FFCA28",
            content_padding=15,
            bgcolor=ft.colors.with_opacity(0.1, "#FFFFFF")
        )
        sexo_field = ft.Dropdown(
            label="Sexo",
            value=info["sexo"],
            options=[ft.dropdown.Option("Masculino"), ft.dropdown.Option("Femenino"), ft.dropdown.Option("Otro")],
            width=350,
            text_size=16,
            text_style=ft.TextStyle(color="#FFFFFF"),
            label_style=ft.TextStyle(color="#E0F7FA"),
            border_radius=12,
            border_color="#FFCA28",
            focused_border_color="#FFCA28",
            content_padding=15,
            bgcolor=ft.colors.with_opacity(0.1, "#FFFFFF")
        )
        edad_field = ft.TextField(
            label="Edad",
            value=str(info["edad"]),
            width=350,
            keyboard_type=ft.KeyboardType.NUMBER,
            text_size=16,
            text_style=ft.TextStyle(color="#FFFFFF"),
            label_style=ft.TextStyle(color="#E0F7FA"),
            border_radius=12,
            border_color="#FFCA28",
            focused_border_color="#FFCA28",
            content_padding=15,
            bgcolor=ft.colors.with_opacity(0.1, "#FFFFFF")
        )
    else:
        nombre_field = ft.TextField(
            label="Nombre completo",
            width=350,
            text_size=16,
            text_style=ft.TextStyle(color="#FFFFFF"),
            label_style=ft.TextStyle(color="#E0F7FA"),
            border_radius=12,
            border_color="#FFCA28",
            focused_border_color="#FFCA28",
            content_padding=15,
            bgcolor=ft.colors.with_opacity(0.1, "#FFFFFF")
        )
        altura_field = ft.TextField(
            label="Altura (m)",
            width=350,
            keyboard_type=ft.KeyboardType.NUMBER,
            text_size=16,
            text_style=ft.TextStyle(color="#FFFFFF"),
            label_style=ft.TextStyle(color="#E0F7FA"),
            border_radius=12,
            border_color="#FFCA28",
            focused_border_color="#FFCA28",
            content_padding=15,
            bgcolor=ft.colors.with_opacity(0.1, "#FFFFFF")
        )
        peso_field = ft.TextField(
            label="Peso (kg)",
            width=350,
            keyboard_type=ft.KeyboardType.NUMBER,
            text_size=16,
            text_style=ft.TextStyle(color="#FFFFFF"),
            label_style=ft.TextStyle(color="#E0F7FA"),
            border_radius=12,
            border_color="#FFCA28",
            focused_border_color="#FFCA28",
            content_padding=15,
            bgcolor=ft.colors.with_opacity(0.1, "#FFFFFF")
        )
        sexo_field = ft.Dropdown(
            label="Sexo",
            options=[ft.dropdown.Option("Masculino"), ft.dropdown.Option("Femenino"), ft.dropdown.Option("Otro")],
            width=350,
            text_size=16,
            text_style=ft.TextStyle(color="#FFFFFF"),
            label_style=ft.TextStyle(color="#E0F7FA"),
            border_radius=12,
            border_color="#FFCA28",
            focused_border_color="#FFCA28",
            content_padding=15,
            bgcolor=ft.colors.with_opacity(0.1, "#FFFFFF")
        )
        edad_field = ft.TextField(
            label="Edad",
            width=350,
            keyboard_type=ft.KeyboardType.NUMBER,
            text_size=16,
            text_style=ft.TextStyle(color="#FFFFFF"),
            label_style=ft.TextStyle(color="#E0F7FA"),
            border_radius=12,
            border_color="#FFCA28",
            focused_border_color="#FFCA28",
            content_padding=15,
            bgcolor=ft.colors.with_opacity(0.1, "#FFFFFF")
        )

    error_message = ft.Text("", size=16, color="#D32F2F", font_family="Roboto")

    def guardar_cambios(e):
        nombre = nombre_field.value
        altura = altura_field.value
        peso = peso_field.value
        sexo = sexo_field.value
        edad = edad_field.value

        errores = []

        if not nombre:
            errores.append("El nombre no puede estar vacío")
        elif not nombre.replace(" ", "").isalpha():
            errores.append("El nombre solo debe contener letras y espacios")

        try:
            altura = float(altura)
            if altura <= 0:
                errores.append("La altura debe ser un número positivo")
        except ValueError:
            errores.append("La altura debe ser un número")

        try:
            peso = float(peso)
            if peso <= 0:
                errores.append("El peso debe ser un número positivo")
        except ValueError:
            errores.append("El peso debe ser un número")

        if not sexo:
            errores.append("Selecciona un sexo")

        try:
            edad = int(edad)
            if edad <= 0:
                errores.append("La edad debe ser un número entero positivo")
        except ValueError:
            errores.append("La edad debe ser un número entero")

        if errores:
            error_message.value = "\n".join(errores)
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

        error_message.value = "Información actualizada correctamente"
        error_message.color = "#2E7D32"
        page.update()

    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Tu Perfil", size=32, weight="bold", color="#FFFFFF", text_align=ft.TextAlign.CENTER, font_family="Roboto"),
                ft.Text("Actualiza tu información personal para personalizar tu experiencia.", size=18, color="#E0F7FA", text_align=ft.TextAlign.CENTER),
                nombre_field,
                altura_field,
                peso_field,
                sexo_field,
                edad_field,
                error_message,
                ft.ElevatedButton(
                    "Actualizar Perfil",
                    on_click=guardar_cambios,
                    bgcolor="#FFCA28",
                    color="#1B5E20",
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
                    height=50,
                    width=200
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
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

def mostrar_pagina_principal(page: ft.Page, username: str, user_id: int):
    page.clean()

    def cambiar_pagina(index):
        if index == 0:
            contenido_actual.content = crear_pagina_nutricion(user_id)
        elif index == 1:
            contenido_actual.content = crear_pagina_gimnasio(user_id)
        elif index == 2:
            contenido_actual.content = crear_pagina_perfil(page, user_id)
        page.update()

    def mostrar_inicial():
        contenido_actual.content = crear_pagina_inicial(username, user_id, cambiar_pagina)
        page.update()

    contenido_actual = ft.Container(expand=True)
    mostrar_inicial()

    appbar = ft.AppBar(
        title=ft.Container(
            content=ft.Column([
                ft.TextButton(
                    content=ft.Text("NutriMax", size=24, weight="bold", color="white"),
                    on_click=lambda e: mostrar_inicial(),
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
        center_title=True,
        actions=[
            ft.IconButton(
                icon=ft.icons.EXIT_TO_APP,
                icon_color="white",
                on_click=lambda e: logout(page)
            )
        ]
    )

    page.appbar = appbar
    page.bgcolor = "#E0F2E9"
    page.add(contenido_actual)
    page.update()

def mostrar_pantalla_info_personal(page: ft.Page, username: str, user_id: int):
    page.clean()
    page.appbar = None
    page.navigation_bar = None
    nombre_field = ft.TextField(
        label="Nombre completo",
        width=350,
        text_size=16,
        text_style=ft.TextStyle(color="#FFFFFF"),
        label_style=ft.TextStyle(color="#E0F7FA"),
        border_radius=12,
        border_color="#FFCA28",
        focused_border_color="#FFCA28",
        content_padding=15,
        bgcolor=ft.colors.with_opacity(0.1, "#FFFFFF")
    )
    altura_field = ft.TextField(
        label="Altura (m)",
        width=350,
        keyboard_type=ft.KeyboardType.NUMBER,
        text_size=16,
        text_style=ft.TextStyle(color="#FFFFFF"),
        label_style=ft.TextStyle(color="#E0F7FA"),
        border_radius=12,
        border_color="#FFCA28",
        focused_border_color="#FFCA28",
        content_padding=15,
        bgcolor=ft.colors.with_opacity(0.1, "#FFFFFF")
    )
    peso_field = ft.TextField(
        label="Peso (kg)",
        width=350,
        keyboard_type=ft.KeyboardType.NUMBER,
        text_size=16,
        text_style=ft.TextStyle(color="#FFFFFF"),
        label_style=ft.TextStyle(color="#E0F7FA"),
        border_radius=12,
        border_color="#FFCA28",
        focused_border_color="#FFCA28",
        content_padding=15,
        bgcolor=ft.colors.with_opacity(0.1, "#FFFFFF")
    )
    sexo_field = ft.Dropdown(
        label="Sexo",
        width=350,
        options=[ft.dropdown.Option("Masculino"), ft.dropdown.Option("Femenino"), ft.dropdown.Option("Otro")],
        text_size=16,
        text_style=ft.TextStyle(color="#FFFFFF"),
        label_style=ft.TextStyle(color="#E0F7FA"),
        border_radius=12,
        border_color="#FFCA28",
        focused_border_color="#FFCA28",
        content_padding=15,
        bgcolor=ft.colors.with_opacity(0.1, "#FFFFFF")
    )
    edad_field = ft.TextField(
        label="Edad",
        width=350,
        keyboard_type=ft.KeyboardType.NUMBER,
        text_size=16,
        text_style=ft.TextStyle(color="#FFFFFF"),
        label_style=ft.TextStyle(color="#E0F7FA"),
        border_radius=12,
        border_color="#FFCA28",
        focused_border_color="#FFCA28",
        content_padding=15,
        bgcolor=ft.colors.with_opacity(0.1, "#FFFFFF")
    )

    error_message = ft.Text("", size=16, color="#D32F2F", font_family="Roboto")

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

        errores = []

        if not nombre:
            errores.append("El nombre no puede estar vacío")
        elif not nombre.replace(" ", "").isalpha():
            errores.append("El nombre solo debe contener letras y espacios")

        try:
            altura = float(altura)
            if altura <= 0:
                errores.append("La altura debe ser un número positivo")
        except ValueError:
            errores.append("La altura debe ser un número")

        try:
            peso = float(peso)
            if peso <= 0:
                errores.append("El peso debe ser un número positivo")
        except ValueError:
            errores.append("El peso debe ser un número")

        if not sexo:
            errores.append("Selecciona un sexo")

        try:
            edad = int(edad)
            if edad <= 0:
                errores.append("La edad debe ser un número entero positivo")
        except ValueError:
            errores.append("La edad debe ser un número entero")

        if errores:
            error_message.value = "\n".join(errores)
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
            error_message.value = f"Error al guardar la información: {e}"
            page.update()
            return
        finally:
            conn.close()

        page.clean()
        mostrar_pagina_principal(page, username, user_id)

    info_container = ft.Container(
        content=ft.Column(
            [
                ft.Text(f"Bienvenido, {username}!", size=32, color="#FFFFFF", weight="bold", text_align=ft.TextAlign.CENTER, font_family="Roboto"),
                ft.Text("Completa tu información personal para comenzar tu viaje.", size=18, color="#E0F7FA", text_align=ft.TextAlign.CENTER),
                nombre_field,
                altura_field,
                peso_field,
                sexo_field,
                edad_field,
                error_message,
                ft.ElevatedButton(
                    "Guardar Información",
                    on_click=guardar_info,
                    bgcolor="#FFCA28",
                    color="#1B5E20",
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
                    height=50,
                    width=200
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        ),
        padding=40,
        border_radius=20,
        bgcolor="#1B5E20",
        width=450,
        shadow=ft.BoxShadow(spread_radius=10, blur_radius=20, color=ft.colors.with_opacity(0.4, "black"), offset=ft.Offset(0, 8)),
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
            colors=["#1B5E20", "#2E7D32"]
        )
    )

    page.add(info_container)
    page.update()

def main(page: ft.Page):
    page.title = "NutriMax - Login"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    login_container = crear_login_container(page)
    page.add(login_container)
    page.update()

ft.app(target=main)