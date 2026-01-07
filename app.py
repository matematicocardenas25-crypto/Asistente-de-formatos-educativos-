import streamlit as st
import easyocr
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from PIL import Image
import numpy as np
import io
from datetime import datetime

# --- 1. DISEÑO Y FOTO ---
st.set_page_config(page_title="Asistente Educativo Inteligente", layout="wide")

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

# --- 2. BASE DE DATOS INTELIGENTE (Auto-sugerencias) ---
# Aquí puedes agregar más temas siguiendo el mismo formato
SUGERENCIAS_AUTO = {
    "Recopilación de datos": {
        "conclusiones": "El estudiante logra identificar las fuentes primarias y secundarias de datos, comprendiendo la importancia de la fiabilidad en la investigación.",
        "recomendaciones": "Realizar ejercicios prácticos de diseño de encuestas breves para validar la comprensión de los conceptos básicos."
    },
    "Cálculo del tamaño muestral": {
        "conclusiones": "Se determinó con precisión el tamaño de la muestra aplicando fórmulas estadísticas según el margen de error aceptable.",
        "recomendaciones": "Reforzar el uso de calculadoras estadísticas y tablas de distribución para agilizar el proceso de muestreo."
    },
    "Estadística descriptiva": {
        "conclusiones": "Se sintetizaron los datos mediante medidas de tendencia central, permitiendo una interpretación clara del fenómeno estudiado.",
        "recomendaciones": "Utilizar software como Excel o SPSS para la visualización gráfica de las frecuencias obtenidas."
    }
}

# --- 3. FUNCIONES ---
def generar_word_oficial(d):
    doc = Document()
    titulo = doc.add_heading('PROGRAMACIÓN DIDÁCTICA PARA LOS APRENDIZAJES', 0)
    titulo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_heading('I. DATOS GENERALES:', level=1)
    p = doc.add_paragraph()
    p.add_run(f"1.1 Área: {d['area']}\n1.4 Asignatura: {d['asignatura']}\n1.5 Fecha: {d['fecha']}\n1.7 Profesor: {d['profesor']}")
    
    doc.add_heading('II. UNIDAD:', level=1)
    doc.add_paragraph(d['unidad'])
    doc.add_paragraph(f"2.1. Contenido: \n{d['contenido']}")
    
    for sec, cont in [('VIII. CONCLUSIONES:', d['conclusiones']), ('IX. RECOMENDACIONES:', d['recomendaciones']), ('X. BIBLIOGRAFIA:', d['biblio'])]:
        doc.add_heading(sec, level=1)
        doc.add_paragraph(cont)

    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf

# --- 4. INTERFAZ ---
st.title("📝 Programación Didáctica Automática")

# Configuración de Fecha Automática
fecha_hoy = datetime.now().strftime("%d/%m/%Y")

with st.form("main_form"):
    col1, col2 = st.columns(2)
    with col1:
        asignatura = st.text_input("Asignatura", "Estadística descriptiva")
        fecha = st.text_input("Fecha de la sesión", value=fecha_hoy)
    with col2:
        # Selección de tema que dispara la automatización
        tema_seleccionado = st.selectbox("Seleccione el Tema de la Unidad", list(SUGERENCIAS_AUTO.keys()))
        profesor = st.text_input("Profesor", "Ismael Antonio Cárdenas López")

    st.subheader("Contenido y Desarrollo")
    contenido = st.text_area("2.1 Contenido del tema", height=100)
    
    # Lógica de auto-rellenado
    sug_concl = SUGERENCIAS_AUTO[tema_seleccionado]["conclusiones"]
    sug_recom = SUGERENCIAS_AUTO[tema_seleccionado]["recomendaciones"]
    
    conclusiones = st.text_area("VIII. Conclusiones (Auto-generadas)", value=sug_concl)
    recomendaciones = st.text_area("IX. Recomendaciones (Auto-generadas)", value=sug_recom)
    
    biblio = st.text_area("X. Bibliografía", "Posada, G. J. (2016). Elementos básicos de estadística descriptiva...")

    procesar = st.form_submit_button("Validar y Preparar Descarga")

if procesar:
    datos = {
        'area': "Ciencias Económicas e Ingeniería", 'asignatura': asignatura,
        'fecha': fecha, 'profesor': profesor, 'unidad': tema_seleccionado,
        'contenido': contenido, 'conclusiones': conclusiones, 
        'recomendaciones': recomendaciones, 'biblio': biblio
    }
    st.success(f"Plan actualizado para el tema: {tema_seleccionado}")
    st.download_button("📥 Descargar Plan en Word", generar_word_oficial(datos), f"Plan_{tema_seleccionado}.docx")
