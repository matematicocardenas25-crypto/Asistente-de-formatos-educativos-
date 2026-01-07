import streamlit as st
import easyocr
from docx import Document
from PIL import Image
import numpy as np
import io

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
