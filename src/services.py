"""Integrações externas da aplicação."""

import logging
import sqlite3
from threading import Lock
import time
from datetime import date, datetime

import requests
from urllib.parse import quote

from src.config import API_BASE_URL, METRICS_DB_PATH

LOGGER = logging.getLogger(__name__)
_STATS_LOCK = Lock()
_STATS = {
    "accesses": 0,
    "searches": 0,
    "positive_searches": 0,
    "negative_searches": 0,
    "failed_searches": 0,
    "breached_sites": 0,
    "confirmed_incidents": 0,
    "plaintext_password_incidents": 0,
    "exposed_password_incidents": 0,
    "exposed_data_types": 0,
    "affected_industries": 0,
    "risk_score_sum": 0,
    "risk_score_count": 0,
    "low_risk_searches": 0,
    "medium_risk_searches": 0,
    "high_risk_searches": 0,
    "critical_risk_searches": 0,
    "affected_records": 0,
    "rendered_reports": 0,
    "translation_fallbacks": 0,
    "translation_rate_limits": 0,
    "translation_requests": 0,
    "translation_successes": 0,
    "translation_errors": 0,
    "render_duration_ms_sum": 0,
    "render_duration_count": 0,
    "reports_with_missing_description": 0,
    "reports_with_missing_domain": 0,
    "reports_with_missing_reference": 0,
    "reports_with_missing_logo": 0,
    "weak_hash_incidents": 0,
    "strong_hash_incidents": 0,
    "reports_with_api_degradation": 0,
}


def _inicializar_metricas():
    METRICS_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(METRICS_DB_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS daily_metrics (
                metric_date TEXT PRIMARY KEY,
                accesses INTEGER NOT NULL DEFAULT 0,
                searches INTEGER NOT NULL DEFAULT 0,
                positive_searches INTEGER NOT NULL DEFAULT 0,
                negative_searches INTEGER NOT NULL DEFAULT 0,
                failed_searches INTEGER NOT NULL DEFAULT 0,
                breached_sites INTEGER NOT NULL DEFAULT 0,
                confirmed_incidents INTEGER NOT NULL DEFAULT 0,
                plaintext_password_incidents INTEGER NOT NULL DEFAULT 0,
                exposed_password_incidents INTEGER NOT NULL DEFAULT 0,
                exposed_data_types INTEGER NOT NULL DEFAULT 0,
                affected_industries INTEGER NOT NULL DEFAULT 0,
                risk_score_sum REAL NOT NULL DEFAULT 0,
                risk_score_count INTEGER NOT NULL DEFAULT 0,
                low_risk_searches INTEGER NOT NULL DEFAULT 0,
                medium_risk_searches INTEGER NOT NULL DEFAULT 0,
                high_risk_searches INTEGER NOT NULL DEFAULT 0,
                critical_risk_searches INTEGER NOT NULL DEFAULT 0,
                affected_records INTEGER NOT NULL DEFAULT 0,
                rendered_reports INTEGER NOT NULL DEFAULT 0,
                translation_fallbacks INTEGER NOT NULL DEFAULT 0,
                translation_rate_limits INTEGER NOT NULL DEFAULT 0,
                translation_requests INTEGER NOT NULL DEFAULT 0,
                translation_successes INTEGER NOT NULL DEFAULT 0,
                translation_errors INTEGER NOT NULL DEFAULT 0,
                render_duration_ms_sum REAL NOT NULL DEFAULT 0,
                render_duration_count INTEGER NOT NULL DEFAULT 0,
                reports_with_missing_description INTEGER NOT NULL DEFAULT 0,
                reports_with_missing_domain INTEGER NOT NULL DEFAULT 0,
                reports_with_missing_reference INTEGER NOT NULL DEFAULT 0,
                reports_with_missing_logo INTEGER NOT NULL DEFAULT 0,
                weak_hash_incidents INTEGER NOT NULL DEFAULT 0,
                strong_hash_incidents INTEGER NOT NULL DEFAULT 0,
                reports_with_api_degradation INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        columns = {
            row[1]
            for row in connection.execute("PRAGMA table_info(daily_metrics)")
        }
        additions = {
            "breached_sites": "INTEGER NOT NULL DEFAULT 0",
            "confirmed_incidents": "INTEGER NOT NULL DEFAULT 0",
            "plaintext_password_incidents": "INTEGER NOT NULL DEFAULT 0",
            "exposed_password_incidents": "INTEGER NOT NULL DEFAULT 0",
            "exposed_data_types": "INTEGER NOT NULL DEFAULT 0",
            "affected_industries": "INTEGER NOT NULL DEFAULT 0",
            "risk_score_sum": "REAL NOT NULL DEFAULT 0",
            "risk_score_count": "INTEGER NOT NULL DEFAULT 0",
            "low_risk_searches": "INTEGER NOT NULL DEFAULT 0",
            "medium_risk_searches": "INTEGER NOT NULL DEFAULT 0",
            "high_risk_searches": "INTEGER NOT NULL DEFAULT 0",
            "critical_risk_searches": "INTEGER NOT NULL DEFAULT 0",
            "affected_records": "INTEGER NOT NULL DEFAULT 0",
            "rendered_reports": "INTEGER NOT NULL DEFAULT 0",
            "translation_fallbacks": "INTEGER NOT NULL DEFAULT 0",
            "translation_rate_limits": "INTEGER NOT NULL DEFAULT 0",
            "translation_requests": "INTEGER NOT NULL DEFAULT 0",
            "translation_successes": "INTEGER NOT NULL DEFAULT 0",
            "translation_errors": "INTEGER NOT NULL DEFAULT 0",
            "render_duration_ms_sum": "REAL NOT NULL DEFAULT 0",
            "render_duration_count": "INTEGER NOT NULL DEFAULT 0",
            "reports_with_missing_description": "INTEGER NOT NULL DEFAULT 0",
            "reports_with_missing_domain": "INTEGER NOT NULL DEFAULT 0",
            "reports_with_missing_reference": "INTEGER NOT NULL DEFAULT 0",
            "reports_with_missing_logo": "INTEGER NOT NULL DEFAULT 0",
            "weak_hash_incidents": "INTEGER NOT NULL DEFAULT 0",
            "strong_hash_incidents": "INTEGER NOT NULL DEFAULT 0",
            "reports_with_api_degradation": "INTEGER NOT NULL DEFAULT 0",
        }
        for coluna, definicao in additions.items():
            if coluna not in columns:
                connection.execute(
                    f"ALTER TABLE daily_metrics ADD COLUMN {coluna} {definicao}"
                )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS affected_sites (
                site_name TEXT PRIMARY KEY,
                occurrences INTEGER NOT NULL DEFAULT 0,
                first_seen TEXT NOT NULL,
                last_seen TEXT NOT NULL
            )
            """
        )
        site_columns = {
            row[1] for row in connection.execute("PRAGMA table_info(affected_sites)")
        }
        if "first_seen" not in site_columns:
            connection.execute(
                "ALTER TABLE affected_sites ADD COLUMN first_seen TEXT NOT NULL DEFAULT ''"
            )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS api_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_time TEXT NOT NULL,
                endpoint TEXT NOT NULL,
                status_code INTEGER,
                duration_ms INTEGER NOT NULL,
                success INTEGER NOT NULL,
                error_type TEXT
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS hourly_metrics (
                metric_date TEXT NOT NULL,
                metric_hour INTEGER NOT NULL,
                accesses INTEGER NOT NULL DEFAULT 0,
                searches INTEGER NOT NULL DEFAULT 0,
                positive_searches INTEGER NOT NULL DEFAULT 0,
                negative_searches INTEGER NOT NULL DEFAULT 0,
                failed_searches INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY (metric_date, metric_hour)
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS exposed_data_types (
                data_type TEXT PRIMARY KEY,
                occurrences INTEGER NOT NULL DEFAULT 0,
                last_seen TEXT NOT NULL
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS affected_industries (
                industry TEXT PRIMARY KEY,
                occurrences INTEGER NOT NULL DEFAULT 0,
                last_seen TEXT NOT NULL
            )
            """
        )


def _atualizar_metricas(**incrementos):
    _inicializar_metricas()
    hoje = date.today().isoformat()
    with sqlite3.connect(METRICS_DB_PATH) as connection:
        connection.execute(
            """
            INSERT INTO daily_metrics (metric_date) VALUES (?)
            ON CONFLICT(metric_date) DO NOTHING
            """,
            (hoje,),
        )
        for coluna, valor in incrementos.items():
            if valor:
                connection.execute(
                    f"UPDATE daily_metrics SET {coluna} = {coluna} + ? WHERE metric_date = ?",
                    (valor, hoje),
                )
        hora = datetime.now().hour
        connection.execute(
            """
            INSERT INTO hourly_metrics (metric_date, metric_hour)
            VALUES (?, ?)
            ON CONFLICT(metric_date, metric_hour) DO NOTHING
            """,
            (hoje, hora),
        )
        for coluna in (
            "accesses",
            "searches",
            "positive_searches",
            "negative_searches",
            "failed_searches",
        ):
            valor = incrementos.get(coluna, 0)
            if valor:
                connection.execute(
                    f"""
                    UPDATE hourly_metrics
                    SET {coluna} = {coluna} + ?
                    WHERE metric_date = ? AND metric_hour = ?
                    """,
                    (valor, hoje, hora),
                )
        totais = connection.execute(
            """
            SELECT COALESCE(SUM(accesses), 0), COALESCE(SUM(searches), 0),
                   COALESCE(SUM(positive_searches), 0), COALESCE(SUM(negative_searches), 0),
                   COALESCE(SUM(failed_searches), 0), COALESCE(SUM(breached_sites), 0),
                   COALESCE(SUM(confirmed_incidents), 0),
                   COALESCE(SUM(plaintext_password_incidents), 0),
                   COALESCE(SUM(exposed_password_incidents), 0),
                   COALESCE(SUM(exposed_data_types), 0),
                   COALESCE(SUM(affected_industries), 0),
                   COALESCE(SUM(risk_score_sum), 0), COALESCE(SUM(risk_score_count), 0),
                   COALESCE(SUM(low_risk_searches), 0), COALESCE(SUM(medium_risk_searches), 0),
                   COALESCE(SUM(high_risk_searches), 0), COALESCE(SUM(critical_risk_searches), 0),
                   COALESCE(SUM(affected_records), 0), COALESCE(SUM(rendered_reports), 0),
                   COALESCE(SUM(translation_fallbacks), 0),
                   COALESCE(SUM(translation_rate_limits), 0),
                   COALESCE(SUM(translation_requests), 0),
                   COALESCE(SUM(translation_successes), 0),
                   COALESCE(SUM(translation_errors), 0),
                   COALESCE(SUM(render_duration_ms_sum), 0),
                   COALESCE(SUM(render_duration_count), 0),
                   COALESCE(SUM(reports_with_missing_description), 0),
                   COALESCE(SUM(reports_with_missing_domain), 0),
                   COALESCE(SUM(reports_with_missing_reference), 0),
                   COALESCE(SUM(reports_with_missing_logo), 0),
                   COALESCE(SUM(weak_hash_incidents), 0),
                   COALESCE(SUM(strong_hash_incidents), 0),
                   COALESCE(SUM(reports_with_api_degradation), 0)
            FROM daily_metrics
            """
        ).fetchone()
    return dict(zip(_STATS, totais))


def registrar_evento_api(endpoint, status_code, inicio, error_type=None):
    """Persiste telemetria técnica da API, sem dados da consulta."""
    _inicializar_metricas()
    duracao_ms = round((time.monotonic() - inicio) * 1000)
    with sqlite3.connect(METRICS_DB_PATH) as connection:
        connection.execute(
            """
            INSERT INTO api_events
                (event_time, endpoint, status_code, duration_ms, success, error_type)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.now().isoformat(timespec="seconds"),
                endpoint,
                status_code,
                duracao_ms,
                int(status_code == 200 and error_type is None),
                error_type,
            ),
        )


def registrar_telemetria(nome, quantidade=1):
    """Registra métricas internas agregadas, sem identificadores pessoais."""
    if nome not in _STATS or not quantidade:
        return
    with _STATS_LOCK:
        _STATS[nome] += quantidade
        _atualizar_metricas(**{nome: quantidade})


def registrar_acesso():
    """Registra um acesso à aplicação e exibe o contador no terminal."""
    with _STATS_LOCK:
        _STATS["accesses"] += 1
        metricas = _atualizar_metricas(accesses=1)
    LOGGER.info(
        "\n%s\n📊 ACESSO À APLICAÇÃO\n   Total de acessos: %s\n%s",
        "-" * 56,
        metricas["accesses"],
        "-" * 56,
    )


def registrar_busca(resultado, detalhes=None, analytics=None):
    """Atualiza as métricas de busca sem registrar dados pessoais."""
    detalhes = detalhes or []
    sites = {
        str(item.get("breach", "")).strip()
        for item in detalhes
        if isinstance(item, dict) and str(item.get("breach", "")).strip()
    }
    sites.update(
        str(site).strip()
        for site in (resultado if isinstance(resultado, list) else [])
        if str(site).strip()
    )
    confirmados = sum(
        str(item.get("verified", "")).lower() == "yes"
        for item in detalhes
        if isinstance(item, dict)
    )
    plaintext = sum(
        "plain" in str(item.get("password_risk", "")).lower()
        for item in detalhes
        if isinstance(item, dict)
    )
    senhas_expostas = sum(
        "password" in str(item.get("xposed_data", "")).lower()
        for item in detalhes
        if isinstance(item, dict)
    )
    hashes_fracos = sum(
        any(
            marcador in str(item.get("password_risk", "")).lower()
            for marcador in ("weak", "fraco", "md5", "sha1", "unsalted")
        )
        for item in detalhes
        if isinstance(item, dict)
    )
    hashes_fortes = sum(
        any(
            marcador in str(item.get("password_risk", "")).lower()
            for marcador in ("strong", "forte", "bcrypt", "scrypt", "argon")
        )
        for item in detalhes
        if isinstance(item, dict)
    )
    tipos_dados = {
        str(item).strip().lower()
        for detalhe in detalhes
        if isinstance(detalhe, dict)
        for item in str(detalhe.get("xposed_data", "")).replace(",", "|").split("|")
        if str(item).strip()
    }
    setores = {
        str(item.get("industry", "")).strip().lower()
        for item in detalhes
        if isinstance(item, dict) and str(item.get("industry", "")).strip()
    }
    risco = analytics.get("BreachMetrics", {}).get("risk", []) if analytics else []
    risco = risco[0] if isinstance(risco, list) and risco else risco
    score = risco.get("risk_score") if isinstance(risco, dict) else None
    try:
        score = float(score)
    except (TypeError, ValueError):
        score = None
    nivel = str(risco.get("risk_label", "") if isinstance(risco, dict) else "").lower()
    registros = sum(
        int(item.get("xposed_records", 0) or 0)
        for item in detalhes
        if isinstance(item, dict) and str(item.get("xposed_records", "")).isdigit()
    )
    campos_ausentes = {
        "reports_with_missing_description": int(
            any(not str(item.get("description", "")).strip() for item in detalhes if isinstance(item, dict))
        ),
        "reports_with_missing_domain": int(
            any(not str(item.get("domain", "")).strip() for item in detalhes if isinstance(item, dict))
        ),
        "reports_with_missing_reference": int(
            any(
                not str(item.get("reference", item.get("references", ""))).strip()
                for item in detalhes
                if isinstance(item, dict)
            )
        ),
        "reports_with_missing_logo": int(
            any(
                not str(item.get("logo", item.get("logo_url", ""))).strip()
                for item in detalhes
                if isinstance(item, dict)
            )
        ),
    }
    incrementos = {
        "searches": 1,
        "positive_searches": int(bool(resultado)),
        "negative_searches": int(resultado == []),
        "failed_searches": int(resultado is None),
        "breached_sites": len(sites),
        "confirmed_incidents": confirmados,
        "plaintext_password_incidents": plaintext,
        "exposed_password_incidents": senhas_expostas,
        "exposed_data_types": len(tipos_dados),
        "affected_industries": len(setores),
        "risk_score_sum": score or 0,
        "risk_score_count": int(score is not None),
        "low_risk_searches": int(nivel in ("low", "baixo")),
        "medium_risk_searches": int(nivel in ("medium", "moderate", "médio", "moderado")),
        "high_risk_searches": int(nivel in ("high", "alto")),
        "critical_risk_searches": int(nivel in ("critical", "crítico")),
        "affected_records": registros,
        "weak_hash_incidents": hashes_fracos,
        "strong_hash_incidents": hashes_fortes,
        "reports_with_api_degradation": int(analytics is None and bool(resultado)),
        **campos_ausentes,
    }
    with _STATS_LOCK:
        _STATS["searches"] += 1
        if resultado is None:
            _STATS["failed_searches"] += 1
        elif resultado:
            _STATS["positive_searches"] += 1
        else:
            _STATS["negative_searches"] += 1
        metricas = _atualizar_metricas(**incrementos)
        hoje = date.today().isoformat()
        with sqlite3.connect(METRICS_DB_PATH) as connection:
            for site in sites:
                connection.execute(
                    """
                    INSERT INTO affected_sites (site_name, occurrences, first_seen, last_seen)
                    VALUES (?, 1, ?, ?)
                    ON CONFLICT(site_name) DO UPDATE SET
                        occurrences = occurrences + 1,
                        last_seen = excluded.last_seen
                    """,
                    (site, hoje, hoje),
                )
            for tabela, valores in (
                ("exposed_data_types", tipos_dados),
                ("affected_industries", setores),
            ):
                coluna = "data_type" if tabela == "exposed_data_types" else "industry"
                for valor in valores:
                    connection.execute(
                        f"""
                        INSERT INTO {tabela} ({coluna}, occurrences, last_seen)
                        VALUES (?, 1, ?)
                        ON CONFLICT({coluna}) DO UPDATE SET
                            occurrences = occurrences + 1, last_seen = excluded.last_seen
                        """,
                        (valor, hoje),
                    )
    LOGGER.info(
        "\n%s\n🔎 RESUMO DAS BUSCAS\n   Acessos: %s\n   Buscas totais: %s\n   ✅ Positivas: %s\n   ⚪ Negativas: %s\n   ❌ Falhas: %s\n   🌐 Sites afetados: %s\n   ✔️ Incidentes confirmados: %s\n   🔓 Incidentes com senha em texto puro: %s\n   🔑 Incidentes com senha exposta: %s\n   🧩 Tipos de dados: %s\n   🏢 Setores afetados: %s\n   ⚠️ Risco: baixo %s | médio %s | alto %s | crítico %s\n   📊 Registros afetados: %s\n   🧪 Hashes fracos: %s | fortes: %s\n   🌐 Respostas degradadas da API: %s\n   🌍 Traduções: %s solicitações | %s sucesso | %s fallback | %s erros\n%s",
        "-" * 56,
        metricas["accesses"],
        metricas["searches"],
        metricas["positive_searches"],
        metricas["negative_searches"],
        metricas["failed_searches"],
        metricas["breached_sites"],
        metricas["confirmed_incidents"],
        metricas["plaintext_password_incidents"],
        metricas["exposed_password_incidents"],
        metricas["exposed_data_types"],
        metricas["affected_industries"],
        metricas["low_risk_searches"],
        metricas["medium_risk_searches"],
        metricas["high_risk_searches"],
        metricas["critical_risk_searches"],
        metricas["affected_records"],
        metricas["weak_hash_incidents"],
        metricas["strong_hash_incidents"],
        metricas["reports_with_api_degradation"],
        metricas["translation_requests"],
        metricas["translation_successes"],
        metricas["translation_fallbacks"],
        metricas["translation_errors"],
        "-" * 56,
    )


def registrar_renderizacao(duracao_ms):
    registrar_telemetria("rendered_reports")
    registrar_telemetria("render_duration_ms_sum", duracao_ms)
    registrar_telemetria("render_duration_count")


def buscar_vazamentos(email):
    """Consulta os vazamentos associados ao e-mail."""
    inicio = time.monotonic()
    LOGGER.info("Consulta de vazamentos iniciada")
    try:
        response = requests.get(
            f"{API_BASE_URL}/v1/check-email/{quote(email)}",
            timeout=20,
        )
        registrar_evento_api(
            "check-email",
            response.status_code,
            inicio,
            None if response.status_code == 200 else "http_error",
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
        registrar_evento_api("check-email", None, inicio, type(error).__name__)
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
        registrar_evento_api(
            "breach-analytics",
            response.status_code,
            inicio,
            None if response.status_code == 200 else "http_error",
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
        registrar_evento_api("breach-analytics", None, inicio, type(error).__name__)
        LOGGER.error(
            "Erro na consulta de analytics (%.2fs): %s",
            time.monotonic() - inicio,
            type(error).__name__,
        )
        return None
