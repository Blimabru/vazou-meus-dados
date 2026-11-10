"""Integrações externas da aplicação."""

import logging
from threading import Lock
import time

import requests
from urllib.parse import quote

from src.config import API_BASE_URL

LOGGER = logging.getLogger(__name__)
_STATS_LOCK = Lock()
_STATS = {
    "accesses": 0,
    "searches": 0,
    "positive_searches": 0,
    "negative_searches": 0,
    "failed_searches": 0,
}


def registrar_acesso():
    """Registra um acesso à aplicação e exibe o contador no terminal."""
    with _STATS_LOCK:
        _STATS["accesses"] += 1
        accesses = _STATS["accesses"]
    LOGGER.info(
        "\n%s\n📊 ACESSO À APLICAÇÃO\n   Total de acessos: %s\n%s",
        "-" * 56,
        accesses,
        "-" * 56,
    )


def registrar_busca(resultado):
    """Atualiza as métricas de busca sem registrar dados pessoais."""
    with _STATS_LOCK:
        _STATS["searches"] += 1
        if resultado is None:
            _STATS["failed_searches"] += 1
        elif resultado:
            _STATS["positive_searches"] += 1
        else:
            _STATS["negative_searches"] += 1
        metricas = _STATS.copy()
    LOGGER.info(
        "\n%s\n🔎 RESUMO DAS BUSCAS\n   Acessos: %s\n   Buscas totais: %s\n   ✅ Positivas: %s\n   ⚪ Negativas: %s\n   ❌ Falhas: %s\n%s",
        "-" * 56,
        metricas["accesses"],
        metricas["searches"],
        metricas["positive_searches"],
        metricas["negative_searches"],
        metricas["failed_searches"],
        "-" * 56,
    )


def buscar_vazamentos(email):
    """Consulta os vazamentos associados ao e-mail."""
    inicio = time.monotonic()
    LOGGER.info("Consulta de vazamentos iniciada")
    try:
        response = requests.get(
            f"{API_BASE_URL}/v1/check-email/{quote(email)}",
            timeout=20,
        )
        if response.status_code != 200:
            LOGGER.error(
                "Consulta de vazamentos falhou: status HTTP %s (%.2fs)",
                response.status_code,
                time.monotonic() - inicio,
            )
            return None

        breaches = response.json().get("breaches", [[]])
        resultado = breaches[0] if isinstance(breaches, list) and breaches else breaches
        LOGGER.info(
            "Consulta de vazamentos concluída: %s encontrado(s) (%.2fs)",
            len(resultado) if isinstance(resultado, list) else 0,
            time.monotonic() - inicio,
        )
        return resultado
    except (requests.exceptions.RequestException, ValueError, TypeError) as error:
        LOGGER.error(
            "Erro na consulta de vazamentos (%.2fs): %s",
            time.monotonic() - inicio,
            type(error).__name__,
        )
        return None


def buscar_analytics(email):
    """Consulta o relatório detalhado de risco do e-mail."""
    inicio = time.monotonic()
    LOGGER.info("Consulta de analytics iniciada")
    try:
        response = requests.get(
            f"{API_BASE_URL}/v1/breach-analytics?email={quote(email)}",
            timeout=20,
        )
        if response.status_code != 200:
            LOGGER.error(
                "Consulta de analytics falhou: status HTTP %s (%.2fs)",
                response.status_code,
                time.monotonic() - inicio,
            )
            return None
        resultado = response.json()
        LOGGER.info("Consulta de analytics concluída (%.2fs)", time.monotonic() - inicio)
        return resultado
    except (requests.exceptions.RequestException, ValueError, TypeError) as error:
        LOGGER.error(
            "Erro na consulta de analytics (%.2fs): %s",
            time.monotonic() - inicio,
            type(error).__name__,
        )
        return None
