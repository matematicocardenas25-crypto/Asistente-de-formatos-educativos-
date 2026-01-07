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

# --- 2. GENERADOR DE WORD ---
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
    lineas = [
        ("1.1 Área de conocimiento: ", f"{d['area']} " + "."*35),
        ("1.2 Carrera: ", f"{d['carrera']} " + "."*15 + " 1.3 Modalidad: " + f"{d['modalidad']} " + "."*10),
        ("1.4. Nombre de la asignatura: ", f"{d['asignatura']} " + "."*35),
        ("1.5. Fecha: ", f"{d['fecha']} " + "."*15 + " 1.7. Profesor: " + f"{d['profesor']}")
    ]
    for bold_t, norm_t in lineas:
        p = doc.add_paragraph()
        p.add_run(bold_t).bold = True
        p.add_run(norm_t)

    secciones = [
        ('II. UNIDAD:', d['unidad']), ('VI. ACTIVIDADES:', d['actividades']),
        ('X. BIBLIOGRAFIA:', d['biblio'])
    ]
    for tit, cont in secciones:
        doc.add_heading(tit, level=1)
        doc.add_paragraph(cont)

    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf

# --- 3. INTERFAZ ---
tab1, tab2 = st.tabs(["📄 Planificación Didáctica", "📊 Calculadora Multidimensión"])

with tab1:
    st.title("Generador de Formatos")
    archivo_img = st.file_uploader("📷 Escanear Actividades", type=['jpg','png','jpeg'])
    texto_escaneado = ""
    if archivo_img:
        reader = easyocr.Reader(['es'])
        texto_escaneado = "\n".join(reader.readtext(np.array(Image.open(archivo_img)), detail=0))

    with st.form("form_doc"):
        c1, c2 = st.columns(2)
        area = c1.text_input("Área", "Ciencias Económica e Ingeniería")
        carrera = c2.text_input("Carrera", "Ingeniería")
        asignatura = c1.text_input("Asignatura", "Estadística")
        profesor = c2.text_input("Profesor", "Ismael Antonio Cárdenas López")
        fecha = st.text_input("Fecha", datetime.now().strftime("%d/%m/%Y"))
        modalidad = "Presencial"
        unidad = st.text_input("Unidad", "Recopilación de datos")
        actividades = st.text_area("Actividades", value=texto_escaneado, height=150)
        biblio = st.text_area("Bibliografía")
        
        btn_validar = st.form_submit_button("✅ Procesar Datos")

    if btn_validar:
        # Guardar en diccionario para evitar NameError
        datos_plan = {
            "area": area, "carrera": carrera, "asignatura": asignatura, 
            "profesor": profesor, "fecha": fecha, "modalidad": modalidad,
            "unidad": unidad, "actividades": actividades, "biblio": biblio
        }
        st.success("¡Documentos generados!")
        col1, col2 = st.columns(2)
        col1.download_button("📥 Descargar Word", generar_word_oficial(datos_plan), f"Plan_{asignatura}.docx")
        
        latex_txt = f"\\section*{{Actividades}}\n{actividades}"
        col2.download_button("📥 Descargar LaTeX", latex_txt.encode(), f"Plan_{asignatura}.tex")

with tab2:
    st.title("📊 Gráficos Trascendentales (Ejes 0,0)")
    dim = st.radio("Dimensión:", ["2D (Plano)", "3D (Espacial)"], horizontal=True)
    
    # Diccionario de funciones para el evaluador
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
