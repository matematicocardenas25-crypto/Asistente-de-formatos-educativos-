import streamlit as st
import easyocr
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from PIL import Image
import numpy as np
import io

# --- DISEÑO ---
st.set_page_config(page_title="Programación Didáctica", layout="wide")

st.markdown(
    """
    <style>
    .stApp { background-color: #E3F2FD; }
    .foto-perfil { position: fixed; top: 50px; right: 30px; z-index: 1000; }
    .foto-perfil img { width: 120px; height: 120px; border-radius: 50%; border: 4px solid #1976D2; object-fit: cover; }
    </style>
    <div class="foto-perfil">
        <img src="https://raw.githubusercontent.com/matematicocardenas25-cripto/Asistente-de-formatos-educativos-/main/foto.jpg.jpeg">
    </div>
    """, unsafe_allow_html=True
)

# --- FUNCIONES ---
def generar_word(d):
    doc = Document()
    t = doc.add_heading('PROGRAMACIÓN DIDÁCTICA PARA LOS APRENDIZAJES', 0)
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # I. DATOS GENERALES 
    doc.add_heading('I. DATOS GENERALES:', level=1)
    doc.add_paragraph(f"1.1 Área de conocimiento: {d['area']}")
    doc.add_paragraph(f"1.2 Carrera: {d['carrera']}   1.3 Modalidad: {d['modalidad']}")
    doc.add_paragraph(f"1.4 Nombre de la asignatura: {d['asignatura']}")
    doc.add_paragraph(f"1.5 Fecha: {d['fecha']}   1.6 Hora: {d['hora']}")
    doc.add_paragraph(f"1.7 Profesor (a): {d['profesor']}")
    
    # II. UNIDAD Y CONTENIDO 
    doc.add_heading('II. UNIDAD:', level=1)
    doc.add_paragraph(d['unidad'])
    doc.add_paragraph(f"2.1 Contenido: \n{d['contenido']}")
    
    # III, IV, V 
    doc.add_heading('III. OBJETIVO GENERAL:', level=1)
    doc.add_paragraph(d['obj_gen'])
    doc.add_heading('IV. OBJETIVO(S) ESPECÍFICO(S):', level=1)
    doc.add_paragraph(d['obj_esp'])
    doc.add_heading('V. EVALUACIÓN DE LOS APRENDIZAJES:', level=1)
    doc.add_paragraph(d['evaluacion'])
    
    # VI, VII, VIII, IX, X 
    doc.add_heading('VI. ACTIVIDADES DEL DOCENTE Y ESTUDIANTES:', level=1)
    doc.add_paragraph(d['actividades'])
    doc.add_heading('VII. MEDIOS O RECURSOS DIDÁCTICOS:', level=1)
    doc.add_paragraph(d['recursos'])
    doc.add_heading('VIII. CONCLUSIONES:', level=1)
    doc.add_paragraph(d['conclusiones'])
    doc.add_heading('IX. RECOMENDACIONES:', level=1)
    doc.add_paragraph(d['recomendaciones'])
    doc.add_heading('X. BIBLIOGRAFIA:', level=1)
    doc.add_paragraph(d['biblio'])

    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf

# --- INTERFAZ ---
st.title("📝 Generador de Programación Didáctica")

img_file = st.file_uploader("Sube imagen para extraer Contenido (OCR)", type=['jpg','png','jpeg'])
texto_ocr = ""
if img_file:
    with st.spinner("Procesando imagen..."):
        reader = easyocr.Reader(['es'])
        texto_ocr = "\n".join(reader.readtext(np.array(Image.open(img_file)), detail=0))

with st.form("main_form"):
    st.subheader("I. Datos Generales")
    col1, col2 = st.columns(2)
    area = col1.text_input("Área de Conocimiento", "Ciencias Económicas e Ingeniería")
    carrera = col2.text_input("Carrera", "Todas")
    asignatura = col1.text_input("Asignatura", "Estadística descriptiva")
    profesor = col2.text_input("Profesor(a)", "Ismael Antonio Cárdenas López")
    modalidad = col1.selectbox("Modalidad", ["Presencial", "Virtual", "Semipresencial"])
    fecha = col2.text_input("Fecha", "22/09/2025")
    hora = col1.text_input("Hora", "10:30 am – 1:00 pm")

    st.subheader("II. Unidad y Contenido")
    unidad = st.text_input("Nombre de la Unidad", "Recopilación de datos")
    contenido = st.text_area("Contenido (OCR)", value=texto_ocr, height=150)

    st.subheader("III, IV y V. Objetivos y Evaluación")
    obj_gen = st.text_area("Objetivo General")
    obj_esp = st.text_area("Objetivos Específicos")
    evaluacion = st.text_area("V. Evaluación (Criterios)")

    st.subheader("VI y VII. Actividades y Recursos")
    actividades = st.text_area("Actividades")
    recursos = st.text_input("Recursos Didácticos", "Plan de clase, Libro, Pizarra")

    st.subheader("Cierre")
    conclusiones = st.text_area("VIII. Conclusiones")
    recomendaciones = st.text_area("IX. Recomendaciones")
    biblio = st.text_area("X. Bibliografía")

    if st.form_submit_button("Generar Plan"):
        datos = {
            'area': area, 'carrera': carrera, 'modalidad': modalidad, 'asignatura': asignatura,
            'fecha': fecha, 'hora': hora, 'profesor': profesor, 'unidad': unidad,
            'contenido': contenido, 'obj_gen': obj_gen, 'obj_esp': obj_esp,
            'evaluacion': evaluacion, 'actividades': actividades, 'recursos': recursos,
            'conclusiones': conclusiones, 'recomendaciones': recomendaciones, 'biblio': biblio
        }
        st.download_button("📥 Descargar Word", generar_word(datos), f"Plan_{asignatura}.docx")
