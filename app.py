import streamlit as st
import pandas as pd
import yfinance as yf

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="App Financiera Vzla", page_icon="🇻🇪", layout="centered")

# --- ESTILOS (Para que se vea bien en celular) ---
st.markdown("""
    <style>
    .stMetric { background-color: #f0f2f6; border-radius: 10px; padding: 10px; }
    h1, h2, h3 { color: #0e1117; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIONES INTERNAS (El motor de la app) ---
def obtener_historia(simbolo, periodo="1mo"):
    """Descarga datos reales de Yahoo Finance"""
    try:
        ticker = yf.Ticker(simbolo)
        hist = ticker.history(period=period)
        # Si descarga datos vacíos, devolvemos 'None' para evitar errores
        if hist.empty:
            return None, 0, 0
        
        precio_actual = hist['Close'].iloc[-1]
        precio_ayer = hist['Open'].iloc[-1]
        cambio = ((precio_actual - precio_ayer) / precio_ayer) * 100
        return hist['Close'], precio_actual, cambio
    except:
        return None, 0, 0

# --- BARRA LATERAL (Navegación) ---
st.sidebar.title("🇻🇪 Finanzas Vzla")
st.sidebar.write("Tu centro de control financiero.")

opcion = st.sidebar.radio("Menú Principal:", 
    ["Mercado & Gráficos", "Noticias Flash", "Academia", "Calculadora P2P"])

# Filtro de tiempo (Solo aparece en la sección de mercado)
if opcion == "Mercado & Gráficos":
    st.sidebar.markdown("---")
    st.sidebar.subheader("📅 Tiempo del Gráfico")
    periodo = st.sidebar.selectbox("Ver:", ["1d", "5d", "1mo", "6mo", "1y"], index=2)
else:
    periodo = "1mo" # Valor por defecto para que no falle

# --- SECCIÓN 1: MERCADO Y GRÁFICOS ---
if opcion == "Mercado & Gráficos":
    st.title("📈 Mercado en Vivo")
    st.caption(f"Mostrando datos de: {periodo}")

    # Pestañas para organizar mejor en el celular
    tab1, tab2 = st.tabs(["Criptomonedas", "Bolsa USA"])

    with tab1:
        st.subheader("Bitcoin (BTC)")
        hist_btc, precio_btc, cambio_btc = obtener_historia("BTC-USD", periodo)
        
        # Mostramos el precio
        st.metric("Precio Actual", f"${precio_btc:,.2f}", f"{cambio_btc:.2f}%")
        
        # Mostramos el gráfico (Validamos que existan datos)
        if hist_btc is not None:
            st.line_chart(hist_btc)
        else:
            st.warning("⏳ Cargando gráfico o error de conexión...")

    with tab2:
        st.subheader("S&P 500 (Economía Global)")
        hist_sp, precio_sp, cambio_sp = obtener_historia("^GSPC", periodo)
        
        st.metric("Precio Actual", f"${precio_sp:,.2f}", f"{cambio_sp:.2f}%")
        
        if hist_sp is not None:
            st.line_chart(hist_sp)
        else:
            st.warning("⏳ Cargando gráfico o error de conexión...")

# --- SECCIÓN 2: NOTICIAS (Regresaron!) ---
elif opcion == "Noticias Flash":
    st.title("📰 Lo Importante Hoy")
    
    noticias = [
        {"titulo": "Bitcoin y el Halving", "tipo": "Cripto", "info": "El evento que reduce la oferta de Bitcoin suele aumentar su precio a largo plazo."},
        {"titulo": "Inflación en Dólares", "tipo": "Economía", "info": "El dólar también pierde valor. Mantener efectivo quieto es perder poder de compra."},
        {"titulo": "USDT en Venezuela", "tipo": "Local", "info": "El uso de USDT supera al efectivo en muchas transacciones comerciales grandes."}
    ]

    for n in noticias:
        with st.expander(f"{n['tipo']} | {n['titulo']}"):
            st.write(n['info'])

# --- SECCIÓN 3: ACADEMIA ---
elif opcion == "Academia":
    st.title("🎓 Aprende a Invertir")
    st.markdown("""
    ### Conceptos Clave
    
    **1. Volatilidad:**
    Es qué tanto sube y baja el precio. 
    * *Cripto:* Alta volatilidad (riesgo alto, ganancia alta).
    * *Bonos:* Baja volatilidad (seguridad, ganancia baja).
    
    **2. Diversificación:**
    "No poner todos los huevos en la misma canasta". Si el Bitcoin baja, quizás tus acciones suban.
    """)

# --- SECCIÓN 4: CALCULADORA ---
elif opcion == "Calculadora P2P":
    st.title("🧮 Calculadora de Cambio")
    st.write("Herramienta rápida para arbitraje.")

    col1, col2 = st.columns(2)
    with col1:
        bs = st.number_input("Tengo Bolívares:", value=1000)
    with col2:
        tasa = st.number_input("Tasa de Cambio:", value=60.0)
    
    if tasa > 0:
        res = bs / tasa
        st.success(f"Son: **${res:.2f} USDT**")
