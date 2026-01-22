import streamlit as st
import pandas as pd
import yfinance as yf

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="App Financiera Vzla", page_icon="🇻🇪", layout="centered")

# --- ESTILOS VISUALES ---
st.markdown("""
    <style>
    .stMetric { background-color: #f0f2f6; border-radius: 10px; padding: 10px; }
    h1, h2, h3 { color: #0e1117; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIONES INTERNAS (CORREGIDA) ---
def obtener_historia(simbolo, p_tiempo="1mo"):
    """Descarga datos reales de Yahoo Finance"""
    try:
        ticker = yf.Ticker(simbolo)
        # CORRECCIÓN: Usamos la variable p_tiempo correctamente
        hist = ticker.history(period=p_tiempo)
        
        # Validación de datos vacíos
        if hist.empty:
            return None, 0, 0
        
        precio_actual = hist['Close'].iloc[-1]
        precio_ayer = hist['Open'].iloc[-1]
        cambio = ((precio_actual - precio_ayer) / precio_ayer) * 100
        return hist['Close'], precio_actual, cambio
    except Exception as e:
        # Si falla, no rompemos la app, devolvemos 0
        return None, 0, 0

# --- BARRA LATERAL (Navegación) ---
st.sidebar.title("🇻🇪 Finanzas Vzla")
opcion = st.sidebar.radio("Menú:", ["Mercado & Gráficos", "Noticias Flash", "Academia", "Calculadora P2P"])

# Filtro de tiempo
if opcion == "Mercado & Gráficos":
    st.sidebar.markdown("---")
    st.sidebar.subheader("📅 Tiempo")
    # Selector de tiempo
    lapso = st.sidebar.selectbox("Ver:", ["1d", "5d", "1mo", "6mo", "1y"], index=2)
else:
    lapso = "1mo"

# --- SECCIÓN 1: MERCADO ---
if opcion == "Mercado & Gráficos":
    st.title("📈 Mercado en Vivo")
    
    tab1, tab2 = st.tabs(["Cripto", "Bolsa USA"])

    with tab1:
        st.subheader("Bitcoin (BTC)")
        # Llamamos a la función con el lapso seleccionado
        hist_btc, precio_btc, cambio_btc = obtener_historia("BTC-USD", lapso)
        
        st.metric("Precio Actual", f"${precio_btc:,.2f}", f"{cambio_btc:.2f}%")
        
        if hist_btc is not None:
            st.line_chart(hist_btc)
        else:
            st.warning("⏳ Cargando datos... (Si tarda mucho, Yahoo puede estar lento)")

    with tab2:
        st.subheader("S&P 500")
        hist_sp, precio_sp, cambio_sp = obtener_historia("^GSPC", lapso)
        
        st.metric("Precio Actual", f"${precio_sp:,.2f}", f"{cambio_sp:.2f}%")
        
        if hist_sp is not None:
            st.line_chart(hist_sp)

# --- SECCIÓN 2: NOTICIAS ---
elif opcion == "Noticias Flash":
    st.title("📰 Lo Importante")
    
    st.info("Resumen de lo que mueve el dinero hoy.")
    
    noticias = [
        {"t": "Bitcoin: ¿Oportunidad?", "d": "El precio muestra estabilidad. Analistas sugieren acumular antes del próximo 'halving'."},
        {"t": "Dólar vs Inflación", "d": "La inflación global persiste. Mantener ahorros en moneda dura (USDT/USD) sigue siendo la estrategia defensiva."},
        {"t": "Petróleo y Energía", "d": "Conflictos globales mantienen el precio de la energía alto, afectando los costos de transporte."}
    ]

    for n in noticias:
        with st.expander(n['t']):
            st.write(n['d'])

# --- SECCIÓN 3: ACADEMIA ---
elif opcion == "Academia":
    st.title("🎓 Escuela de Inversión")
    
    st.markdown("""
    ### 3 Reglas de Oro
    1.  **Nunca inviertas dinero que necesites para comer.** La inversión es a largo plazo.
    2.  **No persigas velas verdes.** Si algo ya subió mucho hoy, espera a que baje (corrección) para comprar.
    3.  **Ten paciencia.** El dinero rápido suele ser estafa. El interés compuesto toma tiempo.
    """)

# --- SECCIÓN 4: CALCULADORA ---
elif opcion == "Calculadora P2P":
    st.title("🧮 Calculadora Vzla")
    
    col1, col2 = st.columns(2)
    with col1:
        bs = st.number_input("Bolívares:", value=1000.0)
    with col2:
        tasa = st.number_input("Tasa Cambio:", value=60.0)
    
    if tasa > 0:
        usdt = bs / tasa
        st.success(f"Son: **${usdt:.2f} USDT**")
        st.caption("Usa Binance P2P o El Dorado para esta conversión.")
