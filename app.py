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

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Asistente Prof. Cárdenas", layout="wide")

# --- ESTILO Y FOTO ---
st.markdown(
    """
    <style>
    .stApp { background-color: #E3F2FD; }
    .foto-perfil { position: fixed; top: 50px; right: 30px; z-index: 1000; }
    .foto-perfil img { width: 110px; height: 110px; border-radius: 50%; border: 3px solid #1976D2; object-fit: cover; }
    </style>
    <div class="foto-perfil">
        <img src="https://raw.githubusercontent.com/matematicocardenas25-cripto/Asistente-de-formatos-educativos-/main/foto.jpg.jpeg">
    </div>
    """, unsafe_allow_html=True
)

# --- FUNCIÓN GENERAR WORD ---
def generar_word_oficial(d):
    doc = Document()
    style = doc.styles['Normal']
    style.font.name = 'Arial'
    style.font.size = Pt(12)
    
    section = doc.sections[0]
    header = section.header
    header.paragraphs[0].text = "PROGRAMACIÓN DIDÁCTICA PARA LOS APRENDIZAJES"
    header.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_heading('I. DATOS GENERALES:', level=1)
    p = doc.add_paragraph()
    p.add_run(f"1.1 Área: {d['area']}\n1.4 Asignatura: {d['asignatura']}\n1.5 Fecha: {d['fecha']} | 1.7 Profesor: {d['profesor']}")
    
    secciones = [
        ('II. UNIDAD:', d['unidad']), ('2.1. Contenido:', d['contenido']),
        ('III. OBJETIVO GENERAL:', d['obj_gen']), ('IV. OBJETIVO(S) ESPECÍFICO(S):', d['obj_esp']),
        ('V. EVALUACIÓN:', d['evaluacion']), ('VI. ACTIVIDADES:', d['actividades']),
        ('VII. RECURSOS:', d['recursos']), ('VIII. CONCLUSIONES:', d['conclusiones']),
        ('IX. RECOMENDACIONES:', d['recomendaciones']), ('X. BIBLIOGRAFIA:', d['bibliografia'])
    ]
    for tit, cont in secciones:
        doc.add_heading(tit, level=1)
        doc.add_paragraph(cont)
    
    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf

# --- INTERFAZ ---
tab1, tab2 = st.tabs(["📄 Plan de Clase", "📊 Calculadora Multidimensión"])

with tab1:
    st.title("📝 Generador de Planes")
    with st.form("form_plan"):
        area = st.text_input("Área", "Ciencias Económica e Ingeniería")
        asignatura = st.text_input("Asignatura", "Estadística descriptiva")
        profesor = st.text_input("Profesor", "Ismael Antonio Cárdenas López")
        fecha = st.text_input("Fecha", datetime.now().strftime("%d/%m/%Y"))
        unidad = st.text_input("Unidad", "Recopilación de datos")
        contenido = st.text_area("Contenido")
        obj_gen = st.text_area("Objetivo General")
        obj_esp = st.text_area("Objetivos Específicos")
        actividades = st.text_area("Actividades")
        evaluacion = st.text_area("Evaluación")
        conclusiones = st.text_area("Conclusiones")
        recomendaciones = st.text_area("Recomendaciones")
        bibliografia = st.text_area("Bibliografía")
        procesar = st.form_submit_button("✅ Validar Datos")

    if procesar:
        d = locals() # Captura variables del form
        st.success("¡Datos listos!")
        st.download_button("📥 Descargar Word", generar_word_oficial(d), "Plan.docx")

with tab2:
    st.header("📊 Graficador y Calculadora Pro")
    dim = st.radio("Dimensión:", ["2D (Funciones y Estadística)", "3D (Superficies)"], horizontal=True)
    
    if dim == "2D (Funciones y Estadística)":
        tipo = st.selectbox("Tipo:", ["Función Matemática", "Análisis Estadístico"])
        if tipo == "Función Matemática":
            eq = st.text_input("f(x) =", "np.sin(x)")
            x = np.linspace(-10, 10, 400)
            y = eval(eq)
            fig = px.line(x=x, y=y, title=f"Gráfico de {eq}")
            st.plotly_chart(fig)
        else:
            datos_str = st.text_area("Datos (separados por coma):", "15, 20, 15, 30, 25")
            datos = np.array([float(x.strip()) for x in datos_str.split(',')])
            st.write(f"**Media (μ):** {np.mean(datos)} | **Desviación (σ):** {np.std(datos)}")
            st.plotly_chart(px.histogram(datos, title="Histograma de Frecuencias"))
            
    else: # Gráficos 3D
        eq_3d = st.text_input("z = f(x,y)", "np.sin(np.sqrt(x**2 + y**2))")
        x = y = np.linspace(-5, 5, 50)
        X, Y = np.meshgrid(x, y)
        Z = eval(eq_3d, {"np": np, "x": X, "y": Y})
        fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y)])
        st.plotly_chart(fig)

    st.info("💡 Usa el icono de la cámara en el gráfico para descargarlo y pegarlo en tu Word.")
