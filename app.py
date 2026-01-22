import streamlit as st
import pandas as pd
import yfinance as yf

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Finanzas Vzla Real", page_icon="🇻🇪", layout="centered")

# Estilos visuales
st.markdown("""
    <style>
    .stMetric { background-color: #f0f2f6; padding: 15px; border-radius: 10px; border: 1px solid #dcdcdc; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIÓN PARA OBTENER DATOS REALES ---
def obtener_datos(simbolo):
    try:
        ticker = yf.Ticker(simbolo)
        hist = ticker.history(period="1d")
        if not hist.empty:
            precio_actual = hist['Close'].iloc[-1]
            precio_ayer = hist['Open'].iloc[0]
            cambio = ((precio_actual - precio_ayer) / precio_ayer) * 100
            return precio_actual, cambio
    except:
        return 0, 0
    return 0, 0

# --- MENÚ LATERAL ---
st.sidebar.title("🚀 Menú")
opcion = st.sidebar.radio("Ir a:", ["Mercado en Vivo", "Academia Cripto", "Estrategia Venezuela"])

# --- SECCIÓN 1: MERCADO EN VIVO ---
if opcion == "Mercado en Vivo":
    st.title("📈 Mercado en Tiempo Real")
    st.markdown("Precios actualizados directamente desde la bolsa global.")

    # Botón para refrescar datos manualmente
    if st.button('🔄 Actualizar Precios'):
        st.cache_data.clear()

    # Obtener datos reales
    btc_precio, btc_cambio = obtener_datos("BTC-USD")
    eth_precio, eth_cambio = obtener_datos("ETH-USD")
    sp500_precio, sp500_cambio = obtener_datos("^GSPC") # S&P 500

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Bitcoin (BTC)", f"${btc_precio:,.2f}", f"{btc_cambio:.2f}%")
    with col2:
        st.metric("Ethereum (ETH)", f"${eth_precio:,.2f}", f"{eth_cambio:.2f}%")

    st.markdown("---")
    st.subheader("🇺🇸 Bolsa Tradicional")
    st.metric("S&P 500 (Economía EE.UU.)", f"${sp500_precio:,.2f}", f"{sp500_cambio:.2f}%")

    st.info("💡 Nota: Si ves el Bitcoin en rojo, suele ser buen momento para comprar 'en rebaja' si vas a largo plazo.")

# --- SECCIÓN 2: ACADEMIA ---
elif opcion == "Academia Cripto":
    st.title("🎓 Aprende Mientras Ganas")
    
    with st.expander("¿Qué mueve el precio hoy?"):
        st.write("""
        Los precios que ves en la pantalla principal se mueven por **Oferta y Demanda**:
        1. Si hay malas noticias (guerras, regulaciones), la gente vende y el precio baja 📉.
        2. Si hay adopción (ej. BlackRock compra Bitcoin), la gente compra y el precio sube 📈.
        """)

    with st.expander("Diccionario Básico"):
        st.markdown("""
        * **Bull Market (Toro):** Cuando todo sube. El toro ataca hacia arriba.
        * **Bear Market (Oso):** Cuando todo baja. El oso ataca hacia abajo.
        * **HODL:** Comprar y no vender, pase lo que pase.
        """)

# --- SECCIÓN 3: ESTRATEGIA VENEZUELA ---
elif opcion == "Estrategia Venezuela":
    st.title("🇻🇪 Desde Venezuela")
    st.subheader("Calculadora de Arbitraje Simple")
    st.markdown("Calcula el valor real de tu cambio.")

    monto_bs = st.number_input("Tengo esta cantidad de Bolívares:", value=1000.0)
    tasa_dolar = st.number_input("Precio del Dólar (P2P/Paralelo):", value=60.0)

    if tasa_dolar > 0:
        dolares = monto_bs / tasa_dolar
        st.success(f"Esto equivale a: **${dolares:.2f} USDT**")
        
        st.write("Si inviertes estos USDT en Bitcoin y sube un 10%:")
        ganancia = dolares * 1.10
        st.metric(label="Futuro Potencial", value=f"${ganancia:.2f} USDT")

# --- PIE DE PÁGINA ---
st.markdown("---")
st.caption("Datos provistos por Yahoo Finance. Desarrollado con Streamlit.")
