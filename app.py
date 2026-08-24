import re
from collections import Counter
import streamlit as st

# Configuración visual
st.set_page_config(
    page_title="TextSEO — Contador, Densidad SEO, Legibilidad y Meta Descripción",
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
        max-width: 850px;
        margin-left: auto;
        margin-right: auto;
    }

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
        border-color: #4f46e5 !important;
        box-shadow: 0 0 0 2px rgba(79,70,229,0.2) !important;
    }

    /* Banner de Afiliación llamativo de alto contraste */
    .vibrant-banner {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #d946ef 100%);
        border-radius: 12px;
        padding: 14px 22px;
        margin-top: 12px;
        margin-bottom: 28px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 4px 14px rgba(124, 58, 237, 0.22);
    }
    .vibrant-banner-text {
        font-size: 0.95rem;
        color: #ffffff !important;
        font-weight: 500;
    }
    .vibrant-banner-text strong {
        color: #fef08a !important;
    }
    .vibrant-btn {
        background-color: #ffffff;
        color: #4f46e5 !important;
        padding: 9px 18px;
        border-radius: 8px;
        font-size: 0.88rem;
        font-weight: 700;
        text-decoration: none;
        white-space: nowrap;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
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

# Cabecera
st.markdown('<div class="title-text">TextSEO</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle-text">Pega tu texto para obtener al instante <b>recuento preciso</b>, <b>densidad de palabras clave</b>, <b>nivel de legibilidad SEO</b>, <b>meta descripción automatizada</b> y <b>formato limpio</b>.</div>',
    unsafe_allow_html=True,
)

# Badges explicativos
st.markdown(
    """
    <div class="features-badges">
        <span class="badge-item">📊 Conteo & Tiempo de Lectura</span>
        <span class="badge-item">🎯 Densidad de Palabras Clave</span>
        <span class="badge-item">📖 Índice de Legibilidad SEO</span>
        <span class="badge-item">🏷️ Meta Descripción para Google</span>
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

# Banner destacado de alta conversión
st.markdown(
    f"""
    <div class="vibrant-banner">
        <div class="vibrant-banner-text">
            ⚡ <strong>¿Escribiendo un artículo largo?</strong> Genera borradores completos optimizados para SEO en segundos con IA.
        </div>
        <a href="{URL_AFILIADO_IA}" target="_blank" class="vibrant-btn">Probar IA Gratis →</a>
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

    # Tarjetas métricas
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

    # 5 Herramientas avanzadas organizadas por pestañas
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎯 Densidad SEO",
        "📖 Legibilidad & Estilo",
        "🏷️ Meta Descripción",
        "🔄 Formateador Rápido",
        "🔗 Slug URL",
    ])

    # 1. Densidad
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
                "Escribe un texto más largo para generar el informe de densidad de palabras clave."
            )

    # 2. Nueva función avanzada: Legibilidad y Estilo SEO
    with tab2:
        avg_words_per_sentence = (
            round(total_words / sentences, 1) if sentences > 0 else 0
        )
        col_l1, col_l2 = st.columns(2)

        with col_l1:
            st.write("### Promedio de palabras por oración")
            st.markdown(
                f'<div class="metric-card"><div class="metric-value">{avg_words_per_sentence}</div><div class="metric-label">Palabras / Oración</div></div>',
                unsafe_allow_html=True,
            )

        with col_l2:
            st.write("### Nivel de Complejidad SEO")
            if avg_words_per_sentence <= 15:
                st.success(
                    "🟢 **Fácil de leer:** Estructura óptima para retener usuarios y mejorar el SEO móvil."
                )
            elif avg_words_per_sentence <= 24:
                st.warning(
                    "🟡 **Dificultad Media:** Considera dividir algunas oraciones largas con puntos seguidos."
                )
            else:
                st.error(
                    "🔴 **Complejo:** Frases demasiado largas. Acórtalas para evitar abandonos de página."
                )

    # 3. Nueva función avanzada: Generador de Meta Descripción
    with tab3:
        st.write("### Snippet de Meta Descripción Sugerido (150-160 caracteres)")
        # Extrae los primeros 155 caracteres respetando palabras completas
        raw_snippet = text_input.replace("\n", " ").strip()
        meta_desc = (
            raw_snippet[:155].rsplit(" ", 1)[0] + "..."
            if len(raw_snippet) > 155
            else raw_snippet
        )

        st.text_area(
            "Copia tu Meta Descripción lista para Google:",
            meta_desc,
            height=80,
        )
        length_meta = len(meta_desc)
        if 130 <= length_meta <= 160:
            st.caption(
                f"✅ Longitud ideal: **{length_meta} caracteres** (Encaja perfectamente en los resultados de Google)."
            )
        else:
            st.caption(
                f"ℹ️ Longitud actual: **{length_meta} caracteres** (Recomendado entre 130 y 160 caracteres)."
            )

    # 4. Formateador
    with tab4:
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

    # 5. Slug URL
    with tab5:
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
