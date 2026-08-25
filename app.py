import re
from collections import Counter
import streamlit as st
import streamlit.components.v1 as components

# Configuración visual
st.set_page_config(
    page_title="TextSEO — Contador, Densidad SEO, Legibilidad y Meta Descripción",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Inyección directa de Google Analytics 4 en la cabecera principal
components.html(
    """
    <script>
        const parentDoc = window.parent.document;
        if (!parentDoc.getElementById('ga-gtag-script')) {
            // Cargar archivo principal de Google
            const script1 = parentDoc.createElement('script');
            script1.id = 'ga-gtag-script';
            script1.async = true;
            script1.src = 'https://www.googletagmanager.com/gtag/js?id=G-DZCRWL55RY';
            parentDoc.head.appendChild(script1);

            // Inicializar medición con la URL completa de tu app
            const script2 = parentDoc.createElement('script');
            script2.innerHTML = `
                window.dataLayer = window.dataLayer || [];
                function gtag(){dataLayer.push(arguments);}
                gtag('js', new Date());
                gtag('config', 'G-DZCRWL55RY', {
                    'page_location': window.parent.location.href
                });
            `;
            parentDoc.head.appendChild(script2);
        }
    </script>
""",
    height=0,
)

# Inicializar estados de sesión
if "reviewed" not in st.session_state:
    st.session_state.reviewed = False
if "formatted_output" not in st.session_state:
    st.session_state.formatted_output = ""
if "scroll_target" not in st.session_state:
    st.session_state.scroll_target = None

# Enlaces de afiliados
URL_AFILIADO_IA_WRITING = "https://writesonic.com?via=tu_id"
URL_AFILIADO_PARAPHRASE = "https://quillbot.com?via=tu_id"
URL_AFILIADO_SEO_TOOL = "https://surferseo.com?via=tu_id"

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

    div[data-testid="stButton"] button {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 8px 16px !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
        transition: all 0.2s ease !important;
    }
    div[data-testid="stButton"] button:hover {
        background-color: #f1f5f9 !important;
        border-color: #2563eb !important;
        color: #2563eb !important;
    }

    div[data-testid="stButton"] button[kind="primary"] {
        background-color: #2563eb !important;
        color: #ffffff !important;
        border: none !important;
        font-size: 1.05rem !important;
    }
    div[data-testid="stButton"] button[kind="primary"]:hover {
        background-color: #1d4ed8 !important;
        color: #ffffff !important;
    }

    .affiliate-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 16px;
        margin-top: 18px;
        margin-bottom: 24px;
    }

    .aff-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 16px 18px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.03);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .aff-card-1 { border-top: 4px solid #6366f1; }
    .aff-card-2 { border-top: 4px solid #10b981; }
    .aff-card-3 { border-top: 4px solid #f59e0b; }

    .aff-title { font-size: 0.95rem; font-weight: 700; color: #0f172a; margin-bottom: 6px; }
    .aff-desc { font-size: 0.83rem; color: #64748b; margin-bottom: 14px; line-height: 1.35; }
    .aff-btn { text-align: center; padding: 8px 12px; border-radius: 6px; font-size: 0.82rem; font-weight: 700; text-decoration: none; display: block; }
    .aff-btn-1 { background-color: #eef2ff; color: #4f46e5 !important; border: 1px solid #c7d2fe; }
    .aff-btn-2 { background-color: #ecfdf5; color: #059669 !important; border: 1px solid #a7f3d0; }
    .aff-btn-3 { background-color: #fffbeb; color: #d97706 !important; border: 1px solid #fde68a; }

    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02);
    }
    .metric-value { font-size: 1.6rem; font-weight: 800; color: #0f172a; }
    .metric-label { font-size: 0.75rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 4px; font-weight: 600; }

    .section-explanation {
        font-size: 0.88rem;
        color: #64748b;
        margin-top: -6px;
        margin-bottom: 14px;
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
    '<div class="subtitle-text">Pega tu escrito, pulsa <b>Revisar</b> y analiza métricas de longitud, densidad de palabras clave, legibilidad y snippets SEO.</div>',
    unsafe_allow_html=True,
)

# Badges explicativos
st.markdown(
    """
    <div class="features-badges">
        <span class="badge-item">Conteo & Tiempo de Lectura</span>
        <span class="badge-item">Densidad de Palabras Clave</span>
        <span class="badge-item">Legibilidad & Complejidad</span>
        <span class="badge-item">Meta Descripción SEO</span>
        <span class="badge-item">Slug de URL Clean</span>
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

# BANNERS DE AFILIACIÓN
st.markdown(
    f"""
    <div class="affiliate-grid">
        <div class="aff-card aff-card-1">
            <div>
                <div class="aff-title">Generador de Contenido IA</div>
                <div class="aff-desc">Crea artículos completos de 1.500 palabras optimizados para SEO en 30 segundos.</div>
            </div>
            <a href="{URL_AFILIADO_IA_WRITING}" target="_blank" class="aff-btn aff-btn-1">Probar Generador IA →</a>
        </div>
        <div class="aff-card aff-card-2">
            <div>
                <div class="aff-title">Corrector & Paráfrasis</div>
                <div class="aff-desc">Reescribe oraciones, elimina plagio y mejora la fluidez gramatical.</div>
            </div>
            <a href="{URL_AFILIADO_PARAPHRASE}" target="_blank" class="aff-btn aff-btn-2">Reescribir Texto →</a>
        </div>
        <div class="aff-card aff-card-3">
            <div>
                <div class="aff-title">Auditoría SEO Avanzada</div>
                <div class="aff-desc">Analiza tu escrito frente al top 10 de Google para asegurar el primer puesto.</div>
            </div>
            <a href="{URL_AFILIADO_SEO_TOOL}" target="_blank" class="aff-btn aff-btn-3">Auditar para Google →</a>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# Botón centrado
col_b1, col_b2, col_b3 = st.columns([1, 1, 1])
with col_b2:
    if st.button("Revisar Texto", type="primary", use_container_width=True):
        if not text_input.strip():
            st.warning("Por favor, introduce un texto antes de pulsar 'Revisar'.")
            st.session_state.reviewed = False
        else:
            st.session_state.reviewed = True
            st.session_state.scroll_target = "resultados-anchor"

STOP_WORDS_ES = set([
    "de", "la", "que", "el", "en", "y", "a", "los", "del", "se", "las", "por", "un", "para", "con", "no", "una",
    "su", "al", "lo", "como", "más", "pero", "sus", "le", "ya", "o", "este", "sí", "porque", "esta", "son",
    "entre", "está", "cuando", "muy", "sin", "sobre", "también", "me", "hasta", "hay", "donde", "quien",
    "desde", "todo", "nos", "durante", "todos", "uno", "les", "ni", "contra", "otros", "ese", "eso", "ante",
    "ellos", "e", "esto", "mí", "antes", "algunos", "qué", "unos", "yo", "otro", "otras", "otra", "él", "tanto",
    "esa", "estos", "mucho", "quienes", "nada", "muchos", "cual", "poco", "ella", "estar", "estas", "algunas",
    "algo", "nosotros"
])

# Renderizado de resultados
if st.session_state.reviewed and text_input.strip():
    words = re.findall(r"\b\w+\b", text_input.lower())
    total_words = len(words)
    total_chars = len(text_input)
    total_chars_no_spaces = len(text_input.replace(" ", ""))
    sentences = len(re.split(r"[.!?]+", text_input)) - 1
    sentences = max(1, sentences) if total_words > 0 else 0
    reading_time = round(total_words / 200, 1)

    st.markdown('<div id="resultados-anchor"></div>', unsafe_allow_html=True)
    st.divider()

    # SECCIÓN 1: MÉTRICAS BÁSICAS
    st.subheader("1. Conteo de Extensión y Lectura")
    st.markdown(
        '<div class="section-explanation">Métricas esenciales para evaluar la longitud del texto frente a los requisitos de tu blog, universidad o red social.</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.markdown(
        f'<div class="metric-card"><div class="metric-value">{total_words}</div><div class="metric-label">Palabras</div></div>',
        unsafe_allow_html=True,
    )
    col2.markdown(
        f'<div class="metric-card"><div class="metric-value">{total_chars}</div><div class="metric-label">Caracteres</div></div>',
        unsafe_allow_html=True,
    )
    col3.markdown(
        f'<div class="metric-card"><div class="metric-value">{total_chars_no_spaces}</div><div class="metric-label">Sin Espacios</div></div>',
        unsafe_allow_html=True,
    )
    col4.markdown(
        f'<div class="metric-card"><div class="metric-value">{sentences}</div><div class="metric-label">Oraciones</div></div>',
        unsafe_allow_html=True,
    )
    col5.markdown(
        f'<div class="metric-card"><div class="metric-value">~{reading_time} min</div><div class="metric-label">Tiempo Lectura</div></div>',
        unsafe_allow_html=True,
    )

    st.divider()

    # SECCIÓN 2: DENSIDAD SEO
    st.subheader("2. Palabras Clave y Densidad SEO")
    st.markdown(
        '<div class="section-explanation">Muestra las palabras más repetidas excluyendo conectores. Para un buen SEO, la palabra clave principal debe rondar entre el 1% y el 3% de densidad.</div>',
        unsafe_allow_html=True,
    )

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
        st.info("Introduce un texto más extenso para analizar la densidad.")

    st.divider()

    # SECCIÓN 3: LEGIBILIDAD Y ESTILO
    st.subheader("3. Análisis de Legibilidad y Estilo")
    st.markdown(
        '<div class="section-explanation">Evalúa la fluidez de lectura. Las oraciones cortas (menos de 20 palabras) mejoran la retención del usuario y favorecen el posicionamiento móvil.</div>',
        unsafe_allow_html=True,
    )

    avg_words_per_sentence = (
        round(total_words / sentences, 1) if sentences > 0 else 0
    )
    col_l1, col_l2 = st.columns(2)
    with col_l1:
        st.markdown(
            f'<div class="metric-card"><div class="metric-value">{avg_words_per_sentence}</div><div class="metric-label">Palabras por Oración (Promedio)</div></div>',
            unsafe_allow_html=True,
        )
    with col_l2:
        if avg_words_per_sentence <= 15:
            st.success(
                "Lectura Fluida: Frases breves y fáciles de digerir. Excelente para lectura en smartphones."
            )
        elif avg_words_per_sentence <= 24:
            st.warning(
                "Dificultad Media: Estructura aceptable, aunque se recomienda acortar los párrafos más densos."
            )
        else:
            st.error(
                "Complejo: Oraciones demasiado largas. Divídelas con puntos seguidos para evitar rebote de usuarios."
            )

    st.divider()

    # SECCIÓN 4: META DESCRIPCIÓN
    st.subheader("4. Generador de Meta Descripción")
    st.markdown(
        '<div class="section-explanation">Extracto sugerido para la etiqueta meta en Google. Estructura oraciones completas de hasta 160 caracteres sin cortar palabras.</div>',
        unsafe_allow_html=True,
    )

    raw_snippet = text_input.replace("\n", " ").strip()
    sentences_list = re.split(r"(?<=[.!?]) +", raw_snippet)
    meta_desc = ""

    for s in sentences_list:
        if len(meta_desc) + len(s) + (1 if meta_desc else 0) <= 160:
            meta_desc = (meta_desc + " " + s).strip()
        else:
            break

    if not meta_desc:
        meta_desc = (
            raw_snippet[:155].rsplit(" ", 1)[0] + "..."
            if len(raw_snippet) > 155
            else raw_snippet
        )

    st.text_area("Snippet listo para copiar:", meta_desc, height=75)
    length_meta = len(meta_desc)
    if 130 <= length_meta <= 160:
        st.caption(
            f"Longitud ideal: **{length_meta} caracteres** (Encaja perfectamente en Google)."
        )
    else:
        st.caption(
            f"Longitud actual: **{length_meta} caracteres** (Recomendado entre 130 y 160)."
        )

    st.divider()

    # SECCIÓN 5: FORMATEADOR RÁPIDO
    st.subheader("5. Formateador de Texto")
    st.markdown(
        '<div class="section-explanation">Herramienta rápida para corregir mayúsculas, minúsculas o espacios dobles.</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div id="formatter-anchor"></div>', unsafe_allow_html=True)

    col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)

    if col_btn1.button("MAYÚSCULAS", use_container_width=True):
        st.session_state.formatted_output = text_input.upper()
        st.session_state.scroll_target = "formatter-anchor"
    if col_btn2.button("minúsculas", use_container_width=True):
        st.session_state.formatted_output = text_input.lower()
        st.session_state.scroll_target = "formatter-anchor"
    if col_btn3.button("Modo Título", use_container_width=True):
        st.session_state.formatted_output = text_input.title()
        st.session_state.scroll_target = "formatter-anchor"
    if col_btn4.button("Limpiar Espacios", use_container_width=True):
        st.session_state.formatted_output = " ".join(text_input.split())
        st.session_state.scroll_target = "formatter-anchor"

    # Cuadro único formateado
    if st.session_state.formatted_output:
        st.markdown("<br>", unsafe_allow_html=True)
        st.text_area(
            "Resultado formateado:",
            st.session_state.formatted_output,
            height=130,
        )

    st.divider()

    # SECCIÓN 6: SLUG URL
    st.subheader("6. Generador de Slug para URL")
    st.markdown(
        '<div class="section-explanation">Transforma el título de tu artículo en una dirección web limpia sin caracteres especiales ni tildes.</div>',
        unsafe_allow_html=True,
    )

    raw_slug = text_input.split("\n")[0]
    slug = re.sub(r"[^\w\s-]", "", raw_slug.lower())
    slug = re.sub(r"[-\s]+", "-", slug).strip("-")
    st.code(
        slug if slug else "escribe-un-titulo-para-generar-el-slug",
        language="text",
    )

    # Autodesplazamiento
    if st.session_state.scroll_target:
        target_id = st.session_state.scroll_target
        st.session_state.scroll_target = None
        components.html(
            f"""
            <script>
                var element = window.parent.document.getElementById('{target_id}');
                if (element) {{
                    element.scrollIntoView({{behavior: 'smooth'}});
                }}
            </script>
        """,
            height=0,
        )

st.markdown(
    """
    <div class="footer-legal">
        TextSEO © 2026 — Herramienta gratuita de análisis de texto.
    </div>
""",
    unsafe_allow_html=True,
)
