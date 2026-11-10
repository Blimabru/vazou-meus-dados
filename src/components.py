"""Componentes de interface e apresentação dos resultados."""

import re
import base64
from html import escape
from pathlib import Path
from urllib.parse import urlparse

import streamlit as st

from src.config import LOGO_PATH
from src.translator import traduzir_texto


def render_header():
    with st.container(border=True):
        brand, nav = st.columns([2.2, 3.8], vertical_alignment="center")
        with brand:
            logo, text = st.columns([.65, 2.6], gap=None, vertical_alignment="center")
            with logo:
                st.image(LOGO_PATH, width=54)
            with text:
                st.markdown("**Vazou Meus Dados**")
                st.caption("Proteja sua privacidade")
        with nav:
            nav1, nav2, nav3 = st.columns(3)
            with nav1:
                como_funciona = st.button("Como funciona", use_container_width=True)
            with nav2:
                privacidade = st.button("Privacidade", use_container_width=True)
            with nav3:
                dicas = st.button("Dicas de segurança", use_container_width=True)
    if como_funciona:
        st.info("Digite um e-mail e clique em “Verificar risco”. Consultamos a base pública do XposedOrNot e exibimos os incidentes encontrados.")
    if privacidade:
        st.info("O e-mail é usado somente durante a consulta. Esta aplicação não salva, rastreia ou armazena as pesquisas.")
    if dicas:
        st.info("Troque senhas expostas, não reutilize credenciais e ative a autenticação em duas etapas.")


def render_loading():
    """Exibe o indicador central durante a consulta à API."""
    return st.empty()


def preencher_loading(container):
    container.markdown(
        """
        <div class="loading-screen">
            <div class="loading-spinner"></div>
            <div class="loading-title">Analisando seus dados</div>
            <div class="loading-copy">Consultando vazamentos e preparando o relatório...</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer():
    logo_path = Path(LOGO_PATH)
    logo_data = base64.b64encode(logo_path.read_bytes()).decode("ascii")
    st.markdown(
        f"""
        <footer class="app-footer-fixed">
            <div class="footer-fixed-content">
                <div class="footer-fixed-brand">
                    <img class="footer-fixed-logo" src="data:image/png;base64,{logo_data}" alt="Vazou Meus Dados">
                    <span>Vazou Meus Dados <span class="footer-fixed-copy">· Consulta privada e anônima</span></span>
                </div>
                <nav class="footer-fixed-links" aria-label="Links do rodapé">
                    <a href="https://xposedornot.com/api_doc.html" target="_blank">API pública</a>
                    <a href="https://github.com/Blimabru/vazou-meus-dados" target="_blank">GitHub</a>
                </nav>
            </div>
        </footer>
        """,
        unsafe_allow_html=True,
    )


def formatar_dados_vazados(dados):
    if not dados:
        return []
    itens = dados if isinstance(dados, list) else re.split(r"[,;|]", str(dados))
    return [str(item).strip() for item in itens if str(item).strip()]


def render_breach_card(detalhe):
    nome = detalhe.get("breach", "Site desconhecido")
    descricao = traduzir_texto(str(detalhe.get("details", "Sem detalhes adicionais.")))
    dados = formatar_dados_vazados(detalhe.get("xposed_data", ""))
    risco = str(detalhe.get("password_risk", "")).lower()
    setor = detalhe.get("industry", "Não informado")
    dominio = detalhe.get("domain", "")
    ano = detalhe.get("xposed_date", "Não informado")
    registros = detalhe.get("xposed_records", "Não informado")
    referencia = detalhe.get("references", "")
    verificado = detalhe.get("verified", "Não informado")
    senha_exposta = any(
        "password" in item.lower() or "senha" in item.lower() for item in dados
    )

    senha_em_texto_puro = "plain" in risco

    chips = "".join(
        f"<span class='chip'>{traduzir_texto(item)}</span>" for item in dados[:8]
    )
    if senha_exposta and senha_em_texto_puro:
        chips = "<span class='chip chip-danger'>Senha em texto puro</span>" + chips
    logo = detalhe.get("logo", "")
    card_key = f"breach-card-{re.sub(r'[^a-z0-9]+', '-', str(nome).lower()).strip('-')}"
    with st.container(key=card_key, border=True):
        logo_col, content_col = st.columns([1.45, 5.55], gap="small", vertical_alignment="center")
        with logo_col:
            if logo:
                st.markdown(
                    f"""
                    <div class="breach-logo-wrap">
                        <img class="breach-logo-large" src="{escape(str(logo), quote=True)}" alt="Logo de {escape(str(nome), quote=True)}">
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        with content_col:
            st.markdown(f"### {nome}")
            st.caption(f"{setor} · {dominio or 'Domínio não informado'}")
            st.write(descricao)
            metricas = st.columns(3)
            metricas[0].metric("Ano do incidente", ano)
            metricas[1].metric("Registros afetados", f"{registros:,}".replace(",", ".") if isinstance(registros, int) else registros)
            confirmado = str(verificado).lower() == "yes"
            icone_confirmacao = (
                '<svg class="confirmation-icon confirmation-icon-ok" viewBox="0 0 24 24" '
                'aria-label="Confirmado" role="img"><path d="M5 12.5 9.5 17 19 7.5"/></svg>'
                if confirmado
                else
                '<svg class="confirmation-icon confirmation-icon-no" viewBox="0 0 24 24" '
                'aria-label="Não confirmado" role="img"><path d="m7 7 10 10M17 7 7 17"/></svg>'
            )
            metricas[2].markdown(
                f"""
                <div class="confirmation-metric" title="Indica se o XposedOrNot classificou este vazamento como confirmado em sua base.">
                    <div class="confirmation-label">Confirmação do incidente</div>
                    <div class="confirmation-value">{icone_confirmacao}<span>{"" if confirmado else ""}</span></div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<span class='exposed-data-label'>Dados expostos:</span> {chips or 'Não especificado'}",
                unsafe_allow_html=True,
            )
            if dominio:
                site_url = dominio if dominio.startswith(("http://", "https://")) else f"https://{dominio}"
                if urlparse(site_url).netloc:
                    st.link_button("Visitar site afetado", site_url)
            if referencia:
                st.link_button("Ver referência do incidente", referencia)


def mostrar_resumo(analytics, total):
    if not analytics:
        return
    detalhes = analytics.get("ExposedBreaches", {}).get("breaches_details", [])
    senhas = sum("password" in str(item.get("xposed_data", "")).lower() for item in detalhes)
    dados = {item for detalhe in detalhes for item in formatar_dados_vazados(detalhe.get("xposed_data", ""))}
    metricas = analytics.get("BreachMetrics", {})
    risco = metricas.get("risk", [{}])
    risco = risco[0] if isinstance(risco, list) and risco else risco
    score = risco.get("risk_score", "—") if isinstance(risco, dict) else "—"
    nivel_original = risco.get("risk_label", "Não informado") if isinstance(risco, dict) else "Não informado"
    nivel = {
        "low": "Baixo",
        "baixo": "Baixo",
        "medium": "Médio",
        "moderate": "Moderado",
        "médio": "Médio",
        "moderado": "Moderado",
        "high": "Alto",
        "alto": "Alto",
        "critical": "Crítico",
        "crítico": "Crítico",
    }.get(str(nivel_original).strip().lower(), str(nivel_original))
    score_num = int(score) if str(score).isdigit() else 0
    score_num = max(0, min(score_num, 100))
    gauge, metricas_coluna = st.columns([1, 3])
    with gauge:
        st.markdown(
            f"""
            <div class="risk-score-card">
                <div class="risk-score-heading"><span>Pontuação de risco</span><strong>{score_num}/100</strong></div>
                <div class="risk-track"><div class="risk-fill" style="width: {score_num}%"></div></div>
                <div class="risk-scale"><span>Baixo</span><span>Moderado</span><span>Alto</span><span>Crítico</span></div>
                <div class="risk-level">Risco {nivel}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    colunas = metricas_coluna.columns(3)
    for coluna, valor, legenda in zip(
        colunas,
        (total, senhas, len(dados)),
        ("Vazamentos encontrados", "Senhas expostas", "Tipos de dados"),
    ):
        coluna.markdown(f"<div class='metric-box'><div class='value'>{valor}</div><div class='label'>{legenda}</div></div>", unsafe_allow_html=True)
