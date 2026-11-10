# 🚨 Vazou Meus Dados

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

O **Vazou Meus Dados** é um painel web interativo e de código aberto voltado para a conscientização em segurança cibernética. Ele permite que qualquer pessoa verifique rapidamente se o seu endereço de e-mail foi exposto em incidentes públicos de vazamento de dados, oferecendo um diagnóstico claro sobre o nível de risco e planos de ação práticos.

---

## 🎯 Principais Funcionalidades

- 🔒 **Privacy-First (Adequado à LGPD):** A aplicação não possui banco de dados. Nenhum e-mail pesquisado é salvo, cacheado ou rastreado. A consulta morre na memória RAM assim que a página é fechada.
- 📊 **Threat Intelligence (Inteligência de Ameaças):** Não apenas diz *se* vazou, mas calcula um *Risk Score* (Pontuação de Risco) baseada na sensibilidade dos dados expostos.
- 🧨 **Alerta de Criptografia:** Identifica e sinaliza de forma crítica se a senha do usuário vazou em **Texto Puro** (Plaintext) ou se estava protegida por *Hash* criptográfico no momento do ataque.
- 🏷️ **Categorização de Dados:** Mapeia exatamente o que caiu na rede (senhas, e-mails, telefones, endereços físicos) usando tags visuais.
- ⚡ **Integração Real-Time:** Consome a API gratuita e open-source do [XposedOrNot](https://xposedornot.com/), garantindo varreduras em mais de 10 bilhões de registros sem limites drásticos de rate-limit.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.11
- **Interface Web:** Streamlit
- **Requisições:** Requests
- **Infraestrutura:** Docker & Docker Compose (otimizado para proxy reverso)

---

## 🚀 Como Executar o Projeto

Você pode rodar o projeto localmente no seu computador para desenvolvimento ou hospedá-lo em um servidor utilizando Docker para produção.

### Estrutura do Repositório

```text
vazou-meus-dados/
├── .gitignore
├── app.py
├── assets/
│   └── logo.png
├── docker-compose.yml
├── README.md
├── requirements.txt
└── src/
    ├── __init__.py
    ├── components.py
    ├── config.py
    ├── main.py
    ├── services.py
    ├── styles.py
    └── translator.py
```

O projeto usa uma estrutura simples por responsabilidade: `services.py` concentra
a integração com a API, `components.py` concentra os componentes da interface,
`styles.py` reúne o visual e `main.py` orquestra o fluxo da aplicação. O arquivo
`app.py` permanece apenas como ponto de entrada do Streamlit.

### Opção 1: Execução Local com Ambiente Virtual

O uso de um ambiente virtual (`venv`) garante que as dependências do projeto fiquem isoladas, sem interferir na instalação global do Python no seu sistema operacional.

1. Clone o repositório:

```bash
git clone https://github.com/SEU_USUARIO/vazou-meus-dados.git
cd vazou-meus-dados
```

2. Crie e ative o ambiente virtual:

```bash
# Criação do ambiente virtual
python -m venv venv

# Windows (PowerShell/CMD)
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

> Caso o repositório ainda não tenha o arquivo `requirements.txt`, execute: `pip install streamlit requests` e depois gere o arquivo com `pip freeze > requirements.txt`.

4. Inicie a aplicação:

```bash
streamlit run app.py
```

O navegador abrirá automaticamente em `http://localhost:8501`.

### Opção 2: Implantação via Docker

Ideal para infraestruturas utilizando Portainer ou gerenciadores de stacks. O arquivo `docker-compose.yml` já está configurado para instalar dependências do `requirements.txt` e expor a aplicação em porta 8501 para acoplamento com proxies reversos externos, como NGINX UI ou Traefik.

1. Crie o arquivo `docker-compose.yml`:

```yaml
# ==============================================================================
# Stack: Vazou Meus Dados - Plataforma de Conscientização e Segurança
# Descrição: Orquestração do contêiner da aplicação web Python (Streamlit).
#            Configurado para provisionamento ágil, persistência de código-fonte
#            via bind mount e exposição de porta para acoplamento com proxies
#            reversos externos (como NGINX UI, Traefik ou Apache).
# ==============================================================================

services:
  vazou_meus_dados:
    # ── 1. Imagem e Configuração do Contêiner ─────────────────────────────────
    
    # Utiliza a variação 'slim' do Debian com Python 3.11 pré-instalado.
    # Esta escolha reduz drasticamente o tamanho da imagem e a superfície
    # de ataque (menos pacotes desnecessários = maior segurança).
    image: python:3.11-slim
    
    # Nome fixo e identificável para facilitar a administração via CLI 
    # (ex: docker logs vazou_meus_dados_app) e painéis de gerência (Portainer).
    container_name: vazou_meus_dados_app
    
    # Define o diretório raiz de trabalho dentro do sistema de arquivos do
    # contêiner. Todas as instruções subsequentes assumirão este escopo.
    working_dir: /app
    
    # Política de tolerância a falhas: garante que o contêiner seja reiniciado
    # automaticamente em caso de crash da aplicação ou reinicialização do Host.
    restart: unless-stopped
    
    # ── 2. Instruções de Inicialização (Entrypoint) ───────────────────────────
    
    # O comando shell encadeado realiza duas ações críticas em tempo de execução:
    # 1. Lê o arquivo 'requirements.txt' do volume mapeado e instala as dependências.
    # 2. Inicializa o servidor Streamlit escutando explicitamente em '0.0.0.0'.
    # A flag '--server.address=0.0.0.0' é obrigatória no Docker para que a
    # aplicação aceite tráfego externo à interface de rede isolada do contêiner.
    command: >
      sh -c "pip install -r requirements.txt &&
      streamlit run app.py --server.port=8501 --server.address=0.0.0.0"
      
    # ── 3. Topologia de Rede e Exposição ──────────────────────────────────────
    
    ports:
      # Mapeamento [Porta_do_Host]:[Porta_do_Contêiner].
      # Expõe o serviço nativamente no Host para que balanceadores de carga ou
      # proxies reversos localizados em outras sub-redes/VMs possam rotear
      # o tráfego HTTP/WebSocket adequadamente.
      - "8501:8501"
      
    # ── 4. Gerenciamento de Volumes e Persistência ────────────────────────────
    
    volumes:
      # Estratégia de 'Bind Mount': Espelha o diretório atual do host ('./')
      # para dentro do diretório '/app' do contêiner.
      # Vantagem: Permite edição do código ('app.py') e aplicação imediata
      # no frontend sem necessidade de recriar (build) a imagem do Docker.
      - ./:/app

    # ── 5. Políticas de Retenção de Logs ──────────────────────────────────────
    
    logging:
      # Utiliza o driver JSON padrão, porém impõe limites estritos.
      driver: "json-file"
      options:
        # Previne a exaustão de espaço em disco (I/O) limitando cada arquivo
        # de log a 10 Megabytes e retendo apenas os 3 últimos arquivos rotacionados.
        max-size: "10m"
        max-file: "3"
```

2. Suba o contêiner:

```bash
docker-compose up -d
```

> **Aviso para uso com proxy reverso:** habilite suporte a WebSockets nas configurações do seu proxy (por exemplo, com os cabeçalhos `Upgrade` e `Connection: upgrade` no NGINX). O Streamlit depende de WebSockets para atualizar a interface em tempo real.

---

## 🛡️ Aviso Legal e Privacidade

Este projeto foi desenhado com foco estrito em privacidade e caráter educativo. A aplicação atua apenas como um "pass-through" visual para a API pública do XposedOrNot. O projeto não se responsabiliza pela exatidão das bases de dados de terceiros e não armazena logs de tráfego que possam identificar os usuários pesquisados.
