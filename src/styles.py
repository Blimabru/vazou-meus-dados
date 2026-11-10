"""Folha de estilos visual da aplicação Streamlit.

O CSS é mantido em uma constante para ser aplicado em um único ponto do fluxo
principal, garantindo consistência visual entre cartões, métricas e impressão.
"""

# O bloco é injetado no documento pelo Streamlit; por isso permanece como uma
# string literal em vez de um arquivo CSS separado.
CSS = """
<style>
/* Base escura e espaçamento inferior para acomodar o rodapé fixo. */
.main {
    background: linear-gradient(180deg, #0f172a 0%, #111827 100%);
    padding-bottom: 8rem;
}
.logo-wrap { margin: 0 auto 1rem; display: flex; justify-content: center; }
/* Elementos de identidade e cartões usam contraste alto para acessibilidade. */
.app-subtitle { text-align: center; font-size: 1.05rem; color: #dfe7f5; margin-bottom: 1rem; }
/* Cartões de incidentes agrupam informações semânticas e mantêm hierarquia. */
.breach-card {
    background: linear-gradient(180deg, rgba(15, 23, 42, .85), rgba(17, 24, 39, .95));
    border: 1px solid rgba(148, 163, 184, .25);
    border-radius: 18px; padding: 1.1rem; margin: .7rem 0;
    box-shadow: 0 10px 25px rgba(15, 23, 42, .25);
}
.breach-card h4 { margin: 0 0 .3rem; color: #f8fafc; }
.breach-logo { width: 42px; height: 42px; object-fit: contain; float: right; border-radius: 10px; margin-left: .75rem; }
.breach-logo-wrap {
    display: flex; align-items: center; justify-content: center;
    min-height: 180px; width: 100%;
}
.breach-logo-large {
    width: 100%; height: 180px; object-fit: contain;
    display: block; border-radius: 14px;
}
[class*="st-key-breach-card-"] {
    border-radius: 18px;
    transition: background-color .2s ease, box-shadow .2s ease;
}
[class*="st-key-breach-card-"]:hover {
    background-color: rgba(226, 232, 240, .08);
    box-shadow: 0 8px 20px rgba(226, 232, 240, .08);
}
.breach-meta { color: #cbd5e1; font-size: .92rem; margin-bottom: .75rem; }
.chip {
    display: inline-block; background: rgba(56, 189, 248, .12); color: #bae6fd;
    border: 1px solid rgba(125, 211, 252, .28); border-radius: 999px;
    padding: .28rem .7rem; margin: .2rem .35rem .2rem 0; font-size: .76rem;
    font-weight: 600;
}
.chip-danger {
    background: rgba(239, 68, 68, .18);
    color: #fecaca;
    border-color: rgba(248, 113, 113, .65);
}
.exposed-data-label {
    display: inline-block; margin-right: .4rem; color: #f8fafc; font-weight: 700;
}
/* Cores de risco são consistentes com os níveis exibidos pelo relatório. */
.risk-badge {
    display: inline-block; padding: .3rem .7rem; border-radius: 999px;
    font-size: .8rem; font-weight: 700; margin-bottom: .7rem;
}
.risk-high { background: rgba(239, 68, 68, .12); color: #fca5a5; border: 1px solid rgba(248, 113, 113, .4); }
.risk-medium { background: rgba(245, 158, 11, .12); color: #fbbf24; border: 1px solid rgba(251, 191, 36, .4); }
.risk-low { background: rgba(34, 197, 94, .12); color: #86efac; border: 1px solid rgba(74, 222, 128, .4); }
/* Métricas têm altura fixa para evitar deslocamentos entre colunas. */
.metric-box {
    background: linear-gradient(180deg, rgba(15, 23, 42, .88), rgba(30, 41, 59, .9));
    border: 1px solid rgba(148, 163, 184, .2); border-radius: 18px;
    box-sizing: border-box; height: 140px; padding: 1rem; box-shadow: 0 8px 18px rgba(15, 23, 42, .18);
}
.metric-box .value { font-size: 2.1rem; font-weight: 800; color: #f8fafc; margin-bottom: .4rem; }
.metric-box .label { color: #cbd5e1; font-size: .85rem; text-transform: uppercase; letter-spacing: .08em; }
/* Área de confirmação usa SVG para manter o indicador nítido e acessível. */
.confirmation-metric {
    box-sizing: border-box; height: 140px; padding: 1rem;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
}
.confirmation-label {
    color: #cbd5e1; font-size: .8rem; line-height: 1.2;
    margin-bottom: .7rem; text-align: center;
}
.confirmation-value {
    display: flex; align-items: center; justify-content: center; gap: .55rem;
    color: #f8fafc; font-size: 1.2rem; font-weight: 700;
}
.confirmation-icon {
    width: 2.2rem; height: 2.2rem; fill: none;
    stroke-width: 2.8; stroke-linecap: round; stroke-linejoin: round;
}
.confirmation-icon-ok { stroke: #4ade80; }
.confirmation-icon-no { stroke: #fb7185; }
.summary-note {
    background: rgba(30, 41, 59, .75); border-left: 4px solid #38bdf8;
    border-radius: 12px; padding: .9rem 1rem; color: #e2e8f0; margin: .8rem 0 1.2rem;
}
.section-title { color: #f8fafc; margin-top: 1.5rem; margin-bottom: .8rem; }
.st-key-clear-search button {
    background: #2563eb; border-color: #3b82f6; color: #eff6ff;
}
.st-key-clear-search button:hover {
    background: #1d4ed8; border-color: #60a5fa; color: #ffffff;
}

/* O rodapé não deve consumir espaço no relatório impresso. */
@media print {
    .app-footer-fixed { display: none !important; }
}
/* Cabeçalho e rodapé compartilham a linguagem visual da aplicação. */
.app-header {
    display: flex; align-items: center; justify-content: space-between; gap: 1rem;
    background: rgba(15, 23, 42, .86); border: 1px solid rgba(148, 163, 184, .2);
    border-radius: 18px; padding: .55rem .85rem; margin-bottom: .8rem;
}
.brand-block { display: flex; align-items: center; gap: .8rem; min-width: 260px; }
.brand-logo { width: 58px; height: 58px; object-fit: contain; border-radius: 12px; }
.brand-title { font-size: 1.25rem; font-weight: 800; color: #f8fafc; }
.brand-subtitle { font-size: .72rem; color: #cbd5e1; letter-spacing: .05em; text-transform: uppercase; }
.brand-copy { display: flex; flex-direction: column; }
.nav-links { display: flex; flex-wrap: wrap; justify-content: center; gap: .75rem; }
.nav-item, .status-pill { border-radius: 999px; padding: .35rem .8rem; font-size: .75rem; font-weight: 600; }
.nav-item { color: #cbd5e1; background: rgba(30, 41, 59, .7); border: 1px solid rgba(148, 163, 184, .18); }
.status-pill { background: rgba(34, 197, 94, .1); border: 1px solid rgba(74, 222, 128, .35); color: #86efac; white-space: nowrap; }
.app-footer {
    background: rgba(15, 23, 42, .88); border-top: 1px solid rgba(148, 163, 184, .2);
    border-radius: 14px 14px 0 0; padding: .85rem 1rem .65rem; margin-top: 1.5rem; color: #e2e8f0;
}
.footer-brand-block { display: flex; align-items: center; gap: .8rem; }
.footer-logo { width: 42px; height: 42px; object-fit: contain; border-radius: 10px; }
.footer-brand { font-size: 1rem; font-weight: 800; color: #f8fafc; margin-bottom: .35rem; }
.footer-copy { color: #cbd5e1; font-size: .82rem; margin-bottom: .8rem; }
.footer-links { display: flex; flex-wrap: wrap; gap: .75rem; color: #a5f3fc; font-size: .75rem; font-weight: 600; }
.footer-links a { color: #a5f3fc; text-decoration: none; }
.app-footer-fixed {
    position: fixed;
    z-index: 100;
    left: 1rem;
    right: 1rem;
    bottom: .75rem;
    background: rgba(15, 23, 42, .97);
    border: 1px solid rgba(148, 163, 184, .25);
    border-radius: 14px;
    padding: .65rem 1rem;
    box-shadow: 0 12px 30px rgba(0, 0, 0, .3);
}
.footer-fixed-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
}
.footer-fixed-brand {
    display: flex;
    align-items: center;
    gap: .4rem;
    color: #f8fafc;
    font-size: .82rem;
    font-weight: 700;
    line-height: 1.2;
}
.footer-fixed-logo {
    width: 36px;
    height: 36px;
    object-fit: contain;
    border-radius: 8px;
    display: block;
}
.footer-fixed-copy {
    color: #94a3b8;
    font-size: .72rem;
    font-weight: 400;
}
.footer-fixed-links {
    display: flex;
    gap: .8rem;
    white-space: nowrap;
}
.footer-fixed-links a {
    color: #a5f3fc;
    font-size: .72rem;
    text-decoration: none;
}
.gauge-card {
    background: linear-gradient(180deg, rgba(15, 23, 42, .88), rgba(30, 41, 59, .9));
    border: 1px solid rgba(148, 163, 184, .2); border-radius: 18px;
    padding: 1.1rem; text-align: center; min-height: 220px;
}
.gauge {
    width: 170px; height: 85px; margin: .8rem auto 0;
    border-radius: 170px 170px 0 0; position: relative; overflow: hidden;
    background: conic-gradient(from 270deg at 50% 100%, #22c55e 0deg, #facc15 90deg, #f97316 135deg, #ef4444 180deg, transparent 180deg);
}
.gauge::after {
    content: ""; position: absolute; width: 128px; height: 64px; left: 21px; bottom: 0;
    border-radius: 128px 128px 0 0; background: #111827;
}
.gauge-score {
    position: absolute; z-index: 1; bottom: .25rem; left: 0; right: 0;
    color: #f8fafc; font-size: 1.6rem; font-weight: 800;
}
.gauge-label { color: #fb923c; font-size: 1rem; font-weight: 700; margin-top: .55rem; }
.result-card {
    background: rgba(30, 41, 59, .72); border: 1px solid rgba(148, 163, 184, .2);
    border-radius: 16px; padding: 1rem; min-height: 116px;
}
.result-card .result-title { color: #f8fafc; font-size: 1rem; font-weight: 700; margin-bottom: .4rem; }
.result-card .result-text { color: #cbd5e1; font-size: .9rem; line-height: 1.45; }
.recommendation-card {
    display: flex; align-items: center; gap: .75rem; min-height: 86px;
    box-sizing: border-box; padding: 1rem; border-radius: 18px;
    background: transparent;
    border: 1px solid #22c55e;
    box-shadow: none;
    transition: background .2s ease, box-shadow .2s ease;
}
.recommendation-card:hover {
    background: rgba(34, 197, 94, .2);
    box-shadow: 0 0 16px rgba(34, 197, 94, .16);
}
.recommendation-row-gap { height: .75rem; }
.recommendation-icon { font-size: 1.45rem; line-height: 1; }
.recommendation-text { color: #dcfce7; font-size: .88rem; font-weight: 700; line-height: 1.35; }
.loading-screen {
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    min-height: 280px; padding: 2rem; text-align: center;
}
.loading-spinner {
    width: 58px; height: 58px; border: 5px solid rgba(56, 189, 248, .2);
    border-top-color: #38bdf8; border-right-color: #8b5cf6;
    border-radius: 50%; animation: spin 0.85s linear infinite;
}
.loading-title { color: #f8fafc; font-size: 1.15rem; font-weight: 700; margin-top: 1rem; }
.loading-copy { color: #94a3b8; font-size: .85rem; margin-top: .35rem; }
@keyframes spin { to { transform: rotate(360deg); } }
.risk-score-card {
    background: linear-gradient(180deg, rgba(15, 23, 42, .88), rgba(30, 41, 59, .9));
    border: 1px solid rgba(148, 163, 184, .2); border-radius: 18px;
    box-sizing: border-box; height: 140px; padding: 1rem;
}
.risk-score-heading { display: flex; justify-content: space-between; gap: .75rem; color: #cbd5e1; font-size: .82rem; }
.risk-score-heading strong { color: #f8fafc; font-size: 1.35rem; }
.risk-track { height: 12px; background: linear-gradient(90deg, #22c55e 0 25%, #facc15 25% 50%, #f97316 50% 75%, #ef4444 75%); border-radius: 999px; margin: 1.1rem 0 .4rem; overflow: hidden; }
.risk-fill { height: 100%; background: transparent; border-right: 3px solid #f8fafc; box-sizing: border-box; }
.risk-scale { display: flex; justify-content: space-between; color: #94a3b8; font-size: .65rem; }
.risk-level { color: #fb923c; font-size: .9rem; font-weight: 700; margin-top: .75rem; text-align: center; }
@media (max-width: 900px) {
    .app-header { flex-direction: column; align-items: flex-start; }
    .nav-links { justify-content: flex-start; }
    .app-footer-fixed { left: .5rem; right: .5rem; bottom: .5rem; }
    .footer-fixed-copy { display: none; }
}
</style>
"""
