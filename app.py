import streamlit as st
import easyocr
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from PIL import Image
import numpy as np
import io

# --- 1. CONFIGURACIÓN DE PÁGINA Y DISEÑO ---
st.set_page_config(page_title="Asistente de Formatos Educativos", layout="wide")

def aplicar_diseno_educativo():
    st.markdown(
        """
        <style>
        /* Fondo azul claro estilo educativo */
        .stApp {
            background-color: #E3F2FD;
            background-image: url("https://www.transparenttextures.com/patterns/pinstriped-suit.png");
        }

        /* Foto circular en la parte superior derecha */
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

aplicar_diseno_educativo()

# --- 2. FUNCIONES DE GENERACIÓN DE DOCUMENTOS ---

def crear_word(datos):
    doc = Document()
    
    # Encabezado centrado
    encabezado = doc.add_heading('PROGRAMACIÓN DIDÁCTICA PARA LOS APRENDIZAJES', 0)
    encabezado.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Secciones según tu formato oficial 
    doc.add_heading('I. DATOS GENERALES', level=1)
    doc.add_paragraph(f"Asignatura: {datos['asignatura']}")
    doc.add_paragraph(f"Profesor: {datos['profesor']}")
    
    doc.add_heading('II. UNIDAD Y CONTENIDO', level=1)
    doc.add_paragraph(datos['unidad'])
    doc.add_paragraph(f"Contenido: {datos['contenido']}")
    
    doc.add_heading('V. EVALUACIÓN (Criterios y Evidencias)', level=1)
    doc.add_paragraph(datos['evaluacion'])
    
    doc.add_heading('VIII. CONCLUSIONES', level=1)
    doc.add_paragraph(datos['conclusiones'])
    
    doc.add_heading('IX. RECOMENDACIONES', level=1)
    doc.add_paragraph(datos['recomendaciones'])
    
    output = io.BytesIO()
    doc.save(output)
    output.seek(0)
    return output

def crear_latex(datos):
    latex_template = f"""
\\documentclass{{article}}
\\usepackage[utf8]{{inputenc}}
\\title{{Programación Didáctica: {datos['asignatura']}}}
\\author{{{datos['profesor']}}}
\\begin{{document}}
\\maketitle
\\section{{I. Datos Generales}}
\\textbf{{Unidad:}} {datos['unidad']}
\\section{{II. Contenido}}
{datos['contenido']}
\\section{{V. Evaluación}}
{datos['evaluacion']}
\\section{{VIII. Conclusiones}}
{datos['conclusiones']}
\\section{{IX. Recomendaciones}}
{datos['recomendaciones']}
\\end{{document}}
    """
    return latex_template

# --- 3. INTERFAZ DE USUARIO ---

st.title("📝 Asistente de Formatos Educativos")
st.write("Sube una captura de contenido y completa los campos para generar tu plan de clase.")

# Carga de Imagen y OCR
archivo_img = st.file_uploader("Sube imagen del contenido (Libro/Notas)", type=['jpg', 'png', 'jpeg'])
texto_extraido = ""

if archivo_img:
    img = Image.open(archivo_img)
    st.image(img, caption="Imagen cargada", width=400)
    with st.spinner("Extrayendo texto con IA..."):
        reader = easyocr.Reader(['es'])
        resultado = reader.readtext(np.array(img), detail=0)
        texto_extraido = "\n".join(resultado)

# Formulario de datos
with st.form("datos_plan"):
    col1, col2 = st.columns(2)
    with col1:
        asignatura = st.text_input("Asignatura", "Estadística descriptiva")
        profesor = st.text_input("Profesor", "Ismael Antonio Cárdenas López")
    
    unidad = st.text_input("Unidad", "Recopilación de datos")
    contenido = st.text_area("Contenido (Extraído o manual)", value=texto_extraido, height=150)
    
    st.subheader("Secciones Actualizables")
    evaluacion = st.text_area("V. Evaluación (Criterios y Evidencias)", placeholder="Escriba aquí los criterios...")
    conclusiones = st.text_area("VIII. Conclusiones", placeholder="Escriba las conclusiones del tema...")
    recomendaciones = st.text_area("IX. Recomendaciones", placeholder="Escriba las recomendaciones...")
    
    boton_preparar = st.form_submit_button("Preparar Documentos")

# --- 4. DESCARGAS ---
if boton_preparar:
    datos_finales = {
        "asignatura": asignatura,
        "profesor": profesor,
        "unidad": unidad,
        "contenido": contenido,
        "evaluacion": evaluacion,
        "conclusiones": conclusiones,
        "recomendaciones": recomendaciones
    }
    
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.download_button(
            "📥 Descargar Word",
            data=crear_word(datos_finales),
            file_name=f"Plan_{asignatura}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    with col_d2:
        st.download_button(
            "📥 Descargar LaTeX",
            data=crear_latex(datos_finales),
            file_name=f"Plan_{asignatura}.tex",
            mime="text/plain"
        )
