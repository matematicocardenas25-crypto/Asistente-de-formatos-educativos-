import streamlit as st
import easyocr
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from PIL import Image
import numpy as np
import io
from datetime import datetime

# ... (Todo el código inicial de estilo y Word se mantiene exactamente igual) ...

# --- 3. INTERFAZ POR PESTAÑAS ---
tab1, tab2 = st.tabs(["📄 Planificación Didáctica", "📊 Calculadora y Gráficos Multidimensión"])

with tab1:
    # ... (Mantenemos todo el código del Plan de Clase y las descargas Word/LaTeX igual) ...
    st.title("Generador de Programación Didáctica")
    archivo_img = st.file_uploader("📷 Subir imagen para ACTIVIDADES", type=['jpg','png','jpeg'])
    texto_escaneado = ""
    if archivo_img:
        reader = easyocr.Reader(['es'])
        texto_escaneado = "\n".join(reader.readtext(np.array(Image.open(archivo_img)), detail=0))

    with st.form("plan_form"):
        st.subheader("I. Datos Generales")
        c1, c2 = st.columns(2)
        area = c1.text_input("Área de Conocimiento", "Ciencias Económica e Ingeniería")
        carrera = c2.text_input("Carrera", "Todas")
        asignatura = c1.text_input("Asignatura", "Estadística descriptiva")
        profesor = c2.text_input("Profesor(a)", "Ismael Antonio Cárdenas López")
        fecha = c1.text_input("Fecha", value=datetime.now().strftime("%d/%m/%Y"))
        hora = c2.text_input("Hora", "10:30 am – 1:00 pm")
        modalidad = c1.text_input("Modalidad", "Presencial")
        turno = c2.text_input("Turno", "Diurno")

        st.subheader("Planificación y Cierre")
        unidad = st.text_input("II. Unidad", "Recopilación de datos")
        contenido = st.text_area("2.1 Contenido")
        obj_gen = st.text_area("III. Objetivo General")
        obj_esp = st.text_area("IV. Objetivo(s) Específico(s)")
        evaluacion = st.text_area("V. Evaluación (Criterios y Evidencias)")
        actividades = st.text_area("VI. Actividades (Desarrollo)", value=texto_escaneado, height=150)
        recursos = st.text_input("VII. Recursos", "Libro, Pizarra, Guía")
        conclusiones = st.text_area("VIII. Conclusiones")
        recomendaciones = st.text_area("IX. Recomendaciones")
        biblio = st.text_area("X. Bibliografía")
        validar = st.form_submit_button("✅ Procesar Plan")

    if validar:
        datos = {'area': area, 'carrera': carrera, 'modalidad': modalidad, 'turno': turno, 'asignatura': asignatura, 'fecha': fecha, 'hora': hora, 'profesor': profesor, 'unidad': unidad, 'contenido': contenido, 'obj_gen': obj_gen, 'obj_esp': obj_esp, 'evaluacion': evaluacion, 'actividades': actividades, 'recursos': recursos, 'conclusiones': conclusiones, 'recomendaciones': recomendaciones, 'bibliografia': biblio}
        st.success("¡Documentos generados!")
        col_down1, col_down2 = st.columns(2)
        with col_down1:
            st.download_button("📥 Descargar Word", generar_word_oficial(datos), f"Plan_{asignatura}.docx")
        with col_down2:
            latex_code = f"\\section*{{Actividades}}\n{actividades}"
            st.download_button("📥 Descargar LaTeX", latex_code.encode(), f"Plan_{asignatura}.tex")

with tab2:
    st.title("📊 Graficador de Funciones Trascendentales")
    dim = st.radio("Dimensión:", ["2D (Plano)", "3D (Espacial)"], horizontal=True)
    
    # Diccionario para que el usuario pueda escribir 'sin' en lugar de 'np.sin'
    safe_dict = {
        "x": None, "y": None, "np": np,
        "sin": np.sin, "cos": np.cos, "tan": np.tan,
        "arcsin": np.arcsin, "arccos": np.arccos, "arctan": np.arctan,
        "sinh": np.sinh, "cosh": np.cosh, "tanh": np.tanh,
        "exp": np.exp, "log": np.log, "log10": np.log10,
        "sqrt": np.sqrt, "pi": np.pi, "e": np.e
    }

    col_c1, col_c2 = st.columns([1, 2])
    with col_c1:
        st.markdown("**Ejemplos de funciones:**")
        st.code("exp(-x**2), sin(x)/x, log(x), cosh(x)")
        
        if dim == "2D (Plano)":
            f_x = st.text_input("f(x) =", "sin(x)")
            r_x = st.slider("Rango X", -100, 100, (-10, 10))
        else:
            f_z = st.text_input("z = f(x, y)", "sin(sqrt(x**2 + y**2))")
            r_3d = st.slider("Escala", 5, 50, 10)

    with col_c2:
        try:
            if dim == "2D (Plano)":
                x_vals = np.linspace(r_x[0], r_x[1], 1000)
                safe_dict["x"] = x_vals
                y_vals = eval(f_x, {"__builtins__": None}, safe_dict)
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', line=dict(color='#1976D2', width=3)))
                fig.update_xaxes(zeroline=True, zerolinewidth=2, zerolinecolor='Black', showgrid=True)
                fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor='Black', showgrid=True)
                fig.update_layout(title=f"Gráfica 2D: {f_x}", plot_bgcolor='white')
            else:
                x = y = np.linspace(-r_3d, r_3d, 100)
                X, Y = np.meshgrid(x, y)
                safe_dict["x"] = X
                safe_dict["y"] = Y
                Z = eval(f_z, {"__builtins__": None}, safe_dict)
                
                fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Viridis')])
                fig.update_layout(title=f"Superficie 3D: {f_z}")

            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error matemático: {e}. Asegúrate de usar 'x' (y 'y' en 3D).")
