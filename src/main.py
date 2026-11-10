"""Orquestração da interface Streamlit.

O módulo coordena entrada do usuário, chamadas de serviço, estado da sessão,
renderização do relatório e registro de telemetria operacional.
"""

import time
import logging

import streamlit as st

from src.components import (
    preencher_loading,
    mostrar_resumo,
    render_breach_card,
    render_footer,
    render_header,
    render_loading,
)
from src.config import APP_ICON, APP_TITLE, PUBLIC_URL, SHARE_DESCRIPTION, SHARE_IMAGE_URL
from src.services import (
    buscar_analytics,
    buscar_vazamentos,
    obter_status_api,
    registrar_acesso,
    registrar_busca,
    registrar_renderizacao,
    registrar_telemetria,
)
from src.styles import CSS
from src.translator import iniciar_busca_traducao

LOGGER = logging.getLogger(__name__)


def limpar_busca():
    """Remove o resultado atual e registra a ação sem guardar dados pessoais."""
    registrar_telemetria("searches_cleared")
    st.session_state.email_input = ""
    st.session_state.resultado_vazamentos = None
    st.session_state.resultado_analytics = None
    st.session_state.status_api = None
    st.session_state.consulta_realizada = False


def render_share_metadata():
    """Insere metadados Open Graph e Twitter para compartilhamento da página."""
    st.markdown(
        f"""
        <meta property="og:type" content="website">
        <meta property="og:url" content="{PUBLIC_URL}">
        <meta property="og:title" content="Vazou Meus Dados">
        <meta property="og:description" content="{SHARE_DESCRIPTION}">
        <meta property="og:image" content="{SHARE_IMAGE_URL}">
        <meta name="twitter:card" content="summary">
        <meta name="twitter:title" content="Vazou Meus Dados">
        <meta name="twitter:description" content="{SHARE_DESCRIPTION}">
        <meta name="twitter:image" content="{SHARE_IMAGE_URL}">
        """,
        unsafe_allow_html=True,
    )


def render_print_button():
    """Renderiza botão isolado que solicita impressão da janela principal."""
    markup = """
        <style>
            .report-actions { display: flex; justify-content: flex-end; }
            .print-report-button {
                display: inline-flex; align-items: center; gap: .45rem;
                padding: .55rem .9rem;
                border: 1px solid #0284c7;
                border-color: light-dark(#0284c7, rgba(125, 211, 252, .45));
                border-radius: 999px;
                background: #e0f2fe;
                background: light-dark(#e0f2fe, rgba(14, 116, 144, .25));
                color: #0c4a6e;
                color: light-dark(#0c4a6e, #bae6fd);
                font: 700 13px sans-serif; cursor: pointer;
                transition: background-color .2s ease, border-color .2s ease;
            }
            .print-report-button:hover {
                background: #bae6fd;
                background: light-dark(#bae6fd, rgba(14, 116, 144, .45));
                border-color: #0369a1;
                border-color: light-dark(#0369a1, rgba(125, 211, 252, .8));
                color: #082f49;
                color: light-dark(#082f49, #f0f9ff);
            }
            @media print {
                .report-actions { display: none !important; }
            }
        </style>
        <div class="report-actions">
            <button type="button" class="print-report-button" id="print-report">
                <span aria-hidden="true">⎙</span> Imprimir relatório
            </button>
        </div>
        <script>
            document.getElementById("print-report").addEventListener("click", function () {
                window.parent.print();
            });
        </script>
        """
    st.html(markup, unsafe_allow_javascript=True)


def render_resultado(vazamentos, analytics, status_api=None):
    """Renderiza sucesso, ausência de vazamentos ou falhas classificadas."""
    if vazamentos is None:
        if status_api == "cooldown":
            st.warning(
                "⏳ A API recebeu pesquisas muito próximas e solicitou um cooldown. "
                "Aguarde antes de tentar novamente."
            )
            return
        if status_api == "expired":
            st.error(
                "⚠️ A API de vazamentos informou que a configuração de acesso expirou."
            )
            return
        st.error(
            "⚠️ Não foi possível consultar a API de vazamentos neste momento. "
            "O serviço pode estar temporariamente indisponível ou com a chave expirada."
        )
        with st.expander("Detalhes e próximos passos"):
            st.write(
                "A falha foi registrada no log do servidor. Verifique a resposta da API, "
                "as credenciais/configuração e tente novamente em alguns minutos."
            )
        return

    render_print_button()
    if not vazamentos:
        st.success("### 🟢 Risco baixo: nenhum vazamento foi encontrado.")
        st.info("Continue usando senhas únicas e autenticação em duas etapas.")
        return

    if analytics is None:
        st.warning(
            "⚠️ Os vazamentos foram encontrados, mas o relatório detalhado de risco "
            "não está disponível no momento. Exibindo os dados básicos."
        )

    metricas = analytics.get("BreachMetrics") if isinstance(analytics, dict) else None
    metricas = metricas if isinstance(metricas, dict) else {}
    risco = metricas.get("risk", [{}])
    risco = risco[0] if isinstance(risco, list) and risco else risco
    score = risco.get("risk_score", "—") if isinstance(risco, dict) else "—"
    nivel = str(risco.get("risk_label", "Alto") if isinstance(risco, dict) else "Alto").lower()
    icone = "🟢" if nivel in ("baixo", "low") else "🟡" if nivel in ("médio", "moderate", "medium") else "🔴" if nivel in ("crítico", "critical") else "🟠"
    nivel_pt = {"low": "Baixo", "medium": "Médio", "moderate": "Médio", "high": "Alto", "critical": "Crítico"}.get(nivel, risco.get("risk_label", "Alto") if isinstance(risco, dict) else "Alto")

    mostrar_resumo(analytics, len(vazamentos))
    exposed = analytics.get("ExposedBreaches") if isinstance(analytics, dict) else None
    detalhes = exposed.get("breaches_details", []) if isinstance(exposed, dict) else []
    st.markdown("<div class='section-title'><h3>🔎 Vazamentos identificados</h3></div>", unsafe_allow_html=True)
    if detalhes:
        for detalhe in detalhes:
            render_breach_card(detalhe)
    else:
        st.warning(f"Fontes encontradas: {', '.join(vazamentos)}")

    st.markdown("### 📋 Próximos passos")
    recomendacoes = (
        ("🔑", "Troque as senhas afetadas."),
        ("♻️", "Não reutilize credenciais."),
        ("🛡️", "Ative o 2FA no seu e-mail, banco e redes sociais."),
        ("🔐", "Use um gerenciador para criar senhas únicas e fortes."),
        ("🚪", "Encerre sessões abertas e remova dispositivos desconhecidos."),
        ("👀", "Monitore suas contas e fique atento a tentativas de phishing."),
    )
    for inicio in range(0, len(recomendacoes), 3):
        recomendacao_colunas = st.columns(3)
        for coluna, (icone_recomendacao, texto) in zip(
            recomendacao_colunas, recomendacoes[inicio:inicio + 3]
        ):
            coluna.markdown(
                f"""
                <div class="recommendation-card">
                    <div class="recommendation-icon">{icone_recomendacao}</div>
                    <div class="recommendation-text">{texto}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        if inicio + 3 < len(recomendacoes):
            st.markdown("<div class='recommendation-row-gap'></div>", unsafe_allow_html=True)


def main():
    """Inicializa o Streamlit e executa o ciclo principal da aplicação."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout="wide")
    render_share_metadata()
    st.markdown(CSS, unsafe_allow_html=True)
    # A sessão preserva o relatório entre reruns provocados por widgets.
    if "resultado_vazamentos" not in st.session_state:
        st.session_state.resultado_vazamentos = None
        st.session_state.resultado_analytics = None
        st.session_state.status_api = None
        st.session_state.consulta_realizada = False
        registrar_acesso()

    render_header()
    st.markdown("<div class='app-subtitle'>Verifique se o seu e-mail apareceu em vazamentos públicos e entenda quais dados foram expostos.</div>", unsafe_allow_html=True)
    st.info("🔒 **A sua pesquisa é privada.** Não armazenamos os dados consultados.")

    email = st.text_input(
        "Digite o seu e-mail para consulta:",
        placeholder="usuario@email.com",
        key="email_input",
    ).strip()
    verificar_coluna, limpar_coluna, _ = st.columns([0.7, 0.9, 8.4], gap="small")
    with verificar_coluna:
        verificar = st.button("Verificar risco", type="primary")
    with limpar_coluna:
        limpar = st.button(
            "Limpar Busca",
            key="clear-search",
            on_click=limpar_busca,
        )
    # A consulta só começa após validação superficial; a API continua sendo a
    # autoridade para determinar se o endereço existe em sua base.
    if verificar:
        if not email or "@" not in email:
            st.warning("Informe um endereço de e-mail válido.")
        else:
            LOGGER.info("Acesso à busca solicitado")
            loading = render_loading()
            preencher_loading(loading)
            time.sleep(1)
            # As consultas são separadas para distinguir falha básica de falha
            # parcial no relatório detalhado.
            vazamentos = buscar_vazamentos(email)
            status_api = obter_status_api()
            analytics = buscar_analytics(email) if vazamentos else None
            exposed = analytics.get("ExposedBreaches") if isinstance(analytics, dict) else None
            detalhes = exposed.get("breaches_details", []) if isinstance(exposed, dict) else []
            registrar_busca(vazamentos, detalhes, analytics)
            st.session_state.resultado_vazamentos = vazamentos
            st.session_state.resultado_analytics = analytics
            st.session_state.status_api = status_api
            st.session_state.consulta_realizada = True
            iniciar_busca_traducao()
            inicio_render = time.monotonic()
            render_resultado(vazamentos, analytics, status_api)
            registrar_renderizacao(round((time.monotonic() - inicio_render) * 1000))
            loading.empty()
    elif st.session_state.consulta_realizada:
        inicio_render = time.monotonic()
        render_resultado(
            st.session_state.resultado_vazamentos,
            st.session_state.resultado_analytics,
            st.session_state.status_api,
        )
        registrar_renderizacao(round((time.monotonic() - inicio_render) * 1000))
    render_footer()
