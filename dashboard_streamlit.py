# Dashboard con Streamlit y FakeStoreAPI

"""
Este proyecto es una versión del dashboard interactivo usando Streamlit en lugar de Tkinter.
Permite visualizar los productos obtenidos desde FakeStoreAPI, filtrarlos por categoría,
mostrar tablas y generar gráficos interactivos.

Librerías necesarias:
- streamlit
- pandas
- matplotlib
- requests

Instalación:
    pip install streamlit pandas matplotlib requests

Para ejecutar:
    streamlit run dashboard_streamlit.py

"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests

# =============================
# FUNCIONES
# =============================

def obtener_datos_api():
    """
    Obtiene los datos de productos desde la FakeStoreAPI.
    Retorna un DataFrame con la información estructurada.
    """
    url = "https://fakestoreapi.com/products"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data)
        return df
    except requests.exceptions.RequestException as e:
        st.error(f"No se pudo conectar a la API: {e}")
        return pd.DataFrame()

# =============================
# DASHBOARD CON STREAMLIT
# =============================

def main():
    st.set_page_config(page_title="Dashboard Productos", layout="wide")
    st.title("📊 Dashboard de Productos - FakeStoreAPI")

    df = obtener_datos_api()
    if df.empty:
        return

    # Sidebar - Filtros
    categorias = df['category'].unique()
    categoria_seleccionada = st.sidebar.selectbox("Selecciona una categoría:", ["Todas"] + list(categorias))

    if categoria_seleccionada != "Todas":
        df = df[df['category'] == categoria_seleccionada]

    st.subheader("📋 Tabla de productos")
    st.dataframe(df[['title', 'category', 'price']])

    # Visualizaciones
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Cantidad de productos por categoría")
        conteo = df['category'].value_counts()
        fig1, ax1 = plt.subplots()
        conteo.plot(kind='bar', color='skyblue', edgecolor='black', ax=ax1)
        ax1.set_ylabel("Cantidad")
        ax1.set_xlabel("Categoría")
        ax1.set_title("Productos por categoría")
        plt.xticks(rotation=45)
        st.pyplot(fig1)

    with col2:
        st.subheader("Precio promedio por categoría")
        promedio = df.groupby('category')['price'].mean()
        fig2, ax2 = plt.subplots()
        promedio.plot(kind='bar', color='lightgreen', edgecolor='black', ax=ax2)
        ax2.set_ylabel("Precio promedio (USD)")
        ax2.set_xlabel("Categoría")
        ax2.set_title("Precios promedio")
        plt.xticks(rotation=45)
        st.pyplot(fig2)

    # Detalles del producto
    st.subheader("🔍 Detalles de un producto")
    producto = st.selectbox("Selecciona un producto:", df['title'].values)
    producto_seleccionado = df[df['title'] == producto].iloc[0]

    st.markdown(f"**Categoría:** {producto_seleccionado['category']}")
    st.markdown(f"**Precio:** ${producto_seleccionado['price']:.2f}")
    st.markdown(f"**Descripción:** {producto_seleccionado['description']}")
    st.image(producto_seleccionado['image'], width=150)

if __name__ == "__main__":
    main()
