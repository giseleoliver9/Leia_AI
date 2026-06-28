# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from openai import OpenAI
import os
import json
import time
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Base64 image helper for inline logo rendering
import base64
def obter_base64_imagem(caminho):
    try:
        with open(caminho, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception:
        return ""

logo_base64 = obter_base64_imagem("logo.jpg")
logo_html_src = f"data:image/jpeg;base64,{logo_base64}" if logo_base64 else ""

# Initialize session state for query input
if "query_val" not in st.session_state:
    st.session_state.query_val = ""

st.set_page_config(
    page_title="Leia.ai",
    page_icon="📚",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif;
    overflow-x: hidden !important;
}

.stApp {
    background:
        radial-gradient(circle at 20% 10%, rgba(124,58,237,.28), transparent 30%),
        radial-gradient(circle at 80% 20%, rgba(236,72,153,.16), transparent 28%),
        linear-gradient(135deg, #05020d 0%, #10051f 55%, #030108 100%);
    color: white;
}

.block-container {
    max-width: 1120px;
    padding-top: 2.4rem;
    overflow-x: hidden !important;
}

div[data-testid="stSidebar"], [data-testid="stSidebarUserContent"] {
    background: #11121a;
    border-right: 1px solid rgba(255,255,255,.08);
    overflow-x: hidden !important;
}

.hero {
    padding: 44px;
    border-radius: 32px;
    background:
        linear-gradient(135deg, rgba(124,58,237,.32), rgba(236,72,153,.12)),
        rgba(255,255,255,.04);
    border: 1px solid rgba(255,255,255,.14);
    box-shadow: 0 24px 80px rgba(0,0,0,.45);
    position: relative;
    overflow: hidden;
}


.hero h1 {
    font-size: 4rem;
    font-weight: 900;
    margin-bottom: 12px;
    letter-spacing: -2px;
}

.eyebrow {
    font-size: 0.85rem;
    font-weight: 800;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #a78bfa;
    margin-bottom: 8px;
}

.hero p {
    font-size: 1.15rem;
    color: #e9ddff;
    max-width: 760px;
    line-height: 1.7;
}

.badge {
    display: inline-block;
    padding: 9px 15px;
    margin: 16px 8px 0 0;
    border-radius: 999px;
    background: rgba(255,255,255,.06);
    border: 1px solid rgba(255,255,255,.12);
    color: #e7ddff;
    font-size: .88rem;
    font-weight: 700;
}

.metric-card, .prompt-card, .book-card, .empty-card {
    background: rgba(255,255,255,.065);
    border: 1px solid rgba(255,255,255,.12);
    border-radius: 24px;
    box-shadow: 0 18px 50px rgba(0,0,0,.28);
}

.metric-card {
    padding: 24px;
    min-height: 130px;
}

.metric-card h3 {
    font-size: 2rem;
    font-weight: 900;
    margin-bottom: 8px;
    color: #ffffff !important;
}

.metric-card p {
    color: #cfc7e8;
    margin: 0;
}

.prompt-card {
    margin-top: 28px;
    padding: 30px;
}

.prompt-title {
    font-size: 1.5rem;
    font-weight: 900;
    margin-bottom: 6px;
}

.prompt-subtitle {
    color: #bfb7d8;
    margin-bottom: 18px;
}

.ai-chip {
    display: inline-block;
    padding: 7px 12px;
    margin: 6px 6px 0 0;
    border-radius: 12px;
    background: rgba(124,58,237,.18);
    border: 1px solid rgba(167,139,250,.24);
    color: #ddd6fe;
    font-size: .82rem;
    font-weight: 700;
}

.stButton button {
    height: 3.35rem;
    border-radius: 16px;
    font-weight: 900;
    background: linear-gradient(90deg, #7c3aed, #a78bfa);
    border: 0;
    box-shadow: 0 12px 32px rgba(124,58,237,.38);
    width: 100%;
    color: white !important;
    transition: all 0.3s ease;
}

.stButton button:hover {
    transform: translateY(-1px);
    box-shadow: 0 14px 40px rgba(124,58,237,.55);
}

.book-card {
    padding: 22px;
    margin-bottom: 18px;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.book-card:hover {
    transform: translateY(-2px);
    border-color: rgba(167, 139, 250, 0.3);
    box-shadow: 0 24px 60px rgba(124, 58, 237, 0.15);
    background: rgba(255, 255, 255, 0.09);
}

.book-grid {
    display: grid;
    grid-template-columns: 92px 1fr;
    gap: 18px;
}

div[data-testid="stSidebar"] img {
    border-radius: 22px;
    box-shadow: 0 8px 32px rgba(124, 58, 237, 0.25);
}

.cover {
    width: 92px;
    height: 138px;
    border-radius: 14px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 12px 30px rgba(0,0,0,.35);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.book-card:hover .cover {
    transform: scale(1.04);
    box-shadow: 0 16px 40px rgba(124, 58, 237, 0.3);
}

.search-link {
    color: #a78bfa !important;
    text-decoration: none;
    font-size: 0.85rem;
    font-weight: 600;
    transition: all 0.2s ease;
    border-bottom: 1px dashed rgba(167, 139, 250, 0.4);
    padding-bottom: 2px;
}

.search-link:hover {
    color: #ddd6fe !important;
    border-bottom-color: #ddd6fe;
    text-shadow: 0 0 8px rgba(167, 139, 250, 0.6);
}

div[data-testid="stSidebar"] button {
    background: transparent !important;
    border: none !important;
    color: #a78bfa !important;
    text-align: left !important;
    padding: 0 !important;
    height: auto !important;
    font-weight: 500 !important;
    box-shadow: none !important;
    transition: all 0.2s ease !important;
    font-size: 0.9rem !important;
    margin-bottom: 8px !important;
    display: block !important;
    width: 100% !important;
}

div[data-testid="stSidebar"] button:hover {
    color: #ddd6fe !important;
    transform: none !important;
    box-shadow: none !important;
    text-shadow: 0 0 6px rgba(167, 139, 250, 0.4);
}

div[data-testid="column"] button {
    height: auto !important;
    padding: 6px 12px !important;
    border-radius: 12px !important;
    background: rgba(124,58,237,.18) !important;
    border: 1px solid rgba(167,139,250,.24) !important;
    color: #ddd6fe !important;
    font-size: .82rem !important;
    font-weight: 700 !important;
    box-shadow: none !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
    text-align: center !important;
}

div[data-testid="column"] button:hover {
    background: rgba(124,58,237,.32) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(124,58,237,0.2) !important;
}

.book-title {
    font-size: 1.35rem;
    font-weight: 900;
}

.book-meta {
    color: #c4b5fd;
    font-weight: 700;
    margin: 5px 0 12px 0;
}

.reason {
    color: #eee7ff;
    line-height: 1.6;
}

.empty-card {
    padding: 32px;
    text-align: center;
    margin-top: 26px;
    color: #d8cfff;
}

.empty-card h3 {
    font-size: 1.6rem;
    font-weight: 900;
    color: #ffffff !important;
}

.sidebar-box {
    padding: 16px;
    border-radius: 18px;
    background: rgba(96,165,250,.16);
    border: 1px solid rgba(147,197,253,.18);
    color: #dbeafe;
    margin-top: 14px;
}

.hero-logo-icon {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    vertical-align: middle;
    margin-right: 16px;
    margin-top: -8px;
    box-shadow: 0 8px 24px rgba(124,58,237,.35);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

@media (max-width: 640px) {
    .hero {
        padding: 24px !important;
        border-radius: 20px !important;
    }
    .hero h1 {
        font-size: 2.2rem !important;
        letter-spacing: -1px !important;
        display: flex;
        align-items: center;
    }
    .hero-logo-icon {
        width: 36px !important;
        height: 36px !important;
        margin-right: 12px !important;
        border-radius: 10px !important;
    }
    .hero p {
        font-size: 1rem !important;
    }
    .badge {
        padding: 6px 12px !important;
        font-size: 0.8rem !important;
        margin: 8px 4px 0 0 !important;
    }
    .metric-card {
        padding: 16px !important;
        min-height: 100px !important;
    }
    .metric-card h3 {
        font-size: 1.6rem !important;
    }
    .prompt-card {
        padding: 20px !important;
    }
    .prompt-title {
        font-size: 1.25rem !important;
    }
    .book-grid {
        grid-template-columns: 80px 1fr !important;
        gap: 12px !important;
    }
    .cover {
        width: 80px !important;
        height: 120px !important;
    }
    div[data-testid="stHorizontalBlock"]:has(button) {
        flex-direction: row !important;
        flex-wrap: wrap !important;
        justify-content: flex-start !important;
        gap: 8px !important;
    }
    div[data-testid="stHorizontalBlock"]:has(button) div[data-testid="column"] {
        flex: 0 1 auto !important;
        width: calc(33.33% - 6px) !important;
        min-width: 80px !important;
    }
}
</style>
""", unsafe_allow_html=True)

# Mock data fallback (Used when books.csv is not present)
MOCK_BOOKS = [
    {"title": "Duna", "authors": "Frank Herbert", "original_publication_year": 1965, "average_rating": 4.5, "language_code": "por"},
    {"title": "Neuromancer", "authors": "William Gibson", "original_publication_year": 1984, "average_rating": 4.3, "language_code": "por"},
    {"title": "Fahrenheit 451", "authors": "Ray Bradbury", "original_publication_year": 1953, "average_rating": 4.1, "language_code": "por"},
    {"title": "Fundação", "authors": "Isaac Asimov", "original_publication_year": 1951, "average_rating": 4.4, "language_code": "por"},
    {"title": "1984", "authors": "George Orwell", "original_publication_year": 1949, "average_rating": 4.6, "language_code": "por"},
    {"title": "O Senhor dos Anéis", "authors": "J.R.R. Tolkien", "original_publication_year": 1954, "average_rating": 4.8, "language_code": "por"},
    {"title": "O Hobbit", "authors": "J.R.R. Tolkien", "original_publication_year": 1937, "average_rating": 4.7, "language_code": "por"},
    {"title": "Harry Potter e a Pedra Filosofal", "authors": "J.K. Rowling", "original_publication_year": 1997, "average_rating": 4.6, "language_code": "por"},
    {"title": "Frankenstein", "authors": "Mary Shelley", "original_publication_year": 1818, "average_rating": 4.1, "language_code": "eng"},
    {"title": "Pride and Prejudice", "authors": "Jane Austen", "original_publication_year": 1813, "average_rating": 4.6, "language_code": "eng"},
    {"title": "The Catcher in the Rye", "authors": "J.D. Salinger", "original_publication_year": 1951, "average_rating": 3.8, "language_code": "eng"},
    {"title": "O Alquimista", "authors": "Paulo Coelho", "original_publication_year": 1988, "average_rating": 3.9, "language_code": "por"},
    {"title": "Cem Anos de Solidão", "authors": "Gabriel García Márquez", "original_publication_year": 1967, "average_rating": 4.4, "language_code": "spa"},
    {"title": "Don Quixote", "authors": "Miguel de Cervantes", "original_publication_year": 1605, "average_rating": 4.3, "language_code": "spa"},
    {"title": "O Pequeno Príncipe", "authors": "Antoine de Saint-Exupéry", "original_publication_year": 1943, "average_rating": 4.3, "language_code": "fre"}
]

@st.cache_data
def carregar_dados():
    try:
        df = pd.read_csv("archive/books.csv")
        df = df[['title', 'authors', 'original_publication_year', 'average_rating', 'language_code', 'image_url', 'isbn', 'isbn13']]
        df = df.dropna(subset=['title', 'authors', 'original_publication_year', 'average_rating'])
        df['original_publication_year'] = df['original_publication_year'].round().astype(int)
        return df, False
    except FileNotFoundError:
        df = pd.DataFrame(MOCK_BOOKS)
        for col in ['image_url', 'isbn', 'isbn13']:
            if col not in df.columns:
                df[col] = None
        return df, True

# Load book catalog
df_books, is_fallback = carregar_dados()

# Load OpenRouter API Key silently from environment variable or Streamlit secrets
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    try:
        if "OPENROUTER_API_KEY" in st.secrets:
            api_key = st.secrets["OPENROUTER_API_KEY"]
    except Exception:
        pass

# Fallback to GROQ_API_KEY if OpenRouter key is not found
if not api_key:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        try:
            if "GROQ_API_KEY" in st.secrets:
                api_key = st.secrets["GROQ_API_KEY"]
        except Exception:
            pass

# Default AI Config (Defaults to Llama 3.3 on OpenRouter, fallback to Groq model if needed)
modelo = "meta-llama/llama-3.3-70b-instruct"
temperatura = 0.7

def gerar_cores_capa(titulo):
    import hashlib
    h = hashlib.md5(titulo.encode('utf-8')).hexdigest()
    # Purple/lilac/pink hues: 240 to 330
    hue1 = 240 + (int(h[0:2], 16) % 90)
    hue2 = 260 + (int(h[2:4], 16) % 70)
    hue3 = 190 + (int(h[4:6], 16) % 70)
    return f"hsl({hue1}, 70%, 55%)", f"hsl({hue2}, 45%, 18%)", f"hsl({hue3}, 60%, 12%)"

def obter_capa_livro(livro_rec, df_books):
    titulo = livro_rec.get("titulo", "")
    autor = livro_rec.get("autor", "")
    isbn_rec = livro_rec.get("isbn")
    
    # 1. Try to find in catalog
    if df_books is not None and not df_books.empty:
        import re
        t_clean = re.sub(r'[^\w\s]', '', titulo.lower()).strip()
        match = df_books[df_books['title'].str.lower().str.contains(t_clean, na=False, regex=False)]
        if not match.empty:
            # Match author if multiple
            if len(match) > 1 and autor:
                a_clean = re.sub(r'[^\w\s]', '', autor.lower()).strip()
                match_author = match[match['authors'].str.lower().str.contains(a_clean, na=False, regex=False)]
                if not match_author.empty:
                    match = match_author
            row = match.iloc[0]
            img = row.get('image_url')
            if img and pd.notna(img) and 'nophoto' not in str(img).lower():
                return str(img).replace("http://", "https://")
            # If it is a nophoto but catalog has isbn, try to use isbn
            isbn = row.get('isbn') or row.get('isbn13')
            if isbn and pd.notna(isbn):
                clean_isbn = str(isbn).split('.')[0].strip()
                if clean_isbn and clean_isbn.lower() != 'nan':
                    return f"https://covers.openlibrary.org/b/isbn/{clean_isbn}-M.jpg"
                    
    # 2. Use ISBN from LLM if available
    if isbn_rec:
        clean_isbn = str(isbn_rec).strip().replace('-', '')
        if clean_isbn.isdigit():
            return f"https://covers.openlibrary.org/b/isbn/{clean_isbn}-M.jpg"
            
    return None

# SIDEBAR
with st.sidebar:
    pad1, col_img, pad2 = st.columns([1, 8, 1])
    with col_img:
        st.image("logo.jpg")

    st.markdown("### Histórico recente")
    if st.button("🌌 Fantasia sombria", key="hist_1"):
        st.session_state.query_val = "Quero livros de fantasia sombria, com atmosfera densa, mistério e magia."
        st.rerun()
    if st.button("🧠 Ficção científica filosófica", key="hist_2"):
        st.session_state.query_val = "Ficção científica filosófica que explore a consciência e inteligência artificial."
        st.rerun()
    if st.button("🏜️ Parecidos com Duna", key="hist_3"):
        st.session_state.query_val = "Livros parecidos com Duna, com política espacial, ecologia e impérios."
        st.rerun()

    st.markdown("""
    <div class="sidebar-box">
        💡 A IA considera gênero, nota, popularidade, idioma e intenção do usuário.
    </div>
    """, unsafe_allow_html=True)


# HERO
logo_src_html = f'<img src="{logo_html_src}" class="hero-logo-icon" />' if logo_html_src else ''
st.markdown(f"""
<div class="hero">
    <p class="eyebrow">RECOMENDAÇÕES LITERÁRIAS COM IA</p>
    <h1>{logo_src_html}Leia.ai</h1>
    <p>Livros que combinam com você, explicados por inteligência artificial.</p>
    <div class="badges">
        <span class="badge">IA literária</span>
        <span class="badge">GoodBooks-10K</span>
        <span class="badge">Recomendações explicadas</span>
        <span class="badge">Busca por intenção</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.write("")

# METRICS
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <h3>{ "15" if is_fallback else "10K+" }</h3>
        <p>Livros analisados no catálogo.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h3>IA</h3>
        <p>Entende preferências em linguagem natural.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <h3>Explicável</h3>
        <p>Cada indicação vem com motivo claro.</p>
    </div>
    """, unsafe_allow_html=True)


st.markdown("""
<div class="prompt-card">
    <div class="prompt-title">Encontre sua próxima leitura</div>
    <div class="prompt-subtitle" style="margin-bottom: 0px;">
        Escreva como se estivesse conversando com a Leia. Selecione um exemplo abaixo se quiser começar rápido:
    </div>
</div>
""", unsafe_allow_html=True)

st.write("")
col_chip1, col_chip2, col_chip3, col_chip4, col_chip5 = st.columns(5)
with col_chip1:
    if st.button("🎭 Drama", key="chip_drama"):
        st.session_state.query_val = "Quero um drama intenso e emocionante com segredos de família."
        st.rerun()
with col_chip2:
    if st.button("🚀 Sci-Fi", key="chip_scifi"):
        st.session_state.query_val = "Ficção científica sobre exploração espacial e inteligência artificial."
        st.rerun()
with col_chip3:
    if st.button("⚔️ Fantasia", key="chip_fantasy"):
        st.session_state.query_val = "Fantasia sombria com sistema de magia complexo e clima misterioso."
        st.rerun()
with col_chip4:
    if st.button("🕵️ Mistério", key="chip_mystery"):
        st.session_state.query_val = "Um romance policial noir com suspense psicológico instigante."
        st.rerun()
with col_chip5:
    if st.button("🧠 Distopia", key="chip_dystopia"):
        st.session_state.query_val = "Uma distopia filosófica clássica que discuta o futuro da humanidade."
        st.rerun()

query = st.text_area(
    "O que você gostaria de ler hoje?",
    value=st.session_state.query_val,
    placeholder="Ex: Quero fantasia medieval sombria com protagonistas fortes e clima misterioso...",
    height=120
)

col1, col2, col3 = st.columns(3)

with col1:
    idioma = st.selectbox(
        "Idioma original",
        ["Todos", "Português", "Inglês", "Espanhol", "Francês"]
    )

with col2:
    nota = st.slider(
        "Nota mínima no Goodreads",
        0.0,
        5.0,
        3.5
    )

with col3:
    quantidade = st.slider(
        "Quantidade de recomendações",
        1,
        10,
        5
    )

buscar = st.button(
    "🔍 Obter recomendação inteligente",
    use_container_width=True
)

# API Query Function (Supports OpenRouter and Groq)
def recomendar_livros_com_ia(api_key, model, prompt_usuario, livros, temp, num_recom):
    is_openrouter = str(api_key).startswith("sk-or-")
    
    # Configure API endpoint and model target based on key type
    base_url = "https://openrouter.ai/api/v1" if is_openrouter else "https://api.groq.com/openai/v1"
    target_model = "meta-llama/llama-3.3-70b-instruct" if (is_openrouter and model == "llama-3.3-70b-versatile") else model
    
    headers = {}
    if is_openrouter:
        headers = {
            "HTTP-Referer": "https://github.com/giseleoliver9/Leia_AI",
            "X-Title": "Leia.ai",
        }
        
    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
        default_headers=headers
    )
    
    livros_simples = [
        {
            "title": l["title"],
            "authors": l["authors"],
            "original_publication_year": int(l["original_publication_year"]),
            "average_rating": float(l["average_rating"]),
            "language": "Inglês" if l["language_code"] == "eng" else "Português" if l["language_code"] == "por" else "Espanhol" if l["language_code"] == "spa" else "Francês" if l["language_code"] == "fre" else l["language_code"]
        }
        for l in livros
    ]
    
    prompt = f"""
Você é o Leia.ai, um recomendador de livros inteligente.
Com base nas preferências do usuário: "{prompt_usuario}"

Selecione exatamente até {num_recom} livros que melhor se adaptem às preferências do usuário.
Dê preferência para os livros que estão no nosso catálogo fornecido abaixo:
{json.dumps(livros_simples, ensure_ascii=False)}

Caso o catálogo não possua livros ideais ou suficientes para satisfazer a busca do usuário, você DEVE usar o seu próprio conhecimento geral sobre toda a literatura mundial para sugerir outros livros reais existentes que combinem perfeitamente com a busca do usuário.

Retorne um objeto JSON contendo:
1. "introducao": Uma breve frase de introdução no seu estilo característico e carismático.
2. "livros": Uma lista de objetos. Cada objeto deve conter:
   - "titulo": O título do livro.
   - "autor": O autor do livro.
   - "nota": A nota média do livro (Goodreads ou nota aproximada se sugerido do seu conhecimento geral).
   - "idioma": O idioma do livro (ex: "Inglês", "Português", "Espanhol", "Francês").
   - "genero": O gênero literário deduzido.
   - "icone": Um único emoji representativo (ex: 🏜️ para deserto, ❄️ para frio, 🚀 para espaço, 🎻 ou ⚔️ para fantasia, 💾 para cyberpunk, 👻 para terror, 🕵️ para mistério).
   - "origem": A palavra "catálogo" se o livro estiver na lista do catálogo acima, ou a expressão "conhecimento geral" se você o sugeriu a partir do seu próprio conhecimento.
   - "motivo": Uma explicação curta e convincente de por que este livro combina com a preferência do usuário.
   - "isbn": O ISBN-13 ou ISBN-10 do livro (apenas números, sem traços), ou null se não souber.
3. "conclusao": Uma frase final curta e inspiradora.

Retorne APENAS o JSON válido. Exemplo:
{{
  "introducao": "frase...",
  "livros": [
    {{"titulo": "nome", "autor": "autor", "nota": 4.5, "idioma": "Inglês", "genero": "genero", "icone": "🚀", "origem": "catálogo", "motivo": "porque...", "isbn": "9780451524935"}}
  ],
  "conclusao": "frase..."
}}
"""

    completion = client.chat.completions.create(
        model=target_model,
        messages=[
            {"role": "system", "content": "Você é a Leia, uma assistente virtual de recomendação literária inteligente, perspicaz e carismática. Você responde estritamente no formato JSON estruturado."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
        temperature=temp,
        max_tokens=1200
    )
    
    return json.loads(completion.choices[0].message.content.strip())


# PROCESSING
if buscar:
    if not query.strip():
        st.warning("Digite o tipo de livro que você procura.")
    else:
        # Filter logic
        idioma_map = {
            "Todos": None,
            "Português": "por",
            "Inglês": "eng",
            "Espanhol": "spa",
            "Francês": "fre"
        }
        
        df_filtered = df_books.copy()
        if idioma != "Todos":
            lang_code = idioma_map.get(idioma)
            if lang_code:
                df_filtered = df_filtered[df_filtered['language_code'] == lang_code]
        
        df_filtered = df_filtered[df_filtered['average_rating'] >= nota]
        
        if df_filtered.empty:
            st.error("Nenhum livro corresponde aos filtros selecionados. Tente diminuir a nota mínima ou alterar o idioma.")
        else:
            # Ranquear os livros por palavras-chave com base na pesquisa
            if query.strip():
                import re
                clean_query = re.sub(r'[^\w\s]', '', query.lower())
                stopwords = {'quero', 'livro', 'livros', 'sobre', 'como', 'para', 'com', 'uma', 'este', 'que', 'dos', 'das', 'uma', 'uns', 'algum', 'alguns'}
                words = [w for w in clean_query.split() if len(w) > 2 and w not in stopwords]
                
                if words:
                    def calc_score(row):
                        score = 0
                        title = str(row.get('title', '')).lower()
                        authors = str(row.get('authors', '')).lower()
                        for w in words:
                            if w in title:
                                score += 3  # Título tem peso maior
                            if w in authors:
                                score += 1
                        return score
                    
                    df_filtered['match_score'] = df_filtered.apply(calc_score, axis=1)
                    df_filtered = df_filtered.sort_values(by=['match_score', 'average_rating'], ascending=[False, False])
                else:
                    df_filtered = df_filtered.sort_values(by='average_rating', ascending=False)
            else:
                df_filtered = df_filtered.sort_values(by='average_rating', ascending=False)
                
            # Pick first 50 rows to fit LLM context window nicely
            livros_selecionados = df_filtered.head(50).to_dict(orient='records')
            
            # If API Key is missing, fall back to showing demo mocked results
            if not api_key:
                st.warning("⚠️ **Chave de API ausente**: Mostrando recomendações de demonstração (mockadas). Configure o arquivo .env com sua chave do OpenRouter ou Groq para usar a IA!")
                
                # Mock result for demo matching the exact structure
                recomendacoes = {
                    "introducao": "Aqui estão algumas ótimas sugestões de demonstração selecionadas do nosso catálogo:",
                    "livros": [
                        {
                            "titulo": "Duna",
                            "autor": "Frank Herbert",
                            "nota": "4.3",
                            "idioma": "Inglês",
                            "genero": "Ficção científica",
                            "icone": "🏜️",
                            "origem": "catálogo",
                            "motivo": "Combina política, ecologia, religião, poder e construção de mundo complexa.",
                            "isbn": "0441172717"
                        },
                        {
                            "titulo": "A Mão Esquerda da Escuridão",
                            "autor": "Ursula K. Le Guin",
                            "nota": "4.1",
                            "idioma": "Inglês",
                            "genero": "Sci-fi filosófico",
                            "icone": "❄️",
                            "origem": "catálogo",
                            "motivo": "Ideal para quem busca reflexão social, cultura alienígena e profundidade temática.",
                            "isbn": "0441478123"
                        },
                        {
                            "titulo": "O Nome do Vento",
                            "autor": "Patrick Rothfuss",
                            "nota": "4.5",
                            "idioma": "Inglês",
                            "genero": "Fantasia",
                            "icone": "🎻",
                            "origem": "catálogo",
                            "motivo": "Indicado para leitores que gostam de fantasia imersiva e protagonista marcante.",
                            "isbn": "0756404746"
                        },
                        {
                            "titulo": "Fundação",
                            "autor": "Isaac Asimov",
                            "nota": "4.2",
                            "idioma": "Inglês",
                            "genero": "Ficção científica",
                            "icone": "🚀",
                            "origem": "catálogo",
                            "motivo": "Boa escolha para fãs de impérios galácticos, estratégia e grandes ideias.",
                            "isbn": "0553293354"
                        },
                        {
                            "titulo": "Neuromancer",
                            "autor": "William Gibson",
                            "nota": "4.0",
                            "idioma": "Inglês",
                            "genero": "Cyberpunk",
                            "icone": "💾",
                            "origem": "catálogo",
                            "motivo": "Recomendado para quem gosta de tecnologia, futuro distópico e atmosfera urbana.",
                            "isbn": "0441569595"
                        }
                    ],
                    "conclusao": "Configure a variável OPENROUTER_API_KEY ou GROQ_API_KEY no seu arquivo .env para obter sugestões reais da IA!"
                }
                
                # Simulate loading time for mock to feel real
                with st.spinner("🧠 Analisando preferências literárias..."):
                    time.sleep(1)
            else:
                with st.spinner("🧠 Analisando preferências literárias..."):
                    try:
                        recomendacoes = recomendar_livros_com_ia(
                            api_key=api_key,
                            model=modelo,
                            prompt_usuario=query,
                            livros=livros_selecionados,
                            temp=temperatura,
                            num_recom=quantidade
                        )
                    except Exception as e:
                        st.error(f"Erro ao consultar a API do Provedor de IA: {str(e)}")
                        recomendacoes = None
            
            if recomendacoes:
                st.success("Recomendações encontradas!")
                st.markdown(f"## ✨ {recomendacoes.get('introducao', 'Recomendações para você')}")
                
                # Render results in book cards
                for livro in recomendacoes.get("livros", [])[:quantidade]:
                    origem = livro.get("origem", "catálogo").lower()
                    if "catálogo" in origem or "catalogo" in origem:
                        chip_origem = '<span class="ai-chip" style="background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.22); color: #a7f3d0;">📁 No catálogo</span>'
                    else:
                        chip_origem = '<span class="ai-chip" style="background: rgba(59, 130, 246, 0.15); border: 1px solid rgba(59, 130, 246, 0.22); color: #bfdbfe;">✨ IA Geral (Groq)</span>'
                        
                    img_url = obter_capa_livro(livro, df_books)
                    c1, c2, c3 = gerar_cores_capa(livro.get("titulo", ""))
                    import urllib.parse
                    titulo_encoded = urllib.parse.quote(f"{livro.get('titulo')} {livro.get('autor')}")
                    
                    if img_url:
                        cover_html = (
                            f'<div class="cover">'
                            f'<img src="{img_url}" onerror="this.style.display=\'none\';" style="width: 100%; height: 100%; object-fit: cover; position: absolute; top: 0; left: 0; z-index: 2;" />'
                            f'<div style="width: 100%; height: 100%; background: linear-gradient(135deg, {c1} 0%, transparent 60%), linear-gradient(145deg, {c2}, {c3}); position: absolute; top: 0; left: 0; z-index: 1;"></div>'
                            f'</div>'
                        )
                    else:
                        cover_html = (
                            f'<div class="cover">'
                            f'<div style="width: 100%; height: 100%; background: linear-gradient(135deg, {c1} 0%, transparent 60%), linear-gradient(145deg, {c2}, {c3}); position: absolute; top: 0; left: 0;"></div>'
                            f'</div>'
                        )
                    
                    st.markdown(f"""<div class="book-card">
<div class="book-grid">
{cover_html}
<div>
<div class="book-title">{livro.get("titulo")}</div>
<div class="book-meta">
{livro.get("autor")} · ⭐ {livro.get("nota")} · {livro.get("idioma", "Idioma Indefinido")} · {livro.get("genero")}
</div>
<div style="margin-bottom: 12px;">
<span class="ai-chip">{livro.get("genero")}</span>
{chip_origem}
</div>
<p class="reason">
<strong>Por que a Leia recomendou:</strong> {livro.get("motivo")}
</p>
<div style="margin-top: 14px; display: flex; gap: 16px;">
<a href="https://www.goodreads.com/search?q={titulo_encoded}" target="_blank" class="search-link">🔍 Buscar no Goodreads</a>
<a href="https://books.google.com/books?q={titulo_encoded}" target="_blank" class="search-link">📖 Google Books</a>
</div>
</div>
</div>
</div>""", unsafe_allow_html=True)
                
                st.info(recomendacoes.get("conclusao", ""))
                
                # Save recommendations to file
                try:
                    with open("historico_recomendacoes.txt", "a", encoding="utf-8") as f:
                        f.write(f"\nUsuário: {query}\nFiltros: Idioma={idioma}, Nota={nota}\nRecomendação:\n{json.dumps(recomendacoes, ensure_ascii=False, indent=2)}\n---\n")
                except Exception:
                    pass
else:
    st.markdown("""
    <div class="empty-card">
        <h3>📖 Pronto para descobrir um novo livro com a Leia?</h3>
        <p>
            Digite uma preferência, gênero, autor ou clima de leitura.
            A Leia transforma seu pedido em recomendações personalizadas.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<br><br>
<center style="color:#9ca3af;">
    Desenvolvido com Python, Streamlit, GoodBooks-10K e IA.
</center>
""", unsafe_allow_html=True)