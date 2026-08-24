import re
from collections import Counter
import streamlit as st

# Configuración de página
st.set_page_config(
    page_title="TextSEO - Contador de Palabras y Herramientas SEO",
    page_icon="📝",
    layout="wide",
)

# Enlaces de afiliado (los cambiarás por los tuyos más adelante)
URL_AFILIADO_IA = "https://writesonic.com?via=tu_id"

# Estilos CSS
st.markdown(
    """
    <style>
    .affiliate-banner-top {
        background: linear-gradient(90deg, #4f46e5 0%, #7c3aed 100%);
        color: white !important;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 25px;
    }
    .affiliate-banner-top h3 { color: white !important; margin-bottom: 8px; }
    .affiliate-banner-top p { color: #e0e7ff !important; margin-bottom: 15px; }
    .affiliate-btn {
        background-color: #ffffff;
        color: #4f46e5 !important;
        padding: 10px 24px;
        border-radius: 8px;
        font-weight: bold;
        text-decoration: none;
        display: inline-block;
    }
    .metric-card {
        background-color: #f1f3f5;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
    }
    .footer-legal {
        text-align: center;
        color: #888888;
        font-size: 0.85rem;
        margin-top: 40px;
        padding-top: 20px;
        border-top: 1px solid #eeeeee;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("📝 TextSEO: Contador de Palabras y Análisis de Texto")
st.write(
    "Herramienta gratuita para redactores, estudiantes y profesionales del marketing."
)

# Banner de Afiliado (IA)
st.markdown(
    f"""
    <div class="affiliate-banner-top">
        <h3>⚡ Redacta artículos completos de 1.500 palabras en 30 segundos con IA</h3>
        <p>Prueba gratis la mejor Inteligencia Artificial para crear contenidos y blogs SEO.</p>
        <a href="{URL_AFILIADO_IA}" target="_blank" class="affiliate-btn">✨ Probar Generador de Texto IA Gratis</a>
    </div>
""",
    unsafe_allow_html=True,
)

# Caja de texto
text_input = st.text_area(
    "Escribe o pega tu texto aquí:",
    height=200,
    placeholder="Introduce tu contenido...",
)

STOP_WORDS_ES = set([
    "de",
    "la",
    "que",
    "el",
    "en",
    "y",
    "a",
    "los",
    "del",
    "se",
    "las",
    "por",
    "un",
    "para",
    "con",
    "no",
    "una",
    "su",
    "al",
    "lo",
    "como",
    "más",
    "pero",
    "sus",
    "le",
    "ya",
    "o",
    "este",
    "sí",
    "porque",
    "esta",
    "son",
    "entre",
    "está",
    "cuando",
    "muy",
    "sin",
    "sobre",
    "también",
    "me",
    "hasta",
    "hay",
    "donde",
    "quien",
    "desde",
    "todo",
    "nos",
    "durante",
    "todos",
    "uno",
    "les",
    "ni",
    "contra",
    "otros",
    "ese",
    "eso",
    "ante",
    "ellos",
    "e",
    "esto",
    "mí",
    "antes",
    "algunos",
    "qué",
    "unos",
    "yo",
    "otro",
    "otras",
    "otra",
    "él",
    "tanto",
    "esa",
    "estos",
    "mucho",
    "quienes",
    "nada",
    "muchos",
    "cual",
    "poco",
    "ella",
    "estar",
    "estas",
    "algunas",
    "algo",
    "nosotros",
])

if text_input:
    words = re.findall(r"\b\w+\b", text_input.lower())
    total_words = len(words)
    total_chars = len(text_input)
    total_chars_no_spaces = len(text_input.replace(" ", ""))
    sentences = len(re.split(r"[.!?]+", text_input)) - 1
    sentences = max(1, sentences) if total_words > 0 else 0
    reading_time = round(total_words / 200, 1)

    st.subheader("📊 Métricas del Texto")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Palabras", total_words)
    col2.metric("Caracteres", total_chars)
    col3.metric("Sin Espacios", total_chars_no_spaces)
    col4.metric("Oraciones", sentences)
    col5.metric("Tiempo Lectura", f"~{reading_time} min")

    st.divider()

    tab1, tab2, tab3 = st.tabs(
        ["🎯 Densidad SEO", "🔄 Transformador", "🔗 Generador de Slug"]
    )

    with tab1:
        filtered_words = [w for w in words if w not in STOP_WORDS_ES and len(w) > 2]
        if filtered_words:
            counter = Counter(filtered_words)
            top_words = counter.most_common(8)

            cols = st.columns(4)
            for idx, (word, count) in enumerate(top_words):
                density = round((count / total_words) * 100, 2)
                cols[idx % 4].markdown(
                    f'<div class="metric-card"><b>{word.capitalize()}</b><br>{count} veces ({density}%)</div>',
                    unsafe_allow_html=True,
                )
        else:
            st.info("Escribe más palabras para analizar la densidad.")

    with tab2:
        col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
        if col_btn1.button("MAYÚSCULAS"):
            st.text_area("Resultado:", text_input.upper(), height=120)
        if col_btn2.button("minúsculas"):
            st.text_area("Resultado:", text_input.lower(), height=120)
        if col_btn3.button("Modo Título"):
            st.text_area("Resultado:", text_input.title(), height=120)
        if col_btn4.button("Limpiar Espacios"):
            st.text_area(
                "Resultado:", " ".join(text_input.split()), height=120
            )

    with tab3:
        raw_slug = text_input.split("\n")[0]
        slug = re.sub(r"[^\w\s-]", "", raw_slug.lower())
        slug = re.sub(r"[-\s]+", "-", slug).strip("-")
        st.code(
            slug if slug else "escribe-un-titulo-para-generar-el-slug",
            language="text",
        )

# Pie de página legal para AdSense
st.markdown(
    """
    <div class="footer-legal">
        TextSEO © 2026 - Herramienta gratuita de análisis de texto. | 
        <a href="#" style="color: #888;">Política de Privacidad</a> | 
        <a href="#" style="color: #888;">Términos del Servicio</a>
    </div>
""",
    unsafe_allow_html=True,
)
