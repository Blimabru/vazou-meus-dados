"""Tradução de textos públicos retornados pelos serviços de consulta."""

import html
import logging
from threading import Lock

import requests
import streamlit as st

LOGGER = logging.getLogger(__name__)
TRANSLATION_URL = "https://api.mymemory.translated.net/get"
_TRANSLATION_STATE_LOCK = Lock()
_TRANSLATION_RATE_LIMIT_LOGGED = False


def iniciar_busca_traducao():
    """Reinicia o controle de avisos da API para uma nova busca."""
    global _TRANSLATION_RATE_LIMIT_LOGGED
    with _TRANSLATION_STATE_LOCK:
        _TRANSLATION_RATE_LIMIT_LOGGED = False

FALLBACK_TRANSLATIONS = {
    "email addresses": "Endereços de e-mail",
    "names": "Nomes",
    "phone numbers": "Números de telefone",
    "dates of birth": "Datas de nascimento",
    "passwords": "Senhas",
    "physical addresses": "Endereços físicos",
    "ip addresses": "Endereços IP",
    "usernames": "Nomes de usuário",
    "genders": "Gêneros",
    "social media profiles": "Perfis de redes sociais",
    "geographic locations": "Localizações geográficas",
    "language": "Idioma",
    "join date": "Data de cadastro",
    "session ip addresses": "Endereços IP de sessão",
}


@st.cache_data(ttl=86400, show_spinner=False)
def traduzir_texto(texto, idioma_origem="en", idioma_destino="pt-BR"):
    """Traduz um texto público e retorna o original quando a API falhar."""
    texto_original = str(texto)
    texto = texto_original.strip()
    if not texto:
        return texto_original

    fallback = FALLBACK_TRANSLATIONS.get(texto.lower(), texto_original)
    try:
        response = requests.get(
            TRANSLATION_URL,
            params={
                "q": texto,
                "langpair": f"{idioma_origem}|{idioma_destino}",
            },
            timeout=10,
        )
        if response.status_code == 429:
            global _TRANSLATION_RATE_LIMIT_LOGGED
            with _TRANSLATION_STATE_LOCK:
                deve_registrar = not _TRANSLATION_RATE_LIMIT_LOGGED
                _TRANSLATION_RATE_LIMIT_LOGGED = True
            if deve_registrar:
                LOGGER.error(
                    "API de tradução indisponível nesta busca: "
                    "limite de requisições atingido (HTTP 429)"
                )
            return fallback
        response.raise_for_status()
        translated = response.json().get("responseData", {}).get("translatedText")
        return html.unescape(translated).strip() if translated else fallback
    except (requests.RequestException, ValueError, AttributeError) as error:
        LOGGER.warning("Não foi possível traduzir o texto retornado pela API: %s", error)
        return fallback
