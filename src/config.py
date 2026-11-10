"""Configurações compartilhadas da aplicação.

Centralizar caminhos, URLs e textos de configuração evita valores duplicados
nos componentes e reduz o risco de divergência entre ambientes local e Docker.
"""

from pathlib import Path

# Endpoint público usado para consultar os dados de vazamentos.
API_BASE_URL = "https://api.xposedornot.com"
# Metadados principais exibidos pelo Streamlit no navegador.
APP_TITLE = "Vazou Meus Dados | Verificador de Segurança"
APP_ICON = "🛡️"
# Resolve o diretório do projeto independentemente do diretório de execução.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
# Caminhos absolutos evitam falhas quando o processo é iniciado fora da raiz.
LOGO_PATH = PROJECT_ROOT / "assets" / "logo.png"
METRICS_DB_PATH = PROJECT_ROOT / "data" / "metrics.sqlite3"
# Metadados usados em links públicos e cartões de compartilhamento.
PUBLIC_URL = "https://vazoumeusdados.plataformatech.online"
SHARE_IMAGE_URL = "https://raw.githubusercontent.com/Blimabru/vazou-meus-dados/main/assets/logo.png"
SHARE_DESCRIPTION = (
    "Consulte se o seu e-mail apareceu em vazamentos públicos e descubra quais dados "
    "podem ter sido expostos."
)
