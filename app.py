import streamlit as st
import easyocr
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from PIL import Image
import numpy as np
import io

# --- 1. CONFIGURACIÓN Y DISEÑO ---
st.set_page_config(page_title="Asistente de Programación Didáctica", layout="wide")

def aplicar_diseno_personalizado():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #E3F2FD; /* Azul claro educativo */
            background-image: url("https://www.transparenttextures.com/patterns/pinstriped-suit.png");
        }
        .foto-perfil {
            position: fixed;
            top: 50px;
            right: 30px;
            z-index: 1000;
        }
        .foto-perfil img {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            border: 4px solid #1976D2;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
            object-fit: cover;
        }
        </style>
        <div class="foto-perfil">
            <img src="https://raw.githubusercontent.com/matematicocardenas25-cripto/Asistente-de-formatos-educativos-/main/foto.jpg.jpeg">
        </div>
        """,
        unsafe_allow_html=True
    )

aplicar_diseno_personalizado()

# --- 2. LÓGICA DE GENERACIÓN DE DOCUMENTO WORD ---
def generar_word_completo(d):
    doc = Document()
    
    # Título Principal
    t = doc.add_heading('PROGRAMACIÓN DIDÁCTICA PARA LOS APRENDIZAJES', 0)
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # I. DATOS GENERALES
    doc.add_heading('I. DATOS GENERALES:', level=1)
    p1 = doc.add_paragraph()
    p1.add_run(f"1.1 Área de conocimiento: ").bold = True
    p1.add_run(d['area'])
    p1.add_run(f"\n1.4 Nombre de la asignatura: ").bold = True
    p1.add_run(d['asignatura'])
    p1.add_run(f"\n1.7 Profesor (a): ").bold = True
    p1.add_run(d['profesor'])
    
    # II. UNIDAD Y CONTENIDO
    doc.add_heading('II. UNIDAD:', level=1)
    doc.add_paragraph(d['unidad'])
    doc.add_paragraph(f"2.1 Contenido: \n{d['contenido']}")
    
    # III y IV. OBJETIVOS
    doc.add_heading('III. OBJETIVO GENERAL:', level=1)
    doc.add_paragraph(d['obj_general'])
    doc.add_heading('IV. OBJETIVOS ESPECÍFICOS:', level=1)
    doc.add_paragraph(d['obj_especificos'])
    
    # V. EVALUACIÓN
    doc.add_heading('V. EVALUACIÓN DE LOS APRENDIZAJES (Criterios y Evidencias):', level=1)
    doc.add_paragraph(d['evaluacion'])
    
    # VI. ACTIVIDADES
    doc.add_heading('VI. ACTIVIDADES DEL DOCENTE Y ESTUDIANTES:', level=1)
    doc.add_paragraph(d['actividades'])
    
    # VII. RECURSOS
    doc.add_heading('VII. MEDIOS O RECURSOS DIDÁCTICOS:', level=1)
    doc.add_paragraph(d['recursos'])
    
    # VIII y IX. CIERRE
    doc.add_heading('VIII. CONCLUSIONES:', level=1)
    doc.add_paragraph(d['conclusiones'])
    doc.add_heading('IX. RECOMENDACIONES:', level=1)
    doc.add_paragraph(d['recomendaciones'])
    
    # X. BIBLIOGRAFÍA
    doc.add_heading('X. BIBLIOGRAFÍA:', level=1)
    doc.add_paragraph(d['bibliografia'])

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- 3. INTERFAZ DE USUARIO ---
st.title("📝 Creador de Programación Didáctica Oficial")

# OCR - Subida de imagen
img_file = st.file_uploader("Sube captura del libro para el Contenido", type=['jpg','png','jpeg'])
texto_ia = ""
if img_file:
    reader = easyocr.Reader(['es'])
    texto_ia = "\n".join(reader.readtext(np.array(Image.open(img_file)), detail=0))
    st.success("Texto extraído con éxito.")

# FORMULARIO CON TODOS LOS PUNTOS DEL FORMATO
with st.form("form_oficial"):
    st.subheader("I. Datos Generales")
    c1, c2 = st.columns(2)
    area = c1.text_input("Área de Conocimiento", "Ingeniería y Construcción") [cite: 257]
    asignatura = c2.text_input("Asignatura", "Estadística descriptiva") [cite: 259]
    profesor = st.text_input("Profesor(a)", "Ismael Antonio Cárdenas López") [cite: 262]
    
    st.subheader("II. Unidad y Contenido")
    unidad = st.text_input("Nombre de la Unidad", "Recopilación de datos") [cite: 264]
    contenido = st.text_area("2.1 Contenido (Extraído por OCR)", value=texto_ia, height=150) [cite: 266]
    
    st.subheader("III y IV. Objetivos")
    obj_gen = st.text_area("Objetivo General") [cite: 271]
    obj_esp = st.text_area("Objetivos Específicos") [cite: 273]
    
    st.subheader("V. Evaluación")
    evaluacion = st.text_area("Criterios y Evidencias", height=100) [cite: 280]
    
    st.subheader("VI y VII. Desarrollo y Recursos")
    actividades = st.text_area("Actividades Docente/Estudiante") [cite: 289]
    recursos = st.text_input("Medios y Recursos", "Plan de clase, Libro, Pizarra...") [cite: 485]
    
    st.subheader("VIII, IX y X. Cierre y Bibliografía")
    conclusiones = st.text_area("Conclusiones") [cite: 487]
    recomendaciones = st.text_area("Recomendaciones") [cite: 492]
    bibliografia = st.text_area("Bibliografía Utilizada") [cite: 494]
    
    generar = st.form_submit_button("Generar Plan de Clase Completo")

if generar:
    datos = {
        'area': area, 'asignatura': asignatura, 'profesor': profesor,
        'unidad': unidad, 'contenido': contenido, 'obj_general': obj_gen,
        'obj_especificos': obj_esp, 'evaluacion': evaluacion,
        'actividades': actividades, 'recursos': recursos,
        'conclusiones': conclusiones, 'recomendaciones': recomendaciones,
        'bibliografia': bibliografia
    }
    
    st.download_button(
        label="📥 Descargar Programación en Word",
        data=generar_word_completo(datos),
        file_name=f"Programacion_{asignatura}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
