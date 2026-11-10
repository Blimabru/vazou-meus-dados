"""Folha de estilos visual da aplicação Streamlit.

O CSS é mantido em uma constante para ser aplicado em um único ponto do fluxo
principal, garantindo consistência visual entre cartões, métricas, temas claro/escuro
e impressão.
"""

# O bloco é injetado no documento pelo Streamlit; por isso permanece como uma
# string literal em vez de um arquivo CSS separado.
# As cores usam ``light-dark()`` para acompanhar o ``color-scheme`` definido
# pelo Streamlit em ``[data-testid="stApp"]`` nos temas claro e escuro, com
# fallback explícito de alto contraste para o tema claro.
CSS = """
<style>
/* Espaçamento inferior para acomodar o rodapé fixo sem sobrepor conteúdo. */
[data-testid="stMainBlockContainer"],
.main {
    padding-bottom: 7.5rem;
}
.logo-wrap { margin: 0 auto 1rem; display: flex; justify-content: center; }
/* Elementos de identidade e cartões usam contraste alto para acessibilidade. */
.app-subtitle {
    text-align: center;
    font-size: 1.05rem;
    color: #334155;
    color: light-dark(#334155, #dfe7f5);
    margin-bottom: 1rem;
}
/* Cartões de incidentes agrupam informações semânticas e mantêm hierarquia. */
.breach-card {
    background: #ffffff;
    background: linear-gradient(
        180deg,
        light-dark(#ffffff, rgba(15, 23, 42, .85)),
        light-dark(#f8fafc, rgba(17, 24, 39, .95))
    );
    border: 1px solid #cbd5e1;
    border-color: light-dark(#cbd5e1, rgba(148, 163, 184, .25));
    border-radius: 18px; padding: 1.1rem; margin: .7rem 0;
    box-shadow: 0 6px 18px rgba(15, 23, 42, .08);
    box-shadow: 0 10px 25px light-dark(rgba(15, 23, 42, .08), rgba(15, 23, 42, .25));
}
.breach-card h4 {
    margin: 0 0 .3rem;
    color: #0f172a;
    color: light-dark(#0f172a, #f8fafc);
}
.breach-logo { width: 42px; height: 42px; object-fit: contain; float: right; border-radius: 10px; margin-left: .75rem; }
.breach-logo-wrap {
    display: flex; align-items: center; justify-content: center;
    min-height: 180px; width: 100%;
    padding: .5rem; box-sizing: border-box;
    border-radius: 14px;
    background: #f8fafc;
    background: light-dark(#f8fafc, rgba(255, 255, 255, .04));
    border: 1px solid #e2e8f0;
    border-color: light-dark(#e2e8f0, rgba(148, 163, 184, .16));
}
.breach-logo-large {
    width: 100%; height: 180px; object-fit: contain;
    display: block; border-radius: 10px;
}
[class*="st-key-breach-card-"] {
    border-radius: 18px;
    transition: background-color .2s ease, box-shadow .2s ease;
}
[class*="st-key-breach-card-"]:hover {
    background-color: #f8fafc;
    background-color: light-dark(#f8fafc, rgba(226, 232, 240, .08));
    box-shadow: 0 8px 20px rgba(15, 23, 42, .08);
    box-shadow: 0 8px 20px light-dark(rgba(15, 23, 42, .08), rgba(226, 232, 240, .08));
}
.breach-meta {
    color: #475569;
    color: light-dark(#475569, #cbd5e1);
    font-size: .92rem; margin-bottom: .75rem;
}
.chip {
    display: inline-block;
    background: #e0f2fe;
    background: light-dark(#e0f2fe, rgba(56, 189, 248, .12));
    color: #075985;
    color: light-dark(#075985, #bae6fd);
    border: 1px solid #7dd3fc;
    border-color: light-dark(#7dd3fc, rgba(125, 211, 252, .28));
    border-radius: 999px;
    padding: .28rem .7rem; margin: .2rem .35rem .2rem 0; font-size: .76rem;
    font-weight: 600;
}
.chip-danger {
    background: #fee2e2;
    background: light-dark(#fee2e2, rgba(239, 68, 68, .18));
    color: #991b1b;
    color: light-dark(#991b1b, #fecaca);
    border-color: #f87171;
    border-color: light-dark(#f87171, rgba(248, 113, 113, .65));
}
.exposed-data-label {
    display: inline-block; margin-right: .4rem;
    color: #0f172a;
    color: light-dark(#0f172a, #f8fafc);
    font-weight: 700;
}
/* Cores de risco são consistentes com os níveis exibidos pelo relatório. */
.risk-badge {
    display: inline-block; padding: .3rem .7rem; border-radius: 999px;
    font-size: .8rem; font-weight: 700; margin-bottom: .7rem;
}
.risk-high {
    background: #fee2e2; background: light-dark(#fee2e2, rgba(239, 68, 68, .12));
    color: #991b1b; color: light-dark(#991b1b, #fca5a5);
    border: 1px solid #f87171; border-color: light-dark(#f87171, rgba(248, 113, 113, .4));
}
.risk-medium {
    background: #fef3c7; background: light-dark(#fef3c7, rgba(245, 158, 11, .12));
    color: #92400e; color: light-dark(#92400e, #fbbf24);
    border: 1px solid #f59e0b; border-color: light-dark(#f59e0b, rgba(251, 191, 36, .4));
}
.risk-low {
    background: #dcfce7; background: light-dark(#dcfce7, rgba(34, 197, 94, .12));
    color: #166534; color: light-dark(#166534, #86efac);
    border: 1px solid #4ade80; border-color: light-dark(#4ade80, rgba(74, 222, 128, .4));
}
/* Métricas têm altura fixa para evitar deslocamentos entre colunas. */
.metric-box {
    background: #f8fafc;
    background: linear-gradient(
        180deg,
        light-dark(#ffffff, rgba(15, 23, 42, .88)),
        light-dark(#f8fafc, rgba(30, 41, 59, .9))
    );
    border: 1px solid #cbd5e1;
    border-color: light-dark(#cbd5e1, rgba(148, 163, 184, .2));
    border-radius: 18px;
    box-sizing: border-box; height: 140px; padding: 1rem;
    box-shadow: 0 4px 12px rgba(15, 23, 42, .06);
    box-shadow: 0 8px 18px light-dark(rgba(15, 23, 42, .06), rgba(15, 23, 42, .18));
}
.metric-box .value {
    font-size: 2.1rem; font-weight: 800;
    color: #0f172a;
    color: light-dark(#0f172a, #f8fafc);
    margin-bottom: .4rem;
}
.metric-box .label {
    color: #475569;
    color: light-dark(#475569, #cbd5e1);
    font-size: .85rem; text-transform: uppercase; letter-spacing: .08em;
}
/* Área de confirmação usa SVG para manter o indicador nítido e acessível. */
.confirmation-metric {
    box-sizing: border-box; height: 140px; padding: 1rem;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
}
.confirmation-label {
    color: #475569;
    color: light-dark(#475569, #cbd5e1);
    font-size: .8rem; line-height: 1.2;
    margin-bottom: .7rem; text-align: center;
}
.confirmation-value {
    display: flex; align-items: center; justify-content: center; gap: .55rem;
    color: #0f172a;
    color: light-dark(#0f172a, #f8fafc);
    font-size: 1.2rem; font-weight: 700;
}
.confirmation-icon {
    width: 2.2rem; height: 2.2rem; fill: none;
    stroke-width: 2.8; stroke-linecap: round; stroke-linejoin: round;
}
.confirmation-icon-ok {
    stroke: #15803d;
    stroke: light-dark(#15803d, #4ade80);
}
.confirmation-icon-no {
    stroke: #be123c;
    stroke: light-dark(#be123c, #fb7185);
}
.summary-note {
    background: #f1f5f9;
    background: light-dark(#f1f5f9, rgba(30, 41, 59, .75));
    border-left: 4px solid #0284c7;
    border-left-color: light-dark(#0284c7, #38bdf8);
    border-radius: 12px; padding: .9rem 1rem;
    color: #1e293b;
    color: light-dark(#1e293b, #e2e8f0);
    margin: .8rem 0 1.2rem;
}
.section-title {
    margin-top: 1.5rem; margin-bottom: .8rem;
}
.section-title,
.section-title h3 {
    color: #0f172a;
    color: light-dark(#0f172a, #f8fafc);
}
.st-key-clear-search button,
.st-key-clear-search button p {
    color: #ffffff;
}
.st-key-clear-search button {
    background: #1d4ed8; border-color: #1d4ed8;
}
.st-key-clear-search button:hover,
.st-key-clear-search button:focus-visible {
    background: #1e40af; border-color: #1e3a8a; color: #ffffff;
}

/* O rodapé não deve consumir espaço no relatório impresso. */
@media print {
    .app-footer-fixed { display: none !important; }
    [data-testid="stMainBlockContainer"],
    .main { padding-bottom: 0 !important; }
}
/* Cabeçalho e rodapé compartilham a linguagem visual da aplicação. */
.app-header {
    display: flex; align-items: center; justify-content: space-between; gap: 1rem;
    background: #ffffff;
    background: light-dark(#ffffff, rgba(15, 23, 42, .86));
    border: 1px solid #cbd5e1;
    border-color: light-dark(#cbd5e1, rgba(148, 163, 184, .2));
    border-radius: 18px; padding: .55rem .85rem; margin-bottom: .8rem;
}
.brand-block { display: flex; align-items: center; gap: .8rem; min-width: 260px; }
.brand-logo { width: 58px; height: 58px; object-fit: contain; border-radius: 12px; }
.brand-title {
    font-size: 1.25rem; font-weight: 800;
    color: #0f172a;
    color: light-dark(#0f172a, #f8fafc);
}
.brand-subtitle {
    font-size: .72rem;
    color: #475569;
    color: light-dark(#475569, #cbd5e1);
    letter-spacing: .05em; text-transform: uppercase;
}
.brand-copy { display: flex; flex-direction: column; }
.nav-links { display: flex; flex-wrap: wrap; justify-content: center; gap: .75rem; }
.nav-item, .status-pill { border-radius: 999px; padding: .35rem .8rem; font-size: .75rem; font-weight: 600; }
.nav-item {
    color: #334155;
    color: light-dark(#334155, #cbd5e1);
    background: #f1f5f9;
    background: light-dark(#f1f5f9, rgba(30, 41, 59, .7));
    border: 1px solid #cbd5e1;
    border-color: light-dark(#cbd5e1, rgba(148, 163, 184, .18));
}
.status-pill {
    background: #dcfce7;
    background: light-dark(#dcfce7, rgba(34, 197, 94, .1));
    border: 1px solid #16a34a;
    border-color: light-dark(#16a34a, rgba(74, 222, 128, .35));
    color: #166534;
    color: light-dark(#166534, #86efac);
    white-space: nowrap;
}
.app-footer {
    background: #f8fafc;
    background: light-dark(#f8fafc, rgba(15, 23, 42, .88));
    border-top: 1px solid #cbd5e1;
    border-top-color: light-dark(#cbd5e1, rgba(148, 163, 184, .2));
    border-radius: 14px 14px 0 0; padding: .85rem 1rem .65rem; margin-top: 1.5rem;
    color: #1e293b;
    color: light-dark(#1e293b, #e2e8f0);
}
.footer-brand-block { display: flex; align-items: center; gap: .8rem; }
.footer-logo { width: 42px; height: 42px; object-fit: contain; border-radius: 10px; }
.footer-brand {
    font-size: 1rem; font-weight: 800;
    color: #0f172a;
    color: light-dark(#0f172a, #f8fafc);
    margin-bottom: .35rem;
}
.footer-copy {
    color: #475569;
    color: light-dark(#475569, #cbd5e1);
    font-size: .82rem; margin-bottom: .8rem;
}
.footer-links {
    display: flex; flex-wrap: wrap; gap: .75rem;
    color: #0369a1;
    color: light-dark(#0369a1, #a5f3fc);
    font-size: .75rem; font-weight: 600;
}
.footer-links a {
    color: #0369a1;
    color: light-dark(#0369a1, #a5f3fc);
    text-decoration: none;
}
.app-footer-fixed {
    position: fixed;
    z-index: 100;
    left: 1rem;
    right: 1rem;
    bottom: .75rem;
    background: rgba(255, 255, 255, .96);
    background: light-dark(rgba(255, 255, 255, .96), rgba(15, 23, 42, .97));
    backdrop-filter: blur(8px);
    border: 1px solid #cbd5e1;
    border-color: light-dark(#cbd5e1, rgba(148, 163, 184, .25));
    border-radius: 14px;
    padding: .65rem 1rem;
    box-shadow: 0 10px 26px rgba(15, 23, 42, .12);
    box-shadow: 0 12px 30px light-dark(rgba(15, 23, 42, .12), rgba(0, 0, 0, .3));
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
    color: #0f172a;
    color: light-dark(#0f172a, #f8fafc);
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
    color: #475569;
    color: light-dark(#475569, #cbd5e1);
    font-size: .72rem;
    font-weight: 400;
}
.footer-fixed-links {
    display: flex;
    gap: .8rem;
    white-space: nowrap;
}
.footer-fixed-links a {
    color: #0369a1;
    color: light-dark(#0369a1, #a5f3fc);
    font-size: .75rem;
    font-weight: 600;
    text-decoration: none;
}
.footer-fixed-links a:hover {
    text-decoration: underline;
}
.gauge-card {
    background: #ffffff;
    background: linear-gradient(
        180deg,
        light-dark(#ffffff, rgba(15, 23, 42, .88)),
        light-dark(#f8fafc, rgba(30, 41, 59, .9))
    );
    border: 1px solid #cbd5e1;
    border-color: light-dark(#cbd5e1, rgba(148, 163, 184, .2));
    border-radius: 18px;
    padding: 1.1rem; text-align: center; min-height: 220px;
}
.gauge {
    width: 170px; height: 85px; margin: .8rem auto 0;
    border-radius: 170px 170px 0 0; position: relative; overflow: hidden;
    background: conic-gradient(from 270deg at 50% 100%, #22c55e 0deg, #facc15 90deg, #f97316 135deg, #ef4444 180deg, transparent 180deg);
}
.gauge::after {
    content: ""; position: absolute; width: 128px; height: 64px; left: 21px; bottom: 0;
    border-radius: 128px 128px 0 0;
    background: #ffffff;
    background: light-dark(#ffffff, #111827);
}
.gauge-score {
    position: absolute; z-index: 1; bottom: .25rem; left: 0; right: 0;
    color: #0f172a;
    color: light-dark(#0f172a, #f8fafc);
    font-size: 1.6rem; font-weight: 800;
}
.gauge-label {
    color: #c2410c;
    color: light-dark(#c2410c, #fb923c);
    font-size: 1rem; font-weight: 700; margin-top: .55rem;
}
.result-card {
    background: #f8fafc;
    background: light-dark(#f8fafc, rgba(30, 41, 59, .72));
    border: 1px solid #cbd5e1;
    border-color: light-dark(#cbd5e1, rgba(148, 163, 184, .2));
    border-radius: 16px; padding: 1rem; min-height: 116px;
}
.result-card .result-title {
    color: #0f172a;
    color: light-dark(#0f172a, #f8fafc);
    font-size: 1rem; font-weight: 700; margin-bottom: .4rem;
}
.result-card .result-text {
    color: #475569;
    color: light-dark(#475569, #cbd5e1);
    font-size: .9rem; line-height: 1.45;
}
.recommendation-card {
    display: flex; align-items: center; gap: .75rem; min-height: 86px;
    box-sizing: border-box; padding: 1rem; border-radius: 18px;
    background: #f0fdf4;
    background: light-dark(#f0fdf4, transparent);
    border: 1px solid #16a34a;
    border-color: light-dark(#16a34a, #22c55e);
    box-shadow: none;
    transition: background .2s ease, box-shadow .2s ease;
}
.recommendation-card:hover {
    background: #dcfce7;
    background: light-dark(#dcfce7, rgba(34, 197, 94, .2));
    box-shadow: 0 4px 14px rgba(22, 163, 74, .16);
    box-shadow: 0 0 16px light-dark(rgba(22, 163, 74, .18), rgba(34, 197, 94, .16));
}
.recommendation-row-gap { height: .75rem; }
.recommendation-icon { font-size: 1.45rem; line-height: 1; }
.recommendation-text {
    color: #14532d;
    color: light-dark(#14532d, #dcfce7);
    font-size: .88rem; font-weight: 700; line-height: 1.35;
}
.loading-screen {
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    min-height: 280px; padding: 2rem; text-align: center;
}
.loading-spinner {
    width: 58px; height: 58px;
    border: 5px solid rgba(2, 132, 199, .2);
    border-color: light-dark(rgba(2, 132, 199, .2), rgba(56, 189, 248, .2));
    border-top-color: #0284c7;
    border-top-color: light-dark(#0284c7, #38bdf8);
    border-right-color: #6d28d9;
    border-right-color: light-dark(#6d28d9, #8b5cf6);
    border-radius: 50%; animation: spin 0.85s linear infinite;
}
.loading-title {
    color: #0f172a;
    color: light-dark(#0f172a, #f8fafc);
    font-size: 1.15rem; font-weight: 700; margin-top: 1rem;
}
.loading-copy {
    color: #475569;
    color: light-dark(#475569, #cbd5e1);
    font-size: .85rem; margin-top: .35rem;
}
@keyframes spin { to { transform: rotate(360deg); } }
.risk-score-card {
    background: #f8fafc;
    background: linear-gradient(
        180deg,
        light-dark(#ffffff, rgba(15, 23, 42, .88)),
        light-dark(#f8fafc, rgba(30, 41, 59, .9))
    );
    border: 1px solid #cbd5e1;
    border-color: light-dark(#cbd5e1, rgba(148, 163, 184, .2));
    border-radius: 18px;
    box-sizing: border-box; height: 140px; padding: 1rem;
    box-shadow: 0 4px 12px rgba(15, 23, 42, .06);
    box-shadow: 0 8px 18px light-dark(rgba(15, 23, 42, .06), rgba(15, 23, 42, .18));
}
.risk-score-heading {
    display: flex; justify-content: space-between; gap: .75rem;
    color: #475569;
    color: light-dark(#475569, #cbd5e1);
    font-size: .82rem;
}
.risk-score-heading strong {
    color: #0f172a;
    color: light-dark(#0f172a, #f8fafc);
    font-size: 1.35rem;
}
.risk-track { height: 12px; background: linear-gradient(90deg, #22c55e 0 25%, #facc15 25% 50%, #f97316 50% 75%, #ef4444 75%); border-radius: 999px; margin: 1.1rem 0 .4rem; overflow: hidden; }
.risk-fill {
    height: 100%; background: transparent;
    border-right: 3px solid #0f172a;
    border-right-color: light-dark(#0f172a, #f8fafc);
    box-sizing: border-box;
}
.risk-scale {
    display: flex; justify-content: space-between;
    color: #475569;
    color: light-dark(#475569, #cbd5e1);
    font-size: .65rem;
}
.risk-level {
    color: #c2410c;
    color: light-dark(#c2410c, #fb923c);
    font-size: .9rem; font-weight: 700; margin-top: .75rem; text-align: center;
}
@media (max-width: 900px) {
    .app-header { flex-direction: column; align-items: flex-start; }
    .nav-links { justify-content: flex-start; }
    .app-footer-fixed { left: .5rem; right: .5rem; bottom: .5rem; }
    .footer-fixed-copy { display: none; }
}
</style>
"""
