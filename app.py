import streamlit as st
import pandas as pd
import yfinance as yf

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Finanzas Diagnóstico", page_icon="🔧", layout="centered")

# --- FUNCIÓN DE DIAGNÓSTICO ---
def obtener_historia(simbolo, periodo="1mo"):
    """Intenta descargar datos y si falla, muestra el error exacto"""
    try:
        # Paso 1: Intentar conectar
        ticker = yf.Ticker(simbolo)
        hist = ticker.history(period=period)
        
        # Paso 2: Verificar si llegaron datos
        if hist.empty:
            st.error(f"⚠️ Conexión exitosa, pero Yahoo devolvió datos VACÍOS para {simbolo}.")
            return None, 0, 0
            
        # Paso 3: Intentar procesar
        precio_actual = hist['Close'].iloc[-1]
        precio_ayer = hist['Open'].iloc[-1]
        cambio = ((precio_actual - precio_ayer) / precio_ayer) * 100
        
        return hist['Close'], precio_actual, cambio
        
    except Exception as e:
        # AQUÍ ESTÁ LA CLAVE: Imprimimos el error real en la pantalla
        st.error(f"🔴 Error Técnico en {simbolo}: {e}")
        return None, 0, 0

# --- INTERFAZ SIMPLIFICADA PARA PROBAR ---
st.title("🔧 Modo Diagnóstico")
st.write("Probando conexión con Yahoo Finance...")

if st.button("🔄 Probar Conexión Ahora"):
    st.write("---")
    
    # Prueba 1: Bitcoin
    st.subheader("Prueba 1: Bitcoin (BTC-USD)")
    hist_btc, precio, cambio = obtener_historia("BTC-USD")
    if hist_btc is not None:
        st.success(f"¡Éxito! Precio: {precio}")
        st.line_chart(hist_btc)
    
    st.write("---")
    
    # Prueba 2: Google (Acciones)
    st.subheader("Prueba 2: Google (GOOG)")
    hist_goog, precio_g, cambio_g = obtener_historia("GOOG")
    if hist_goog is not None:
        st.success(f"¡Éxito! Precio: {precio_g}")
        st.line_chart(hist_goog)

st.write("---")
st.info("Si ves una caja roja 🔴, por favor escríbeme qué dice el texto adentro.")
