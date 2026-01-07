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

# --- 1. ESTILO Y FOTO CIRCULAR ---
st.set_page_config(page_title="Asistente Educativo - Prof. Cárdenas", layout="wide")
st.markdown(
    """
    <style>
    .stApp { background-color: #E3F2FD; }
    .foto-perfil { position: fixed; top: 50px; right: 30px; z-index: 1000; }
    .foto-perfil img { width: 115px; height: 115px; border-radius: 50%; border: 3px solid #1976D2; object-fit: cover; }
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    </style>
    <div class="foto-perfil">
        <img src="https://raw.githubusercontent.com/matematicocardenas25-cripto/Asistente-de-formatos-educativos-/main/foto.jpg.jpeg">
    </div>
    """, unsafe_allow_html=True
)

# --- 2. GENERADOR DE WORD (FORMATO ORIGINAL INTEGRAL) ---
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

    secciones = [
        ('II. UNIDAD:', d['unidad']), ('2.1. Contenido:', d['contenido']),
        ('III. OBJETIVO GENERAL:', d['obj_gen']), ('IV. OBJETIVO(S) ESPECÍFICO(S):', d['obj_esp']),
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

    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf

# --- 3. INTERFAZ POR PESTAÑAS ---
tab1, tab2 = st.tabs(["📄 Planificación Didáctica", "📊 Calculadora y Gráficos Multidimensión"])

with tab1:
    st.title("Generador de Programación Didáctica")
    archivo_img = st.file_uploader("📷 Subir imagen para ACTIVIDADES", type=['jpg','png','jpeg'])
    texto_escaneado = ""
    if archivo_img:
        reader = easyocr.Reader(['es'])
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

        st.subheader("Planificación y Cierre")
        unidad = st.text_input("II. Unidad", "Recopilación de datos")
        contenido = st.text_area("2.1 Contenido")
        obj_gen = st.text_area("III. Objetivo General")
        obj_esp = st.text_area("IV. Objetivo(s) Específico(s)")
        evaluacion = st.text_area("V. Evaluación (Criterios y Evidencias)")
        actividades = st.text_area("VI. Actividades (Desarrollo)", value=texto_escaneado, height=150)
        recursos = st.text_input("VII. Recursos", "Libro, Pizarra, Guía")
        conclusiones = st.text_area("VIII. Conclusiones")
        recomendaciones = st.text_area("IX. Recomendaciones")
        biblio = st.text_area("X. Bibliografía")
        validar = st.form_submit_button("✅ Procesar Plan")

    if validar:
        datos = {
            'area': area, 'carrera': carrera, 'modalidad': modalidad, 'turno': turno,
            'asignatura': asignatura, 'fecha': fecha, 'hora': hora, 'profesor': profesor,
            'unidad': unidad, 'contenido': contenido, 'obj_gen': obj_gen, 'obj_esp': obj_esp,
            'evaluacion': evaluacion, 'actividades': actividades, 'recursos': recursos,
            'conclusiones': conclusiones, 'recomendaciones': recomendaciones, 'bibliografia': biblio
        }
        st.success("¡Documento generado correctamente!")
        st.download_button("📥 Descargar Word (Arial 12)", generar_word_oficial(datos), f"Plan_{asignatura}.docx")

with tab2:
    st.title("📊 Graficador con Ejes en el Origen (0,0)")
    dim = st.radio("Dimensión del gráfico:", ["2D (Plano)", "3D (Espacial)"], horizontal=True)
    
    col_c1, col_c2 = st.columns([1, 2])
    with col_c1:
        if dim == "2D (Plano)":
            tipo = st.selectbox("Tipo:", ["Función Matemática", "Estadística (Barras)"])
            if tipo == "Función Matemática":
                f_x = st.text_input("f(x) =", "x**2 - 4")
                r_x = st.slider("Rango de visualización", -100, 100, (-10, 10))
            else:
                vals_y = st.text_input("Valores (separados por coma)", "10, -5, 15, -10")
        else:
            f_z = st.text_input("z = f(x, y)", "x**2 - y**2")
            r_3d = st.slider("Rango malla", 5, 50, 10)

    with col_c2:
        fig = go.Figure()
        try:
            if dim == "2D (Plano)":
                if tipo == "Función Matemática":
                    x = np.linspace(r_x[0], r_x[1], 400)
                    y = eval(f_x.replace('x', 'x'))
                    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(color='#1976D2', width=3)))
                    
                    # CONFIGURACIÓN DE EJES EN EL CENTRO (0,0)
                    fig.update_xaxes(zeroline=True, zerolinewidth=2, zerolinecolor='Black', showgrid=True)
                    fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor='Black', showgrid=True)
                    fig.update_layout(title=f"Gráfica de f(x) = {f_x}", plot_bgcolor='white')
                
                else:
                    data = [float(i) for i in vals_y.split(',')]
                    fig = px.bar(y=data, title="Gráfico Estadístico")
                    fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor='Black')

            else:
                x = y = np.linspace(-r_3d, r_3d, 100)
                X, Y = np.meshgrid(x, y)
                Z = eval(f_z)
                fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Viridis')])
                fig.update_layout(title=f"Superficie 3D: {f_z}")

            st.plotly_chart(fig, use_container_width=True)
            st.info("📸 **Para descargar:** Use el icono de la cámara en la esquina superior derecha del gráfico.")
        except Exception as e:
            st.error(f"Error en la expresión matemática: {e}")
