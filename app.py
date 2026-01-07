import streamlit as st
import easyocr
from docx import Document
from PIL import Image
import numpy as np
import io
import streamlit as st

# --- CONFIGURACIÓN DE DISEÑO PERSONALIZADO ---
def agregar_diseno_personalizado():
    st.markdown(
        """
        <style>
        /* 1. Fondo Educativo para toda la página */
        .stApp {
            background-image: url("https://www.transparenttextures.com/patterns/notebook.png"); /* Patrón de hoja de cuaderno */
            background-color: #f0f2f6; /* Color suave de fondo */
            background-attachment: fixed;
        }

        /* 2. Tu imagen en la esquina superior derecha */
        .imagen-derecha {
            position: fixed;
            top: 50px;
            right: 20px;
            z-index: 100;
        }
        
        .imagen-derecha img {
            width: 120px; /* Tamaño de tu foto */
            border-radius: 50%; /* La hace circular */
            border: 3px solid #007bff; /* Un borde azul educativo */
            box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
        }
        </style>
        
        <div class="imagen-derecha">
            <img src="https://github.com/matematicocardenas25-crypto/Asistente-de-formatos-educativos-/blob/main/foto.jpg.jpeg">
        </div>
        """,
        unsafe_allow_html=True
    )

# Llamar a la función para aplicar los cambios
agregar_diseno_personalizado()

# Configuración de la página
st.set_page_config(page_title="Automatizador Educativo", layout="centered")

st.title("📝 Creador de Formatos Educativos")
st.write("Sube una captura de texto/imágenes y genera tu documento automáticamente.")

# Función para extraer texto (OCR)
@st.cache_resource # Esto hace que la página no se trabe al cargar el lector
def cargar_lector():
    return easyocr.Reader(['es'])

reader = cargar_lector()

# 1. Subir la imagen (Captura de libro o notas)
archivo_imagen = st.file_uploader("1. Sube la captura de la información", type=["jpg", "png", "jpeg"])

if archivo_imagen:
    imagen = Image.open(archivo_imagen)
    st.image(imagen, caption="Imagen cargada", use_column_width=True)
    
    with st.spinner('Procesando texto...'):
        # Convertir imagen para el lector
        img_np = np.array(imagen)
        resultado = reader.readtext(img_np, detail=0)
        texto_extraido = "\n".join(resultado)
        
    # Mostrar el texto extraído para que el usuario lo edite si es necesario
    st.subheader("Texto extraído (puedes editarlo):")
    texto_final = st.text_area("Información capturada:", valor=texto_extraido, height=200)

    # 2. Generar el archivo Word
    if st.button("Generar Archivo Word"):
        doc = Document()
        doc.add_heading('PLAN DE CLASE / TUTORÍA', 0)
        
        # Aquí puedes diseñar la estructura de tu formato
        doc.add_heading('Información Extraída:', level=1)
        doc.add_paragraph(texto_final)
        
        # Guardar en memoria para descarga
        buffer = io.BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        
        st.download_button(
            label="📥 Descargar Documento Word",
            data=buffer,
            file_name="Plan_Clase_Generado.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
