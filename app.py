import streamlit as st
import easyocr
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from PIL import Image
import numpy as np
import io
from datetime import datetime

# --- 1. ESTILO VISUAL DE LA APP (Fondo azul y Foto) ---
st.set_page_config(page_title="Asistente de Formatos", layout="wide")
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

# --- 2. LÓGICA DE DATOS AUTOMÁTICOS ---
SUGERENCIAS = {
    "Recopilación de datos": {
        "concl": "El estudiante identifica fuentes de datos y aplica técnicas de recolección con precisión.",
        "recom": "Revisar bibliografía para profundizar conocimiento del tema impartido durante la sesión de clase."
    },
    "Cálculo del tamaño muestral": {
        "concl": "Se logra determinar el tamaño de muestra idóneo garantizando representatividad.",
        "recom": "Realizar ejercicios adicionales con márgenes de error variables."
    }
}

# --- 3. GENERADOR DE WORD CON FORMATO ARYAL 12 Y LÍNEAS DE PUNTOS ---
def generar_word_estilo_original(d):
    doc = Document()
    
    # Configurar Fuente Global a Arial 12
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Arial'
    font.size = Pt(12)

    # ENCABEZADO Y PIE DE PÁGINA
    header = doc.sections[0].header
    header.paragraphs[0].text = "PROGRAMACIÓN DIDÁCTICA PARA LOS APRENDIZAJES"
    header.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    footer = doc.sections[0].footer
    fp = footer.paragraphs[0]
    fp.text = "Formato de Programación Didáctica - Facultad de Ingeniería"
    fp.style.font.size = Pt(8) # Letra pequeñita

    # TITULO PRINCIPAL
    t = doc.add_paragraph()
    run = t.add_run('PROGRAMACIÓN DIDÁCTICA PARA LOS APRENDIZAJES')
    run.bold = True
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # I. DATOS GENERALES (Con líneas de puntos)
    doc.add_heading('I. DATOS GENERALES:', level=1)
    
    p1 = doc.add_paragraph()
    p1.add_run("1.1 Área de conocimiento: ").bold = True
    p1.add_run(f"{d['area']} " + "."*40)
    
    p2 = doc.add_paragraph()
    p2.add_run("1.2 Carrera: ").bold = True
    p2.add_run(f"{d['carrera']} " + "."*20 + " ")
    p2.add_run("1.3 Modalidad: ").bold = True
    p2.add_run(f"{d['modalidad']} " + "."*10 + " ")
    p2.add_run("Turno: ").bold = True
    p2.add_run(f"{d['turno']} " + "."*10)

    p3 = doc.add_paragraph()
    p3.add_run("1.4. Nombre de la asignatura: ").bold = True
    p3.add_run(f"{d['asignatura']} " + "."*40)

    p4 = doc.add_paragraph()
    p4.add_run("1.5. Fecha: ").bold = True
    p4.add_run(f"{d['fecha']} " + "."*15 + " ")
    p4.add_run("1.6. Hora: ").bold = True
    p4.add_run(f"{d['hora']} " + "."*15)

    p5 = doc.add_paragraph()
    p5.add_run("1.7. Profesor (a): ").bold = True
    p5.add_run(f"{d['profesor']} " + "."*40)

    # SECCIONES II A X
    secciones = [
        ('II. UNIDAD:', d['unidad']),
        ('2.1. Contenido:', d['contenido']),
        ('III. OBJETIVO GENERAL:', d['obj_gen']),
        ('IV. OBJETIVO(S) ESPECÍFICO(S):', d['obj_esp']),
        ('V. EVALUACIÓN DE LOS APRENDIZAJES:', d['evaluacion']),
        ('VI. ACTIVIDADES:', d['actividades']),
        ('VII. MEDIOS O RECURSOS:', d['recursos']),
        ('VIII. CONCLUSIONES:', d['conclusiones']),
        ('IX. RECOMENDACIONES:', d['recomendaciones']),
        ('X. BIBLIOGRAFIA:', d['bibliografia'])
    ]

    for titulo, contenido in secciones:
        h = doc.add_heading(titulo, level=1)
        doc.add_paragraph(contenido)

    # Letra pequeña al final (Aclaraciones)
    p_f = doc.add_paragraph()
    run_f = p_f.add_run("\nNota: Este documento es de uso oficial y debe ser actualizado según el tema impartido.")
    run_f.font.size = Pt(8)
    run_f.italic = True

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

def generar_latex_simple(d):
    return f"\\documentclass{{article}}\\begin{{document}}\\section*{{{d['asignatura']}}}\\subsection*{{Contenido}}{d['contenido']}\\end{{document}}"

# --- 4. INTERFAZ ---
st.title("📝 Generador de Formatos Oficiales (Arial 12)")

# OCR
archivo_img = st.file_uploader("📷 Sube imagen para extraer Contenido", type=['jpg','png','jpeg'])
texto_ocr = ""
if archivo_img:
    reader = easyocr.Reader(['es'])
    texto_ocr = "\n".join(reader.readtext(np.array(Image.open(archivo_img)), detail=0))

with st.form("form_oficial"):
    c1, c2 = st.columns(2)
    area = c1.text_input("Área de Conocimiento", "Ciencias Económica e Ingeniería")
    carrera = c2.text_input("Carrera", "Todas")
    asignatura = c1.text_input("Asignatura", "Estadística descriptiva")
    profesor = c2.text_input("Profesor", "Ismael Antonio Cárdenas López")
    
    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    fecha = c1.text_input("Fecha", value=fecha_actual)
    hora = c2.text_input("Hora", "10:30 am – 1:00 pm")
    modalidad = c1.text_input("Modalidad", "Presencial")
    turno = c2.text_input("Turno", "Diurno")

    unidad = st.selectbox("Seleccione el Tema", list(SUGERENCIAS.keys()) + ["Otro"])
    contenido = st.text_area("2.1 Contenido", value=texto_ocr, height=100)
    
    obj_gen = st.text_area("III. Objetivo General")
    obj_esp = st.text_area("IV. Objetivos Específicos")
    evaluacion = st.text_area("V. Evaluación")
    
    sug = SUGERENCIAS.get(unidad, {"concl": "", "recom": ""})
    conclusiones = st.text_area("VIII. Conclusiones", value=sug["concl"])
    recomendaciones = st.text_area("IX. Recomendaciones", value=sug["recom"])
    
    actividades = st.text_area("VI. Actividades")
    recursos = st.text_input("VII. Recursos", "Libro, Pizarra, Plan de Clase")
    bibliografia = st.text_area("X. Bibliografía")

    validar = st.form_submit_button("✅ Preparar Documentos")

if validar:
    d_final = {
        'area': area, 'carrera': carrera, 'modalidad': modalidad, 'turno': turno,
        'asignatura': asignatura, 'fecha': fecha, 'hora': hora, 'profesor': profesor,
        'unidad': unidad, 'contenido': contenido, 'obj_gen': obj_gen, 'obj_esp': obj_esp,
        'evaluacion': evaluacion, 'actividades': actividades, 'recursos': recursos,
        'conclusiones': conclusiones, 'recomendaciones': recomendaciones, 'bibliografia': bibliografia
    }
    
    st.success("¡Documentos generados con formato oficial!")
    col_w, col_l = st.columns(2)
    with col_w:
        st.download_button("📥 Descargar Word (Arial 12)", generar_word_estilo_original(d_final), f"Plan_{asignatura}.docx")
    with col_l:
        st.download_button("📥 Descargar LaTeX", generar_latex_simple(d_final).encode(), f"Plan_{asignatura}.tex")
