"""Configurações compartilhadas da aplicação."""

from pathlib import Path

API_BASE_URL = "https://api.xposedornot.com"
APP_TITLE = "Vazou Meus Dados | Verificador de Segurança"
APP_ICON = "🛡️"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOGO_PATH = PROJECT_ROOT / "assets" / "logo.png"
PUBLIC_URL = "https://vazoumeusdados.plataformatech.online"
SHARE_IMAGE_URL = "https://raw.githubusercontent.com/Blimabru/vazou-meus-dados/main/assets/logo.png"
SHARE_DESCRIPTION = (
    "Consulte se o seu e-mail apareceu em vazamentos públicos e descubra quais dados "
    "podem ter sido expostos."
)
