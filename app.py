import streamlit as st
import pandas as pd
import random
from datetime import datetime

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Finanzas Desde Cero", page_icon="📈", layout="centered")

# Estilos CSS para que parezca una app móvil limpia
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 20px; }
    .big-font { font-size:20px !important; font-weight: bold; }
    .stMetric { background-color: #f0f2f6; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- MENÚ DE NAVEGACIÓN (SIDEBAR) ---
st.sidebar.title("🚀 Navegación")
opcion = st.sidebar.radio("Ir a:", ["Inicio & Mercado", "Noticias Flash", "Academia (Aprende)", "Modo Venezuela"])

# --- DATOS SIMULADOS (Para el prototipo) ---
# En una versión avanzada, aquí conectaríamos con APIs reales como Yahoo Finance o CoinGecko
btc_price = 42000 + random.randint(-500, 500)
eth_price = 2200 + random.randint(-50, 50)
sp500 = 4700 + random.randint(-20, 20)

# --- SECCIÓN 1: INICIO & MERCADO ---
if opcion == "Inicio & Mercado":
    st.title("📊 Mercado al Día")
    st.markdown("Tu visor rápido de cómo se mueve el dinero hoy.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Bitcoin (BTC)", value=f"${btc_price:,}", delta=f"{random.choice(['+','-'])}{random.randint(1,5)}%")
    with col2:
        st.metric(label="S&P 500", value=f"${sp500}", delta=f"{random.choice(['+','-'])}{random.randint(0,2)}%")

    st.subheader("💡 ¿Por qué se mueve hoy?")
    st.info("El mercado reacciona hoy a los datos de inflación en EE.UU. Cuando la inflación baja, las acciones suelen subir.")

# --- SECCIÓN 2: NOTICIAS FLASH ---
elif opcion == "Noticias Flash":
    st.title("📰 Lo que mueve la aguja")
    st.markdown("Resumen curado para entender el ruido mundial.")

    noticias = [
        {"titulo": "La SEC aprueba nuevo ETF", "impacto": "Alto", "resumen": "Esto permite que fondos tradicionales inviertan en Bitcoin, trayendo más dinero al mercado."},
        {"titulo": "Inflación en Europa cede", "impacto": "Medio", "resumen": "Buenas noticias para el Euro. Podría hacer que el Dólar baje ligeramente."},
        {"titulo": "Halving de Bitcoin se acerca", "impacto": "Muy Alto", "resumen": "Históricamente, este evento reduce la oferta de Bitcoin y sube el precio."}
    ]

    for n in noticias:
        with st.expander(f"{n['titulo']} (Impacto: {n['impacto']})"):
            st.write(n['resumen'])
            st.caption("Fuente: Agregador Global")

# --- SECCIÓN 3: ACADEMIA (APRENDE) ---
elif opcion == "Academia (Aprende)":
    st.title("🎓 Escuela de Inversión")
    st.markdown("Aprende paso a paso sin tecnicismos.")

    tab1, tab2, tab3 = st.tabs(["Nivel 1: Básico", "Nivel 2: Cripto", "Nivel 3: Bolsa"])

    with tab1:
        st.header("Conceptos Fundamentales")
        st.markdown("""
        **1. ¿Qué es la inflación?**
        Es el impuesto invisible. Si tienes 100 Bolívares hoy, mañana compran menos. Invertir es la única forma de protegerte.
        
        **2. Interés Compuesto**
        Es ganar intereses sobre tus intereses. Es la bola de nieve que te hace rico con el tiempo.
        """)
    
    with tab2:
        st.header("Mundo Blockchain")
        st.markdown("""
        **¿Qué es una Wallet?**
        No es una cuenta de banco. Es como tu billetera física, tú eres el único dueño. Si pierdes las llaves (frase semilla), pierdes el dinero.
        
        **Stablecoins (USDT/USDC):**
        Criptomonedas que valen siempre $1. Son tu refugio digital contra la devaluación local.
        """)

# --- SECCIÓN 4: MODO VENEZUELA ---
elif opcion == "Modo Venezuela":
    st.title("🇻🇪 Ruta Venezolana")
    st.markdown("Estrategias específicas para operar desde aquí.")

    st.warning("⚠️ Regla de Oro: Nunca inviertas dinero que necesites para comer la próxima semana.")

    st.subheader("El Ciclo del Dinero (Ejemplo)")
    st.code("Bolívares -> Binance P2P (Comprar USDT) -> Inversión (Bitcoin/Acciones)")

    st.subheader("Herramientas Útiles")
    st.markdown("""
    * **Binance P2P:** Para cambiar Bs a Dólares Digitales.
    * **El Dorado / Reserve:** Billeteras fáciles para pagos rápidos.
    * **Interactive Brokers:** (Nivel Avanzado) Para acciones de EE.UU., aunque requiere más papeleo desde Vzla.
    """)

# --- PIE DE PÁGINA ---
st.markdown("---")
st.caption("Desarrollado para educar y crecer. No es asesoramiento financiero profesional.")
