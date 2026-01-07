import streamlit as st
import easyocr
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from PIL import Image
import numpy as np
import io
from datetime import datetime

# --- 1. ESTILO Y FOTO CIRCULAR ---
st.set_page_config(page_title="Generador de Formatos Oficiales", layout="wide")
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

# --- 2. GENERADOR DE WORD (ESTILO ORIGINAL INTEGRAL) ---
def generar_word_oficial(d):
    doc = Document()
    
    # Fuente Arial 12 por defecto
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Arial'
    font.size = Pt(12)

    # Encabezado Oficial
    section = doc.sections[0]
    header = section.header
    header.paragraphs[0].text = "PROGRAMACIÓN DIDÁCTICA PARA LOS APRENDIZAJES"
    header.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Título Principal
    t = doc.add_paragraph()
    run = t.add_run('PROGRAMACIÓN DIDÁCTICA PARA LOS APRENDIZAJES')
    run.bold = True
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # I. DATOS GENERALES (Con líneas de puntos y texto entre paréntesis)
    doc.add_heading('I. DATOS GENERALES:', level=1)
    
    lineas = [
        (f"1.1 Área de conocimiento: ", f"{d['area']} " + "."*35),
        (f"1.2 Carrera: ", f"{d['carrera']} " + "."*15 + " 1.3 Modalidad: " + f"{d['modalidad']} " + "."*10 + " Turno: " + f"{d['turno']} " + "."*10),
        (f"1.4. Nombre de la asignatura: ", f"{d['asignatura']} " + "."*35),
        (f"1.5. Fecha: ", f"{d['fecha']} " + "."*15 + " 1.6. Hora: " + f"{d['hora']} " + "."*15),
        (f"1.7. Profesor (a): ", f"{d['profesor']} " + "."*35)
    ]
    
    for bold_text, normal_text in lineas:
        p = doc.add_paragraph()
        p.add_run(bold_text).bold = True
        p.add_run(normal_text)

    # SECCIONES II A X (Respetando paréntesis originales)
    secciones = [
        ('II. UNIDAD:', d['unidad']),
        ('2.1. Contenido:', d['contenido']),
        ('III. OBJETIVO GENERAL:', d['obj_gen']),
        ('IV. OBJETIVO(S) ESPECÍFICO(S):', d['obj_esp']),
        ('V. EVALUACIÓN DE LOS APRENDIZAJES (Criterios y Evidencias):', d['evaluacion']),
        ('VI. ACTIVIDADES DEL DOCENTE Y ESTUDIANTES (Desarrollo):', d['actividades']),
        ('VII. MEDIOS O RECURSOS DIDÁCTICOS:', d['recursos']),
        ('VIII. CONCLUSIONES:', d['conclusiones']),
        ('IX. RECOMENDACIONES:', d['recomendaciones']),
        ('X. BIBLIOGRAFIA:', d['bibliografia'])
    ]

    for titulo, contenido in secciones:
        doc.add_heading(titulo, level=1)
        doc.add_paragraph(contenido)

    # Pie de página con letra Arial 8
    footer = section.footer
    f_p = footer.paragraphs[0]
    f_p.text = "Formato de Programación Didáctica 1- Presencial. (Uso Oficial)"
    f_p.style.font.size = Pt(8)

    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf

# --- 3. INTERFAZ Y OCR ---
st.title("📝 Generador de Programación Didáctica")

# El escaneo va directo a Actividades de Desarrollo
archivo_img = st.file_uploader("📷 Subir imagen para ACTIVIDADES (Mantiene paréntesis)", type=['jpg','png','jpeg'])
texto_escaneado = ""
if archivo_img:
    with st.spinner("Escaneando texto..."):
        reader = easyocr.Reader(['es'])
        # El lector de easyocr por defecto ya conserva los caracteres ( )
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

    st.subheader("II a IV. Planificación")
    unidad = st.text_input("II. Unidad", "Recopilación de datos")
    contenido = st.text_area("2.1 Contenido", height=80)
    obj_gen = st.text_area("III. Objetivo General")
    obj_esp = st.text_area("IV. Objetivo(s) Específico(s)") # Paréntesis aquí

    st.subheader("V y VI. Evaluación y Actividades")
    evaluacion = st.text_area("V. Evaluación (Criterios y Evidencias)") # Paréntesis aquí
    # Aquí se carga el texto del escaneo automáticamente
    actividades = st.text_area("VI. Actividades (Escaneo)", value=texto_escaneado, height=200)

    st.subheader("Cierre")
    recursos = st.text_input("VII. Recursos", "Libro, Pizarra, Guía")
    conclusiones = st.text_area("VIII. Conclusiones")
    recomendaciones = st.text_area("IX. Recomendaciones")
    biblio = st.text_area("X. Bibliografía")

    validar = st.form_submit_button("✅ Generar Formatos")

if validar:
    datos = {
        'area': area, 'carrera': carrera, 'modalidad': modalidad, 'turno': turno,
        'asignatura': asignatura, 'fecha': fecha, 'hora': hora, 'profesor': profesor,
        'unidad': unidad, 'contenido': contenido, 'obj_gen': obj_gen, 'obj_esp': obj_esp,
        'evaluacion': evaluacion, 'actividades': actividades, 'recursos': recursos,
        'conclusiones': conclusiones, 'recomendaciones': recomendaciones, 'bibliografia': biblio
    }
    
    st.success("¡Documentos listos! Se han conservado todos los caracteres y formato original.")
    col1, col2 = st.columns(2)
    with col1:
        st.download_button("📥 Descargar Word (Arial 12)", generar_word_oficial(datos), f"Plan_{asignatura}.docx")
    with col2:
        # Formato LaTeX conservando todo el texto
        latex_content = f"\\section*{{VI. Actividades}}\n{actividades}".encode('utf-8')
        st.download_button("📥 Descargar LaTeX (.tex)", latex_content, f"Plan_{asignatura}.tex")
