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

# --- 1. CONFIGURACIÓN DE PÁGINA Y ESTILO ---
st.set_page_config(page_title="Asistente Educativo - Prof. Cárdenas", layout="wide")

st.markdown(
    """
    <style>
    .stApp { background-color: #E3F2FD; }
    .foto-perfil { position: fixed; top: 50px; right: 30px; z-index: 1000; }
    .foto-perfil img { width: 110px; height: 110px; border-radius: 50%; border: 3px solid #1976D2; object-fit: cover; }
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] { background-color: #f0f2f6; border-radius: 5px; padding: 10px 20px; }
    </style>
    <div class="foto-perfil">
        <img src="https://raw.githubusercontent.com/matematicocardenas25-cripto/Asistente-de-formatos-educativos-/main/foto.jpg.jpeg">
    </div>
    """, unsafe_allow_html=True
)

# --- 2. FUNCIONES DE GENERACIÓN DE DOCUMENTOS (WORD Y LATEX) ---
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
    p = doc.add_paragraph()
    p.add_run(f"1.1 Área: {d['area']} " + "."*20 + "\n")
    p.add_run(f"1.4 Asignatura: {d['asignatura']} " + "."*20 + "\n")
    p.add_run(f"1.5 Fecha: {d['fecha']} " + "."*10 + " 1.7 Profesor: " + d['profesor'])
    
    secciones = [
        ('II. UNIDAD:', d['unidad']), ('2.1. Contenido:', d['contenido']),
        ('III. OBJETIVO GENERAL:', d['obj_gen']), ('IV. OBJETIVO(S) ESPECÍFICO(S):', d['obj_esp']),
        ('V. EVALUACIÓN (Criterios y Evidencias):', d['evaluacion']),
        ('VI. ACTIVIDADES DEL DOCENTE Y ESTUDIANTES (Desarrollo):', d['actividades']),
        ('VII. MEDIOS O RECURSOS DIDÁCTICOS:', d['recursos']),
        ('VIII. CONCLUSIONES:', d['conclusiones']),
        ('IX. RECOMENDACIONES:', d['recomendaciones']),
        ('X. BIBLIOGRAFIA:', d['bibliografia'])
    ]
    for tit, cont in secciones:
        doc.add_heading(tit, level=1)
        doc.add_paragraph(cont)
    
    footer = section.footer
    footer.paragraphs[0].text = "Uso Oficial - Formato Arial 12"
    footer.paragraphs[0].style.font.size = Pt(8)

    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf

# --- 3. INTERFAZ POR PESTAÑAS SEPARADAS ---
st.title("📝 Asistente Educativo Integral")
tab1, tab2 = st.tabs(["📄 Plan de Clase (OCR)", "📊 Calculadora y Generador Gráfico"])

# --- PESTAÑA 1: PLAN DE CLASE ---
with tab1:
    archivo_img = st.file_uploader("📷 Escanear texto para ACTIVIDADES (Punto VI)", type=['jpg','png','jpeg'])
    texto_escaneado = ""
    if archivo_img:
        reader = easyocr.Reader(['es'])
        texto_escaneado = "\n".join(reader.readtext(np.array(Image.open(archivo_img)), detail=0))

    with st.form("form_plan"):
        c1, c2 = st.columns(2)
        area = c1.text_input("I. Área de Conocimiento", "Ciencias Económica e Ingeniería")
        asignatura = c2.text_input("I. Asignatura", "Estadística descriptiva")
        profesor = st.text_input("I. Profesor(a)", "Ismael Antonio Cárdenas López")
        fecha = st.text_input("I. Fecha", value=datetime.now().strftime("%d/%m/%Y"))
        
        unidad = st.text_input("II. Unidad", "Recopilación de datos")
        contenido = st.text_area("2.1 Contenido", height=80)
        obj_gen = st.text_area("III. Objetivo General")
        obj_esp = st.text_area("IV. Objetivo(s) Específico(s)")
        
        actividades = st.text_area("VI. Actividades (Escaneo automático aquí)", value=texto_escaneado, height=150)
        
        evaluacion = st.text_area("V. Evaluación (Criterios y Evidencias)")
        conclusiones = st.text_area("VIII. Conclusiones")
        recomendaciones = st.text_area("IX. Recomendaciones")
        biblio = st.text_area("X. Bibliografía")
        
        enviar_plan = st.form_submit_button("✅ Validar Datos del Plan")

    if enviar_plan:
        d = {'area':area, 'asignatura':asignatura, 'profesor':profesor, 'fecha':fecha, 'unidad':unidad, 'contenido':contenido, 'obj_gen':obj_gen, 'obj_esp':obj_esp, 'evaluacion':evaluacion, 'actividades':actividades, 'recursos':"Libro, Pizarra", 'conclusiones':conclusiones, 'recomendaciones':recomendaciones, 'bibliografia':biblio, 'carrera':"Todas", 'modalidad':"Presencial", 'turno':"Diurno", 'hora':"10:30 am"}
        
        st.success("¡Plan de clase listo!")
        col_w, col_l = st.columns(2)
        with col_w:
            st.download_button("📥 Descargar Word (.docx)", generar_word_oficial(d), f"Plan_{asignatura}.docx")
        with col_l:
            latex_code = f"\\section*{{VI. Actividades}}\n{actividades}"
            st.download_button("📥 Descargar LaTeX (.tex)", latex_code.encode(), f"Plan_{asignatura}.tex")

# --- PESTAÑA 2: CALCULADORA Y GRAFICADOR APARTE ---
with tab2:
    st.header("📊 Generador de Gráficos e Imágenes")
    st.write("Crea tus gráficas aquí, descárgalas como imagen y pégalas en tu documento manualmente.")
    
    col_g1, col_g2 = st.columns([1, 2])
    
    with col_g1:
        tipo = st.selectbox("Seleccione tipo de gráfico", ["Matemático (y=f(x))", "Barras Estadísticas", "Distribución Normal"])
        color_graf = st.color_picker("Elige color del gráfico", "#1976D2")
        
        if tipo == "Matemático (y=f(x))":
            ecuacion = st.text_input("Escribe la función (ej: x**2, np.sin(x))", "x**2")
            x_range = st.slider("Rango de X", -50, 50, (-10, 10))
            
        elif tipo == "Barras Estadísticas":
            datos_x = st.text_input("Etiquetas (A, B, C...)", "Muestra 1, Muestra 2, Muestra 3")
            datos_y = st.text_input("Valores (10, 20...)", "15, 30, 25")

    with col_g2:
        fig = go.Figure()
        
        if tipo == "Matemático (y=f(x))":
            x = np.linspace(x_range[0], x_range[1], 500)
            try:
                y = eval(ecuacion)
                fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(color=color_graf), name=ecuacion))
                fig.update_layout(title=f"Gráfica de f(x) = {ecuacion}", xaxis_title="Eje X", yaxis_title="Eje Y")
            except:
                st.error("Error en la fórmula. Usa formato Python (ej: np.exp(x) para e^x)")

        elif tipo == "Barras Estadísticas":
            x_vals = [i.strip() for i in datos_x.split(',')]
            y_vals = [float(i) for i in datos_y.split(',')]
            fig.add_trace(go.Bar(x=x_vals, y=y_vals, marker_color=color_graf))
            fig.update_layout(title="Distribución de Frecuencias")

        st.plotly_chart(fig, use_container_width=True)
        
        # Opción de descarga de la gráfica como imagen para pegar en Word
        st.info("💡 Para llevar esta gráfica a tu Word: Haz clic en el ícono de la 'Cámara' que aparece arriba a la derecha del gráfico al pasar el ratón.")
