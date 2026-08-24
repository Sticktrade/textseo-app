import re
from collections import Counter
import streamlit as st

# Configuración visual
st.set_page_config(
    page_title="TextSEO — Contador de Palabras, Densidad SEO y Formateador",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Enlace de afiliado
URL_AFILIADO_IA = "https://writesonic.com?via=tu_id"

# Estilos CSS
st.markdown(
    """
    <style>
    .stApp, .main, [data-testid="stAppViewContainer"] {
        background-color: #f8fafc !important;
        color: #0f172a !important;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .title-text {
        text-align: center;
        font-size: 3.5rem;
        font-weight: 800;
        color: #0f172a;
        margin-top: 0.5rem;
        margin-bottom: 0.2rem;
        letter-spacing: -0.03em;
        line-height: 1.1;
    }
    
    .subtitle-text {
        text-align: center;
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 1.5rem;
        font-weight: 400;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
    }

    /* Badges con los beneficios exactos */
    .features-badges {
        display: flex;
        justify-content: center;
        gap: 10px;
        flex-wrap: wrap;
        margin-bottom: 2rem;
    }
    .badge-item {
        background-color: #ffffff;
        border: 1px solid #cbd5e1;
        color: #334155;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02);
    }

    .stTextArea textarea {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 10px !important;
        font-size: 1rem !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02) !important;
    }
    .stTextArea textarea:focus {
        border-color: #2563eb !important;
        box-shadow: 0 0 0 2px rgba(37,99,235,0.2) !important;
    }

    .compact-banner {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #2563eb;
        border-radius: 10px;
        padding: 12px 20px;
        margin-top: 10px;
        margin-bottom: 28px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    .compact-banner-text {
        font-size: 0.92rem;
        color: #334155;
    }
    .compact-banner-text strong {
        color: #0f172a;
    }
    .compact-btn {
        background-color: #eff6ff;
        color: #2563eb !important;
        padding: 8px 16px;
        border-radius: 8px;
        font-size: 0.85rem;
        font-weight: 600;
        text-decoration: none;
        border: 1px solid #bfdbfe;
        white-space: nowrap;
    }

    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02);
    }
    .metric-value {
        font-size: 1.6rem;
        font-weight: 800;
        color: #0f172a;
    }
    .metric-label {
        font-size: 0.75rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 4px;
        font-weight: 600;
    }

    .footer-legal {
        text-align: center;
        color: #94a3b8;
        font-size: 0.85rem;
        margin-top: 60px;
        padding-top: 20px;
        border-top: 1px solid #e2e8f0;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Cabecera directa
st.markdown('<div class="title-text">TextSEO</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle-text">Pega tu texto abajo y calcula al instante la <b>extensión exacta</b>, detecta <b>palabras repetidas para SEO</b>, <b>limpia el formato</b> y genera la <b>URL (slug)</b> de tu artículo.</div>',
    unsafe_allow_html=True,
)

# Badges explicativos directos
st.markdown(
    """
    <div class="features-badges">
        <span class="badge-item">📊 Conteo & Tiempo de lectura</span>
        <span class="badge-item">🎯 Porcentaje de Palabras Clave</span>
        <span class="badge-item">🔄 Corrector de Formato</span>
        <span class="badge-item">🔗 Generador de Slug Web</span>
    </div>
""",
    unsafe_allow_html=True,
)

# Entrada de texto
text_input = st.text_area(
    "Área de texto",
    height=210,
    placeholder="Pega aquí tu escrito o artículo...",
    label_visibility="collapsed",
)

# Banner sutil
st.markdown(
    f"""
    <div class="compact-banner">
        <div class="compact-banner-text">
            💡 <strong>Sugerencia:</strong> ¿Necesitas redactar borradores largos desde cero? Genera artículos completos con IA.
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
            f'<div class="metric-card"><div class="metric-value">~{reading_time} min</div><div class="metric-label">Lectura</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs([
        "🎯 Palabras Clave & Densidad SEO",
        "🔄 Formateador Rápido",
        "🔗 Generador de Slug URL",
    ])

    with tab1:
        filtered_words = [
            w for w in words if w not in STOP_WORDS_ES and len(w) > 2
        ]
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
            st.info(
                "Escribe o pega un texto más largo para mostrar el análisis de densidad SEO."
            )

    with tab2:
        col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
        if col_btn1.button("Convertir a MAYÚSCULAS", use_container_width=True):
            st.text_area(
                "Resultado",
                text_input.upper(),
                height=120,
                label_visibility="collapsed",
            )
        if col_btn2.button("Convertir a minúsculas", use_container_width=True):
            st.text_area(
                "Resultado",
                text_input.lower(),
                height=120,
                label_visibility="collapsed",
            )
        if col_btn3.button("Modo Título", use_container_width=True):
            st.text_area(
                "Resultado",
                text_input.title(),
                height=120,
                label_visibility="collapsed",
            )
        if col_btn4.button("Quitar Espacios Dobles", use_container_width=True):
            st.text_area(
                "Resultado",
                " ".join(text_input.split()),
                height=120,
                label_visibility="collapsed",
            )

    with tab3:
        raw_slug = text_input.split("\n")[0]
        slug = re.sub(r"[^\w\s-]", "", raw_slug.lower())
        slug = re.sub(r"[-\s]+", "-", slug).strip("-")
        st.code(
            slug if slug else "escribe-un-titulo-para-generar-el-slug",
            language="text",
        )

st.markdown(
    """
    <div class="footer-legal">
        TextSEO © 2026 — Herramienta gratuita de análisis de texto.
    </div>
""",
    unsafe_allow_html=True,
)
