import re
from collections import Counter
import streamlit as st

# Configuración visual
st.set_page_config(
    page_title="TextSEO — Análisis de Texto & SEO",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Enlace de afiliado
URL_AFILIADO_IA = "https://writesonic.com?via=tu_id"

# Estilos CSS: Colores limpios, tranquilos y diseño simétrico
st.markdown(
    """
    <style>
    /* Estilo general */
    .main {
        background-color: #f8fafc;
    }
    
    /* Encabezado minimalista */
    .title-text {
        text-align: center;
        font-size: 2.2rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.2rem;
        letter-spacing: -0.02em;
    }
    .subtitle-text {
        text-align: center;
        font-size: 0.95rem;
        color: #64748b;
        margin-bottom: 1.8rem;
    }

    /* Banner compacto y sutil */
    .compact-banner {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 3px solid #3b82f6;
        border-radius: 8px;
        padding: 10px 18px;
        margin-top: 12px;
        margin-bottom: 24px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .compact-banner-text {
        font-size: 0.88rem;
        color: #334155;
    }
    .compact-banner-text strong {
        color: #0f172a;
    }
    .compact-btn {
        background-color: #f1f5f9;
        color: #2563eb !important;
        padding: 6px 14px;
        border-radius: 6px;
        font-size: 0.82rem;
        font-weight: 600;
        text-decoration: none;
        border: 1px solid #cbd5e1;
        white-space: nowrap;
    }

    /* Tarjetas de métricas simétricas */
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 14px;
        text-align: center;
    }
    .metric-value {
        font-size: 1.4rem;
        font-weight: 700;
        color: #0f172a;
    }
    .metric-label {
        font-size: 0.75rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 2px;
    }

    /* Pie de página */
    .footer-legal {
        text-align: center;
        color: #94a3b8;
        font-size: 0.8rem;
        margin-top: 60px;
        padding-top: 20px;
        border-top: 1px solid #e2e8f0;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Encabezado
st.markdown(
    '<div class="title-text">TextSEO</div>', unsafe_allow_html=True
)
st.markdown(
    '<div class="subtitle-text">Análisis de texto, densidad y métricas en tiempo real.</div>',
    unsafe_allow_html=True,
)

# Espacio de trabajo principal (Funcionalidad prioritaria)
text_input = st.text_area(
    "Área de texto",
    height=210,
    placeholder="Escribe o pega tu texto aquí para analizarlo al instante...",
    label_visibility="collapsed",
)

# Banner sutil debajo del editor
st.markdown(
    f"""
    <div class="compact-banner">
        <div class="compact-banner-text">
            💡 <strong>Sugerencia:</strong> ¿Necesitas redactar borradores largos? Prueba generar artículos con IA.
        </div>
        <a href="{URL_AFILIADO_IA}" target="_blank" class="compact-btn">Probar herramienta →</a>
    </div>
""",
    unsafe_allow_html=True,
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
    "when",
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

# Resultados y herramientas
if text_input:
    words = re.findall(r"\b\w+\b", text_input.lower())
    total_words = len(words)
    total_chars = len(text_input)
    total_chars_no_spaces = len(text_input.replace(" ", ""))
    sentences = len(re.split(r"[.!?]+", text_input)) - 1
    sentences = max(1, sentences) if total_words > 0 else 0
    reading_time = round(total_words / 200, 1)

    # Bloque de métricas
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(
            f'<div class="metric-card"><div class="metric-value">{total_words}</div><div class="metric-label">Palabras</div></div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f'<div class="metric-card"><div class="metric-value">{total_chars}</div><div class="metric-label">Caracteres</div></div>',
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f'<div class="metric-card"><div class="metric-value">{total_chars_no_spaces}</div><div class="metric-label">Sin Espacios</div></div>',
            unsafe_allow_html=True,
        )
    with col4:
        st.markdown(
            f'<div class="metric-card"><div class="metric-value">{sentences}</div><div class="metric-label">Oraciones</div></div>',
            unsafe_allow_html=True,
        )
    with col5:
        st.markdown(
            f'<div class="metric-card"><div class="metric-value">~{reading_time}</div><div class="metric-label">Min. Lectura</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(
        ["🎯 Densidad SEO", "🔄 Formato de Texto", "🔗 Slug de URL"]
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
                    f'<div class="metric-card"><b>{word.capitalize()}</b><br><span style="color:#64748b; font-size:0.85rem;">{count} veces ({density}%)</span></div>',
                    unsafe_allow_html=True,
                )
        else:
            st.info("Escribe un texto más largo para analizar la densidad de palabras clave.")

    with tab2:
        col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
        if col_btn1.button("MAYÚSCULAS", use_container_width=True):
            st.text_area("Resultado", text_input.upper(), height=120, label_visibility="collapsed")
        if col_btn2.button("minúsculas", use_container_width=True):
            st.text_area("Resultado", text_input.lower(), height=120, label_visibility="collapsed")
        if col_btn3.button("Modo Título", use_container_width=True):
            st.text_area("Resultado", text_input.title(), height=120, label_visibility="collapsed")
        if col_btn4.button("Limpiar Espacios", use_container_width=True):
            st.text_area("Resultado", " ".join(text_input.split()), height=120, label_visibility="collapsed")

    with tab3:
        raw_slug = text_input.split("\n")[0]
        slug = re.sub(r"[^\w\s-]", "", raw_slug.lower())
        slug = re.sub(r"[-\s]+", "-", slug).strip("-")
        st.code(
            slug if slug else "escribe-un-titulo-para-generar-el-slug",
            language="text",
        )

# Pie de página
st.markdown(
    """
    <div class="footer-legal">
        TextSEO © 2026 — Herramienta gratuita de análisis de texto.
    </div>
""",
    unsafe_allow_html=True,
)
