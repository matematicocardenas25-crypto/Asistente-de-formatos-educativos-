import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from PIL import Image
import io
from datetime import datetime
import easyocr

# --- 1. CONFIGURACIÓN Y ESTILO ---
st.set_page_config(page_title="Asistente Prof. Cárdenas", layout="wide")

st.markdown(
    """
    <style>
    .stApp { background-color: #E3F2FD; }
    .foto-perfil { position: fixed; top: 50px; right: 30px; z-index: 1000; }
    .foto-perfil img { width: 115px; height: 115px; border-radius: 50%; border: 3px solid #1976D2; object-fit: cover; }
    </style>
    <div class="foto-perfil">
        <img src="https://raw.githubusercontent.com/matematicocardenas25-cripto/Asistente-de-formatos-educativos-/main/foto.jpg.jpeg">
    </div>
    """, unsafe_allow_html=True
)

# --- 2. LÓGICA DE CONTENIDO AUTOMÁTICO ---
def generar_conclusiones(unidad):
    return (f"Se desarrolló exitosamente el contenido programado para la unidad de '{unidad}'. "
            "Los estudiantes lograron identificar los fundamentos teóricos y su aplicación práctica. "
            "Se cumplió con la metodología de clase práctica, permitiendo que el estudiante fortalezca su capacidad "
            "de análisis y resolución de problemas reales.")

def generar_recomendaciones(unidad):
    return (f"Se recomienda a los estudiantes revisar la bibliografía básica asignada para profundizar en '{unidad}'. "
            "Es fundamental practicar los ejercicios de la guía de trabajo independiente y consultar dudas en la "
            "siguiente sesión para consolidar el dominio de los instrumentos presentados.")

# --- 3. GENERADOR DE WORD (FORMATO ORIGINAL FIEL) ---
def generar_word_oficial(d):
    doc = Document()
    
    # Estilo global
    style = doc.styles['Normal']
    style.font.name = 'Arial'
    style.font.size = Pt(11)

    # Título Principal
    p_titulo = doc.add_paragraph()
    p_titulo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_titulo.add_run("PROGRAMACIÓN DIDÁCTICA PARA LOS APRENDIZAJES").bold = True

    # I. DATOS GENERALES
    doc.add_heading('I. DATOS GENERALES:', level=1)
    
    p1 = doc.add_paragraph()
    p1.add_run("1.1 Área de conocimiento: ").bold = True
    p1.add_run(f"{d['area']}")

    p2 = doc.add_paragraph()
    p2.add_run("1.2 Carrera: ").bold = True
    p2.add_run(f"{d['carrera']}")
    p2.add_run("    1.3 Modalidad: ").bold = True
    p2.add_run(f"{d['modalidad']}")
    p2.add_run("    Turno: ").bold = True
    p2.add_run("Diurno")

    p3 = doc.add_paragraph()
    p3.add_run("1.4. Nombre de la asignatura: ").bold = True
    p3.add_run(f"{d['asignatura']}")

    p4 = doc.add_paragraph()
    p4.add_run("1.5. Fecha: ").bold = True
    p4.add_run(f"{d['fecha']}")
    p4.add_run("    1.6. Hora: ").bold = True
    p4.add_run("10:30 am – 1:00 pm")

    p5 = doc.add_paragraph()
    p5.add_run("1.7. Profesor (a): ").bold = True
    p5.add_run(f"{d['profesor']}")

    # II. UNIDAD
    doc.add_heading('II. UNIDAD:', level=1)
    doc.add_paragraph(d['unidad'])

    # III. OBJETIVO GENERAL
    doc.add_heading('III. OBJETIVO GENERAL:', level=1)
    doc.add_paragraph("Reconocer diferentes métodos para la recolección y organización de información para la construcción de base de datos mediante técnicas descripticas.")

    # IV. OBJETIVOS ESPECÍFICOS
    doc.add_heading('IV. OBJETIVO(S) ESPECÍFICO(S):', level=1)
    obj_esp = [
        "Definir conceptos básicos de estadística, fuentes de datos para investigación.",
        "Explicar conceptos básicos de estadística y necesidad para realizar una investigación.",
        "Aplicar técnicas de obtención de datos mediante encuesta."
    ]
    for obj in obj_esp:
        doc.add_paragraph(obj, style='List Bullet')

    # V. EVALUACIÓN
    doc.add_heading('V. EVALUACIÓN DE LOS APRENDIZAJES (Criterios y Evidencias):', level=1)
    doc.add_paragraph(d['evaluacion'])

    # VI. ACTIVIDADES (Incluyendo texto de escáner)
    doc.add_heading('VI. ACTIVIDADES DEL DOCENTE Y DE LOS ESTUDIANTES:', level=1)
    doc.add_paragraph(d['actividades'])

    # VII. MEDIOS
    doc.add_heading('VII. MEDIOS O RECURSOS DIDÁCTICOS NECESARIOS:', level=1)
    doc.add_paragraph("Plan de clase, Libro digital, pizarra acrílica, borrador, marcadores.")

    # VIII. CONCLUSIONES (Automáticas)
    doc.add_heading('VIII. CONCLUSIONES', level=1)
    doc.add_paragraph(generar_conclusiones(d['unidad']))

    # IX. RECOMENDACIONES (Automáticas)
    doc.add_heading('IX. RECOMENDACIONES:', level=1)
    doc.add_paragraph(generar_recomendaciones(d['unidad']))

    # X. BIBLIOGRAFIA
    doc.add_heading('X. BIBLIOGRAFIA:', level=1)
    doc.add_paragraph(d['biblio'])

    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf

# --- 4. INTERFAZ ---
tab1, tab2 = st.tabs(["📄 Planificación Didáctica", "📊 Calculadora Multidimensión"])

with tab1:
    st.title("Generador de Formatos Académicos")
    archivo_img = st.file_uploader("📷 Escanear contenido de Actividades", type=['jpg','png','jpeg'])
    texto_escaneado = ""
    if archivo_img:
        reader = easyocr.Reader(['es'])
        texto_escaneado = "\n".join(reader.readtext(np.array(Image.open(archivo_img)), detail=0))

    with st.form("form_doc"):
        c1, c2 = st.columns(2)
        area = c1.text_input("1.1 Área de conocimiento", "Ciencias Económica y Empresariales, Ingeniería y Construcción")
        carrera = c2.text_input("1.2 Carrera", "Todas")
        asignatura = c1.text_input("1.4 Nombre de la asignatura", "Estadística Descriptiva")
        profesor = c2.text_input("1.7 Profesor (a)", "Ismael Antonio Cárdenas López")
        fecha = st.text_input("1.5 Fecha", datetime.now().strftime("%d/%m/%Y"))
        modalidad = "Presencial"
        
        unidad = st.text_area("II. UNIDAD (Tema de la sesión)", "Recopilación de datos. Clase practica 1.")
        evaluacion = st.text_area("V. Evaluación (Criterios)", "Identifique los diferentes tipos de variables. Registro de participación.")
        actividades = st.text_area("VI. Actividades (Cuerpo docente/estudiante)", value=texto_escaneado, height=200)
        biblio = st.text_area("X. Bibliografía", "Saldaña, M. Y. (2024). Principios de Estadística descriptiva. Perú.")
        
        btn_validar = st.form_submit_button("✅ Generar Programación Completa")

    if btn_validar:
        datos_plan = {
            "area": area, "carrera": carrera, "asignatura": asignatura, 
            "profesor": profesor, "fecha": fecha, "modalidad": modalidad,
            "unidad": unidad, "evaluacion": evaluacion, "actividades": actividades, "biblio": biblio
        }
        st.success("¡Documento estructurado correctamente con conclusiones y recomendaciones automáticas!")
        st.download_button("📥 Descargar Word Oficial", generar_word_oficial(datos_plan), f"Programacion_{asignatura}.docx")

with tab2:
    # --- LA CALCULADORA SE MANTIENE SIN CAMBIOS ---
    st.title("📊 Gráficos Trascendentales (Ejes 0,0)")
    dim = st.radio("Dimensión:", ["2D (Plano)", "3D (Espacial)"], horizontal=True)
    
    contexto_mat = {
        "np": np, "x": None, "y": None,
        "sin": np.sin, "cos": np.cos, "tan": np.tan, "exp": np.exp, "log": np.log, "sqrt": np.sqrt
    }

    col_a, col_b = st.columns([1, 2])
    with col_a:
        if dim == "2D (Plano)":
            eq = st.text_input("f(x) =", "sin(x)")
            r = st.slider("Rango", -50, 50, (-10, 10))
        else:
            eq_3d = st.text_input("z = f(x, y)", "x**2 - y**2")
            res = st.slider("Resolución", 5, 20, 10)

    with col_b:
        try:
            if dim == "2D (Plano)":
                x_val = np.linspace(r[0], r[1], 500)
                contexto_mat["x"] = x_val
                y_val = eval(eq, {"__builtins__": None}, contexto_mat)
                fig = go.Figure(go.Scatter(x=x_val, y=y_val, line=dict(color='#1976D2', width=3)))
                fig.update_xaxes(zeroline=True, zerolinewidth=2, zerolinecolor='black')
                fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor='black')
                st.plotly_chart(fig)
            else:
                x = y = np.linspace(-res, res, 100)
                X, Y = np.meshgrid(x, y)
                contexto_mat["x"], contexto_mat["y"] = X, Y
                Z = eval(eq_3d, {"__builtins__": None}, contexto_mat)
                st.plotly_chart(go.Figure(data=[go.Surface(z=Z, x=X, y=Y)]))
        except Exception as e:
            st.error(f"Error matemático: {e}")

    st.info("📸 Usa el icono de la cámara en el gráfico para descargar la imagen.")
