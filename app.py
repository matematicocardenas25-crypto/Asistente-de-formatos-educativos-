# --- PESTAÑA 2: CALCULADORA Y GRAFICADOR MULTIDIMENSIÓN ---
with tab2:
    st.header("📊 Generador de Gráficos Multidimensión")
    st.write("Configura la dimensión y el tipo de gráfico. Luego descárgalo como imagen para tu documento.")
    
    # Selector de Dimensión
    dimension = st.radio("Seleccione la Dimensión del Gráfico:", ["2D (Plano)", "3D (Espacial)"], horizontal=True)
    
    col_g1, col_g2 = st.columns([1, 2])
    
    with col_g1:
        if dimension == "2D (Plano)":
            tipo = st.selectbox("Tipo de gráfico 2D", ["Matemático (y=f(x))", "Barras Estadísticas", "Distribución Normal"])
            color_graf = st.color_picker("Color del trazo", "#1976D2")
            
            if tipo == "Matemático (y=f(x))":
                ecuacion = st.text_input("Escribe la función (ej: x**3 - 2*x)", "x**2")
                x_range = st.slider("Rango de X", -100, 100, (-10, 10))
            elif tipo == "Distribución Normal":
                mu = st.number_input("Media (μ)", value=0.0)
                sigma = st.number_input("Desviación (σ)", value=1.0, min_value=0.1)
                
        else:  # Gráficos 3D
            st.info("Visualización de superficies z = f(x, y)")
            ecuacion_3d = st.text_input("Escribe la función (x, y)", "np.sin(np.sqrt(x**2 + y**2))")
            rango_3d = st.slider("Rango de la malla (X e Y)", 1, 50, 10)
            estilo_3d = st.selectbox("Escala de colores", ["Viridis", "Plasma", "Turbo", "Blues"])

    with col_g2:
        fig = go.Figure()

        if dimension == "2D (Plano)":
            if tipo == "Matemático (y=f(x))":
                x = np.linspace(x_range[0], x_range[1], 500)
                y = eval(ecuacion.replace('x', 'x'))
                fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(color=color_graf, width=3)))
                fig.update_layout(title=f"Gráfico 2D: f(x) = {ecuacion}")

            elif tipo == "Distribución Normal":
                x = np.linspace(mu - 4*sigma, mu + 4*sigma, 200)
                y = (1/(sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu)/sigma)**2)
                fig.add_trace(go.Scatter(x=x, y=y, fill='tozeroy', line=dict(color=color_graf)))
                fig.update_layout(title="Campana de Gauss (Distribución Normal)")

        else: # Generación 3D
            x = np.linspace(-rango_3d, rango_3d, 100)
            y = np.linspace(-rango_3d, rango_3d, 100)
            X, Y = np.meshgrid(x, y)
            try:
                Z = eval(ecuacion_3d)
                fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale=estilo_3d)])
                fig.update_layout(title=f"Superficie 3D: {ecuacion_3d}", scene=dict(
                    xaxis_title='Eje X', yaxis_title='Eje Y', zaxis_title='Eje Z'))
            except Exception as e:
                st.error(f"Error en la función 3D: {e}")

        st.plotly_chart(fig, use_container_width=True)
        st.caption("Utilice las herramientas del gráfico para rotar (en 3D) o descargar la captura.")
