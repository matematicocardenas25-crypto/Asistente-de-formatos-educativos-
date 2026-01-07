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

# --- CONFIGURACIÓN Y ESTILO ---
st.set_page_config(page_title="Asistente Educativo Prof. Cárdenas", layout="wide")

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

# --- FUNCIONES DE GENERACIÓN ---
def generar_word_oficial(d):
    doc = Document()
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Arial'
    font.size = Pt(12)
    
    section = doc.sections[0]
    header = section.header
    header.paragraphs[0].text = "PROGRAMACIÓN DIDÁCTICA PARA LOS APRENDIZAJES"
    header.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_heading('I. DATOS GENERALES:', level=1)
    
    # Datos Generales con formato de puntos
    p1 = doc.add_paragraph()
    p1.add_run("1.1 Área de conocimiento: ").bold = True
    p1.add_run(f"{d['area']} " + "."*30)
    
    p2 = doc.add_paragraph()
    p2.add_run("1.2 Carrera: ").bold = True
    p2.add_run(f"{d['carrera']} " + "."*15 + " 1.3 Modalidad: " + f"{d['modalidad']} " + "."*10)
    
    p3 = doc.add_paragraph()
    p3.add_run("1.4. Nombre de la asignatura: ").bold = True
    p3.add_run(f"{d['asignatura']} " + "."*30)

    p4 = doc.add_paragraph()
    p4.add_run("1.5. Fecha: ").bold = True
    p4.add_run(f"{d['fecha']} " + "."*15 + " 1.6. Hora: " + f"{d['hora']} " + "."*15)

    p5 = doc.add_paragraph()
    p5.add_run("1.7. Profesor (a): ").bold = True
    p5.add_run(f"{d['profesor']} " + "."*30)

    # Resto de secciones (II a X)
    secciones = [
        ('II. UNIDAD:', d['unidad']),
        ('2.1. Contenido:', d['contenido']),
        ('III. OBJETIVO GENERAL:', d['obj_gen']),
        ('IV. OBJETIVO(S) ESPECÍFICO(S):', d['obj_esp']),
        ('V. EVALUACIÓN DE LOS APRENDIZAJES (Criterios y Evidencias):', d['evaluacion']),
        ('VI. ACTIVIDADES DEL DOCENTE Y ESTUDIANTES (Desarrollo):', d['actividades']),
        ('VII. MEDIOS O RECURSOS DIDÁCTICOS NECESARIOS:', d['recursos']),
        ('VIII. CONCLUSIONES:', d['conclusiones']),
        ('IX. RECOMENDACIONES:', d['recomendaciones']),
        ('X. BIBLIOGRAFIA:', d['biblio'])
    ]
    for tit, cont in secciones:
        doc.add_heading(tit, level=1)
        doc.add_paragraph(cont)
    
    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf

# --- INTERFAZ ---
tab1, tab2 = st.tabs(["📄 Planificación", "📊 Graficador y Calculadora"])

with tab1:
    st.title("Generador de Programación Didáctica")
    
    # Escaneo fuera del form para agilidad
    archivo_img = st.file_uploader("📷 Escanear para ACTIVIDADES (Punto VI)", type=['jpg','png','jpeg'])
    texto_escaneado = ""
    if archivo_img:
        reader = easyocr.Reader(['es'])
        texto_escaneado = "\n".join(reader.readtext(np.array(Image.open(archivo_img)), detail=0))

    with st.form("main_form"):
        c1, c2 = st.columns(2)
        area = c1.text_input("Área de Conocimiento", "Ciencias Económica e Ingeniería")
        asignatura = c2.text_input("Asignatura", "Estadística descriptiva")
        profesor = st.text_input("Profesor(a)", "Ismael Antonio Cárdenas López")
        fecha = st.text_input("Fecha", value=datetime.now().strftime("%d/%m/%Y"))
        hora = c1.text_input("Hora", "10:30 am – 1:00 pm")
        carrera = c2.text_input("Carrera", "Todas")
        
        unidad = st.text_input("II. Unidad", "Recopilación de datos")
        contenido = st.text_area("2.1 Contenido")
        obj_gen = st.text_area("III. Objetivo General")
        obj_esp = st.text_area("IV. Objetivo(s) Específico(s)")
        
        # El escaneo cae aquí
        actividades = st.text_area("VI. Actividades (Desarrollo)", value=texto_escaneado, height=200)
        
        evaluacion = st.text_area("V. Evaluación (Criterios y Evidencias)")
        conclusiones = st.text_area("VIII. Conclusiones")
        recomendaciones = st.text_area("IX. Recomendaciones")
        biblio = st.text_area("X. Bibliografía")
        
        # Botón del formulario solo para procesar datos
        procesar = st.form_submit_button("✅ Procesar Datos")

    # BOTONES DE DESCARGA FUERA DEL FORM (Para evitar el error de la imagen)
    if procesar:
        datos = {
            'area': area, 'asignatura': asignatura, 'profesor': profesor, 'fecha': fecha,
            'hora': hora, 'carrera': carrera, 'modalidad': "Presencial", 'turno': "Diurno",
            'unidad': unidad, 'contenido': contenido, 'obj_gen': obj_gen, 'obj_esp': obj_esp,
            'actividades': actividades, 'evaluacion': evaluacion, 'conclusiones conclusiones': conclusiones,
            'recomendaciones': recomendaciones, 'biblio': biblio, 'recursos': "Libro, Pizarra, Guía",
            'bibliografia': biblio
        }
        st.success("¡Datos listos para descargar!")
        col_w, col_l = st.columns(2)
        with col_w:
            st.download_button("📥 Descargar Word", generar_word_oficial(datos), f"Plan_{asignatura}.docx")
        with col_l:
            st.download_button("📥 Descargar LaTeX", f"\\section*{{Actividades}}\n{actividades}".encode(), f"Plan_{asignatura}.tex")

with tab2:
    st.header("📊 Calculadora Gráfica Independiente")
    tipo = st.selectbox("Tipo de Gráfico", ["Barras Estadísticas", "Curva Matemática (y=f(x))"])
    
    if tipo == "Barras Estadísticas":
        val_x = st.text_input("Etiquetas (ej: A, B, C)", "Muestra 1, Muestra 2")
        val_y = st.text_input("Valores (ej: 10, 20)", "15, 25")
        
        x_list = [i.strip() for i in val_x.split(',')]
        y_list = [float(i) for i in val_y.split(',')]
        fig = px.bar(x=x_list, y=y_list, title="Gráfico Estadístico")
        st.plotly_chart(fig)
