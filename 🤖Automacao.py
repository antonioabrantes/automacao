# https://share.streamlit.io/
# https://faleconosco.streamlit.app/
# https://github.com/antonioabrantes/automacao

import streamlit as st
import PyPDF2

def extrair_argumentacao_ipas(texto: str) -> str:
    """
    Extrai apenas a argumentação do requerente em petições do INPI,
    removendo dados pessoais e partes administrativas iniciais.
    """

    if not texto or not texto.strip():
        return ""

    # Normaliza espaços
    texto = re.sub(r'\n{2,}', '\n\n', texto)

    # Padrões que indicam início da argumentação
    padrao_inicio = re.compile(
        r"(ILMO\s+SENHOR\s+PRESIDENTE\s+DO\s+INPI|"
        r"DOS\s+FATOS|"
        r"DO\s+DIREITO|"
        r"DAS\s+RAZÕES)",
        re.IGNORECASE
    )

    match = padrao_inicio.search(texto)

    if match:
        texto_filtrado = texto[match.start():]
        return texto_filtrado.strip()

    # Se nenhum marcador for encontrado, retorna texto inteiro (fallback)
    return texto.strip()

def ler_pdf_pypdf2(pdf_bytes):
    """
    Lê PDF textual usando PyPDF2 e retorna o texto completo
    """
    leitor = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
    texto = ""

    for i, pagina in enumerate(leitor.pages):
        texto_pagina = pagina.extract_text()
        if texto_pagina:
            texto += f"\n\n--- Página {i+1} ---\n{texto_pagina}"

    return texto
    


uploaded_file = st.file_uploader("Faça upload do PDF da petição", type=["pdf"])

if uploaded_file:
    st.info("🔍 Processando OCR do PDF, aguarde...")

    pdf_bytes = uploaded_file.read()
    
    #texto_ocr = ocr_pdf(pdf_bytes)
    #argumentacao = extrair_argumentacao(texto_ocr)

    texto_pdf = ler_pdf_pypdf2(pdf_bytes)
    argumentacao = extrair_argumentacao(texto_pdf)

    st.subheader("🧠 Argumentação do Requerente (extraída automaticamente)")
    st.text_area(
        label="Conteúdo filtrado",
        value=argumentacao,
        height=500
    )

    with st.expander("📜 Ver texto completo do OCR"):
        st.text_area(
            label="Texto integral",
            value=texto_pdf,
            height=400
        )