import streamlit as st
import requests
import time

# ==============================================================================
# 1. CONFIGURAÇÃO GERAL DA APLICAÇÃO
# ==============================================================================
# Define os parâmetros fundamentais da página web, como título na aba do navegador,
# ícone (favicon) e o layout de exibição centralizado.
st.set_page_config(
    page_title="VazouMeusDados | Verificador de Segurança",
    page_icon="🛡️",
    layout="centered"
)

# ==============================================================================
# 2. INTERFACE VISUAL (CABEÇALHO E FORMULÁRIO)
# ==============================================================================

# TODO: Espaço reservado para a logo da instituição ou evento
# Descomente a linha abaixo e insira o caminho da imagem quando necessário
# st.image("caminho_para_sua_logo.png", width=200)

st.title("🛡️ VazouMeusDados")
st.markdown("### Verifique a exposição do seu e-mail na internet")

# TODO: Espaço reservado para a assinatura institucional
# st.markdown("*[Insira o nome da sua Instituição / Equipe / Evento Aqui]*")

# Aviso de Privacidade - Fator crucial para conformidade com LGPD
st.info("🔒 **Sua pesquisa é privada.** Não armazenamos os e-mails consultados. Esta ferramenta utiliza a base de dados open-source do XposedOrNot de forma anônima.")
st.write("---")

# Campo de entrada de dados com sanitização básica (remoção de espaços em branco)
email_usuario = st.text_input("Digite seu e-mail para consulta:", placeholder="usuario@email.com").strip()

# ==============================================================================
# 3. SERVIÇOS DE INTEGRAÇÃO COM API EXTERNA (XposedOrNot)
# ==============================================================================

def buscar_vazamentos(email):
    """
    Realiza consulta na API do XposedOrNot para verificar se o e-mail informado
    está presente em algum banco de dados público de vazamentos.
    
    Args:
        email (str): Endereço de e-mail do usuário.
    Returns:
        list: Lista contendo os nomes dos vazamentos encontrados. 
              Retorna lista vazia se não houver vazamentos, ou None em caso de erro.
    """
    url = f"https://api.xposedornot.com/v1/check-email/{email}"
    try:
        resp = requests.get(url)
        # O status 200 indica que o e-mail foi encontrado em vazamentos
        if resp.status_code == 200:
            dados = resp.json()
            breaches = dados.get("breaches", [[]])
            # Trata o retorno para garantir que seja sempre uma lista padronizada
            return breaches[0] if isinstance(breaches, list) and len(breaches) > 0 else breaches
        # O status 404 (tratado implicitamente) significa que não há registros (e-mail seguro)
        return []
    except requests.exceptions.RequestException:
        # Captura falhas de rede, timeout ou indisponibilidade do serviço
        return None

def buscar_analytics(email):
    """
    Realiza consulta no endpoint de analytics para obter detalhes aprofundados
    sobre a exposição, incluindo Risk Score e metadados sobre as senhas expostas.
    
    Args:
        email (str): Endereço de e-mail do usuário.
    Returns:
        dict: Dicionário completo com as análises do vazamento. Retorna None em caso de erro.
    """
    url = f"https://api.xposedornot.com/v1/breach-analytics/{email}"
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            return resp.json()
        return None
    except requests.exceptions.RequestException:
        return None

# ==============================================================================
# 4. PROCESSAMENTO E LÓGICA DE EXIBIÇÃO DOS RESULTADOS
# ==============================================================================

# O bloco principal é executado apenas quando o botão de submissão é acionado
if st.button("Verificar Risco", type="primary"):
    
    # Validação simples para garantir que a string possui o formato mínimo de um e-mail
    if email_usuario and "@" in email_usuario:
        
        # Componente visual para indicar processamento em andamento
        with st.spinner("Analisando registros de segurança, origens e criptografia..."):
            time.sleep(1) # Pausa intencional para melhorar a experiência do usuário (UX)
            
            # Chamada principal à API
            vazamentos = buscar_vazamentos(email_usuario)
            
            st.write("---")
            
            # ── Tratamento de Respostas ───────────────────────────────────────
            
            # Cenário 1: Falha na comunicação
            if vazamentos is None:
                st.error("⚠️ Erro de comunicação com os servidores. Verifique a conexão com a internet e tente novamente.")
            
            # Cenário 2: E-mail não encontrado em vazamentos (Seguro)
            elif len(vazamentos) == 0:
                st.success("### 🟢 Risco Baixo: Seu e-mail está seguro!")
                st.markdown("Não encontramos este endereço de e-mail em grandes vazamentos de dados públicos catalogados.")
                st.info("""
                **Como manter esse nível de segurança:**
                * **Use 2FA (Verificação em Duas Etapas):** Mantenha ativado em serviços críticos.
                * **Senhas Únicas:** Não reutilize a mesma senha para múltiplas plataformas.
                """)
                
            # Cenário 3: E-mail exposto (Análise de Risco Necessária)
            else:
                # Realiza a segunda requisição para obter os detalhes ricos do ataque
                analytics = buscar_analytics(email_usuario)
                
                # Extração segura da pontuação e nível de risco (Fallback para "Alto" e "Crítico" se falhar)
                score = analytics.get("Risk", {}).get("risk_score", "Alto") if analytics else "Alto"
                label = analytics.get("Risk", {}).get("risk_label", "Crítico") if analytics else "Crítico"
                
                st.error(f"### 🔴 Risco {label} (Pontuação: {score}/100)")
                st.markdown(f"Seu e-mail foi exposto em **{len(vazamentos)}** incidente(s) de segurança cibernética.")
                
                st.write("### 🔍 Detalhamento das Violações")
                
                # Extrai a matriz de detalhes dos incidentes
                detalhes_vazamentos = analytics.get("BreachesDetails", []) if analytics else []
                
                # ── Renderização dos Cards de Incidentes ──────────────────────
                if detalhes_vazamentos:
                    for detalhe in detalhes_vazamentos:
                        # Extração de variáveis do dicionário
                        nome_site = detalhe.get("breach", "Site Desconhecido")
                        descricao = detalhe.get("details", "Sem detalhes adicionais sobre este incidente.")
                        dados_vazados = detalhe.get("xposed_data", "Não especificado")
                        risco_senha = str(detalhe.get("password_risk", "")).lower()
                        industria = detalhe.get("industry", "Não informado")
                        domain = detalhe.get("domain", "")
                        
                        # Criação do componente colapsável (expander) para cada incidente
                        with st.expander(f"🚨 Incidente: {nome_site} ({industria})", expanded=False):
                            
                            # Divisão do layout em duas colunas para metadados e status da senha
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown(f"**Setor:** {industria}")
                                if domain:
                                    st.markdown(f"**Domínio Afetado:** {domain}")
                                    
                            with col2:
                                # Lógica de severidade baseada no método de armazenamento da senha roubada
                                if "password" in dados_vazados.lower():
                                    if "plaintext" in risco_senha or "plain" in risco_senha:
                                        st.error("🧨 **Senha em TEXTO PURO (Nível Máximo)**")
                                    elif "hash" in risco_senha or "encrypted" in risco_senha:
                                        st.warning("🔒 **Senha Criptografada exposta**")
                                    else:
                                        st.warning("⚠️ **Senha Exposta**")
                                else:
                                    st.success("✅ **Senhas Seguras neste ataque**")
                            
                            st.write("---")
                            st.write("**Contexto do Incidente:**")
                            st.caption(descricao) 
                            
                            st.write("**Dados Específicos Expostos:**")
                            
                            # Tratamento de string: Converte lista separada por vírgula/ponto e vírgula em badges visuais
                            tags_dados = "".join([f"`{dado.strip()}` " for dado in dados_vazados.split(";") if dado.strip()])
                            st.markdown(tags_dados)

                # Fallback: Exibição simples caso o endpoint de analytics não retorne detalhes
                else:
                    st.write(f"**Fontes do vazamento:** {', '.join(vazamentos)}")
                    st.warning("⚠️ **Verifique as senhas utilizadas nestes serviços e faça a troca imediata.**")
                
                # ── Plano de Mitigação ─────────────────────────────────────────
                st.markdown("---")
                st.markdown("### 📋 Plano de Ação Recomendado:")
                st.info("""
                **1. Alteração Imediata:** Modifique a senha, priorizando os serviços que vazaram credenciais em TEXTO PURO. 
                **2. Engenharia Social:** Com o vazamento de dados demográficos, aumente a cautela contra abordagens telefônicas ou mensagens se passando por instituições legítimas.
                **3. Autenticação Multifator (2FA):** Ative mecanismos de dupla verificação. Eles neutralizam a utilidade de uma senha comprometida para o atacante.
                """)
    else:
        # Tratamento para input em branco ou mal formatado
        st.warning("Por favor, forneça um endereço de e-mail válido contendo '@' para prosseguir.")