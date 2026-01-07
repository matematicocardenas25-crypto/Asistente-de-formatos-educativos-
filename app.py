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

# --- CONFIGURACIÓN Y ESTILO ---
st.set_page_config(page_title="Asistente Prof. Cárdenas - Multidimensión", layout="wide")
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

# --- PESTAÑAS ---
tab1, tab2 = st.tabs(["📄 Planificación (Formato Original)", "📊 Calculadora y Gráficos Multidimensión"])

with tab1:
    st.title("Generador de Programación Didáctica")
    # (Aquí se mantiene todo el código del formulario anterior del Plan de Clase...)
    st.info("Complete los datos para generar el Word con Arial 12 y todos los puntos oficiales.")

# --- PESTAÑA 2: CALCULADORA Y GRAFICADOR MULTIDIMENSIÓN ---
with tab2:
    st.header("📊 Graficador de Múltiples Dimensiones")
    
    tipo_dim = st.radio("Seleccione Dimensión:", ["2D (Plano)", "3D (Espacial)", "Multivariable (Estadística)"], horizontal=True)

    if tipo_dim == "2D (Plano)":
        col1, col2 = st.columns([1, 2])
        with col1:
            func = st.text_input("f(x) =", "np.sin(x) * np.exp(-0.1*x)")
            rango = st.slider("Rango X", -50, 50, (-10, 10))
            color = st.color_picker("Color", "#1976D2")
        with col2:
            x = np.linspace(rango[0], rango[1], 500)
            y = eval(func)
            fig = px.line(x=x, y=y, title=f"Gráfico 2D: {func}")
            fig.update_traces(line_color=color)
            st.plotly_chart(fig, use_container_width=True)

    elif tipo_dim == "3D (Espacial)":
        st.subheader("Visualización de Superficies f(x, y)")
        col1, col2 = st.columns([1, 2])
        with col1:
            func_3d = st.text_input("z = f(x, y)", "np.sin(np.sqrt(x**2 + y**2))")
            res = st.slider("Resolución", 20, 100, 50)
        with col2:
            x = np.linspace(-5, 5, res)
            y = np.linspace(-5, 5, res)
            X, Y = np.meshgrid(x, y)
            Z = eval(func_3d, {"np": np, "x": X, "y": Y})
            
            fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Viridis')])
            fig.update_layout(title=f"Superficie 3D: {func_3d}", scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'))
            st.plotly_chart(fig, use_container_width=True)

    elif tipo_dim == "Multivariable (Estadística)":
        st.subheader("Comparación de Múltiples Series de Datos")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.write("Ingrese valores para comparar dimensiones (Series):")
            serie1 = st.text_input("Serie A (ej: Ventas)", "10, 20, 30, 40")
            serie2 = st.text_input("Serie B (ej: Costos)", "15, 18, 25, 38")
            nombres = st.text_input("Etiquetas", "Ene, Feb, Mar, Abr")
        with col2:
            labels = [i.strip() for i in nombres.split(',')]
            y1 = [float(i) for i in serie1.split(',')]
            y2 = [float(i) for i in serie2.split(',')]
            
            fig = go.Figure()
            fig.add_trace(go.Bar(x=labels, y=y1, name='Serie A', marker_color='#1976D2'))
            fig.add_trace(go.Bar(x=labels, y=y2, name='Serie B', marker_color='#FF5733'))
            fig.update_layout(barmode='group', title="Gráfico Estadístico Multivariable")
            st.plotly_chart(fig, use_container_width=True)

    st.success("💡 Para usar en tu Word: Usa el botón de la cámara en el gráfico para descargar la imagen (.png).")
