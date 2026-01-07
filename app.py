import streamlit as st
import easyocr
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from PIL import Image
import numpy as np
import io
from datetime import datetime

# --- 1. CONFIGURACIÓN Y DISEÑO ---
st.set_page_config(page_title="Asistente de Programación Didáctica", layout="wide")

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

# --- 2. LÓGICA DE AUTO-RELLENADO ---
SUGERENCIAS = {
    "Recopilación de datos": {
        "concl": "El estudiante identifica fuentes de datos y aplica técnicas de recolección con precisión.",
        "recom": "Fomentar el uso de herramientas digitales para tabulación inmediata de datos."
    },
    "Cálculo del tamaño muestral": {
        "concl": "Se logra determinar el tamaño de muestra idóneo garantizando la representatividad estadística.",
        "recom": "Practicar con diferentes niveles de confianza para observar variaciones en la muestra."
    },
    "General / Otro": {
        "concl": "Se cumplieron los objetivos de aprendizaje mediante la participación activa y resolución de problemas.",
        "recom": "Revisar la bibliografía complementaria para profundizar en los conceptos discutidos."
    }
}

# --- 3. FUNCIONES DE GENERACIÓN DE ARCHIVOS ---

def generar_word(d):
    doc = Document()
    titulo = doc.add_heading('PROGRAMACIÓN DIDÁCTICA PARA LOS APRENDIZAJES', 0)
    titulo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # I. DATOS GENERALES
    doc.add_heading('I. DATOS GENERALES:', level=1)
    p = doc.add_paragraph()
    p.add_run(f"1.1 Área: {d['area']}\n1.2 Carrera: {d['carrera']}   1.3 Modalidad: {d['modalidad']}\n1.4 Asignatura: {d['asignatura']}\n1.5 Fecha: {d['fecha']}   1.6 Hora: {d['hora']}\n1.7 Profesor: {d['profesor']}")
    
    # II a X
    secciones = [
        ('II. UNIDAD:', d['unidad']), ('2.1. Contenido:', d['contenido']),
        ('III. OBJETIVO GENERAL:', d['obj_gen']), ('IV. OBJETIVO(S) ESPECÍFICO(S):', d['obj_esp']),
        ('V. EVALUACIÓN:', d['evaluacion']), ('VI. ACTIVIDADES:', d['actividades']),
        ('VII. MEDIOS Y RECURSOS:', d['recursos']), ('VIII. CONCLUSIONES:', d['conclusiones']),
        ('IX. RECOMENDACIONES:', d['recomendaciones']), ('X. BIBLIOGRAFIA:', d['biblio'])
    ]
    for tit, cont in secciones:
        doc.add_heading(tit, level=1)
        doc.add_paragraph(cont)

    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf

def generar_latex(d):
    return f"""
\\documentclass{{article}}
\\usepackage[utf8]{{inputenc}}
\\title{{Programación Didáctica: {d['asignatura']}}}
\\author{{{d['profesor']}}}
\\begin{{document}}
\\maketitle
\\section{{I. Datos Generales}}
Fecha: {d['fecha']} \\\\ Tema: {d['unidad']}
\\section{{II. Contenido}}
{d['contenido']}
\\section{{VIII. Conclusiones}}
{d['conclusiones']}
\\section{{IX. Recomendaciones}}
{d['recomendaciones']}
\\end{{document}}
    """

# --- 4. INTERFAZ ---
st.title("📝 Generador Pro: Word + LaTeX + OCR")

# Lector de Imágenes (OCR)
archivo_img = st.file_uploader("📷 Sube una imagen para extraer texto automáticamente", type=['jpg','png','jpeg'])
texto_extraido = ""
if archivo_img:
    with st.spinner("Leyendo imagen..."):
        reader = easyocr.Reader(['es'])
        texto_extraido = "\n".join(reader.readtext(np.array(Image.open(archivo_img)), detail=0))
        st.success("¡Texto extraído con éxito!")

# Formulario
with st.form("main_form"):
    st.subheader("I. Datos Generales y Unidad")
    c1, c2 = st.columns(2)
    area = c1.text_input("Área de Conocimiento", "Ciencias Económica e Ingeniería")
    carrera = c2.text_input("Carrera", "Todas")
    asignatura = c1.text_input("Asignatura", "Estadística descriptiva")
    profesor = c2.text_input("Profesor(a)", "Ismael Antonio Cárdenas López")
    
    # Fecha automática
    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    fecha = c1.text_input("Fecha", value=fecha_actual)
    hora = c2.text_input("Hora", "10:30 am – 1:00 pm")
    
    # Selección de tema para auto-actualizar conclusiones
    unidad = st.selectbox("Seleccione el Tema de la Unidad", list(SUGERENCIAS.keys()))
    contenido = st.text_area("2.1 Contenido (Extraído por OCR)", value=texto_extraido, height=100)
    
    st.subheader("Objetivos y Evaluación")
    obj_gen = st.text_area("III. Objetivo General")
    obj_esp = st.text_area("IV. Objetivos Específicos")
    evaluacion = st.text_area("V. Evaluación (Criterios)")
    
    st.subheader("Cierre (Auto-actualizable)")
    # Se actualizan según la opción de 'unidad'
    sug = SUGERENCIAS.get(unidad, SUGERENCIAS["General / Otro"])
    conclusiones = st.text_area("VIII. Conclusiones", value=sug["concl"])
    recomendaciones = st.text_area("IX. Recomendaciones", value=sug["recom"])
    
    st.subheader("Extras")
    actividades = st.text_area("VI. Actividades")
    recursos = st.text_input("VII. Recursos", "Plan de clase, Libro, Pizarra")
    biblio = st.text_area("X. Bibliografía", "Posada, G. J. (2016). Elementos básicos de estadística...")

    procesar = st.form_submit_button("✅ Validar Datos")

# --- 5. DESCARGAS ---
if 'datos_listos' not in st.session_state: st.session_state.datos_listos = False
if procesar: st.session_state.datos_listos = True

if st.session_state.datos_listos:
    d = {
        'area': area, 'carrera': carrera, 'modalidad': "Presencial", 'asignatura': asignatura,
        'fecha': fecha, 'hora': hora, 'profesor': profesor, 'unidad': unidad, 'contenido': contenido,
        'obj_gen': obj_gen, 'obj_esp': obj_esp, 'evaluacion': evaluacion, 'actividades': actividades,
        'recursos': recursos, 'conclusiones': conclusiones, 'recomendaciones': recomendaciones, 'biblio': biblio
    }
    
    st.info("Selecciona el formato de descarga:")
    col_w, col_l = st.columns(2)
    with col_w:
        st.download_button("📥 Descargar en Word", generar_word(d), f"Plan_{unidad}.docx")
    with col_l:
        st.download_button("📥 Descargar en LaTeX", generar_latex(d), f"Plan_{unidad}.tex")
