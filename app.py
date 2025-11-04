import streamlit as st
import google.generativeai as genai
from functions import get_secret, reset_chat
import feedparser
import re # Para limpar o HTML
from urllib.parse import urlparse, parse_qs # Para limpar os links do Google Alert

# --- FUNÇÕES DE BUSCA (RAG) ADICIONADAS ---
# (Estas são as funções que leem e cacheiam os feeds)

def limpar_html(texto):
    """Remove tags HTML simples de um texto."""
    if texto:
        return re.sub(r'<[^>]+>', '', texto)
    return ""

def extrair_link_real_google(google_url):
    """Extrai o link real de um feed do Google Alerts."""
    try:
        # Pega a URL de rastreamento e extrai o parâmetro 'q' (o link real)
        parsed_url = urlparse(google_url)
        real_link = parse_qs(parsed_url.query)['q'][0]
        return real_link
    except Exception:
        # Se falhar (ou se não for um link do Google), retorna o link original
        return google_url

@st.cache_data(ttl=86400) # Cacheia os feeds por 24 horas (86400 segundos)
def carregar_todos_os_feeds(lista_de_urls):
    """Busca e analisa todos os feeds de uma vez. Fica no cache."""
    # Este print aparecerá no seu terminal 1x por dia
    print(f"ATUALIZANDO CACHE DE FEEDS... (Isso acontece 1x por dia)")
    entries_totais = []
    for url in lista_de_urls:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                # Adiciona o nome da fonte da busca (Google Alert)
                entry.fonte_rss = feed.feed.title if feed.feed.title else 'Google Alert'
                entries_totais.append(entry)
        except Exception as e:
            print(f"Erro ao processar feed: {url} - {e}")
    return entries_totais

def buscar_oportunidades_rss(todas_as_entradas_cacheadas, palavras_chave):
    """
    Busca em memória (rápido!) nas entradas cacheadas pelas palavras-chave.
    """
    oportunidades_encontradas = []
    
    termos_chave = palavras_chave.lower().split()
    if not termos_chave:
        return "Nenhuma palavra-chave fornecida para a busca."

    print(f"Buscando em {len(todas_as_entradas_cacheadas)} entradas cacheadas por: {termos_chave}")

    for entry in todas_as_entradas_cacheadas:
        titulo = entry.title.lower() if entry.title else ""
        sumario = limpar_html(entry.summary.lower() if entry.summary else "")

        # Verifica se TODOS os termos-chave estão no título ou sumário
        if all(termo in (titulo + sumario) for termo in termos_chave):
            
            # Limpa o link do Google para ter o link direto
            link_real = extrair_link_real_google(entry.link)
            
            oportunidades_encontradas.append(
                f"Oportunidade: {entry.title}\n"
                f"Fonte: {entry.fonte_rss}\n"
                f"Link: {link_real}\n"
                f"Resumo: {limpar_html(entry.summary)}\n---\n"
            )
            
    if not oportunidades_encontradas:
        return "Infelizmente, não encontrei nenhuma oportunidade relevante nos feeds RSS monitorados. Você quer tentar de novo? Eu sou uma IA que monitora o conteúdo disponível na internet usando o Google Alertas. Pode ser que não tenha nenhuma oportunidade aberta com os filtros que você aplicou. Ou pode ter sido a forma como você escreveu o pedido para mim. Em vez de escrever 'extensão universitária em marketing', escreva 'extensão universitária marketing', por exemplo. Essa é a forma como eu vou consultar as informações. Digite novamente."
        
    print(f"Encontradas {len(oportunidades_encontradas)} oportunidades.")
    return "\n".join(oportunidades_encontradas)
# --- FIM DAS FUNÇÕES RSS ---


# Configuração da API e Modelo (Seu código original)
api_key = get_secret("API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash") 

# Configuração da Sidebar (Seu código original)
temperature = st.sidebar.slider(
    label="Select the temperature",
    min_value=0.0,
    max_value=2.0,
    value=1.0
)

if st.sidebar.button("Reset chat"):
    reset_chat()

# Configuração do Histórico de Chat (Seu código original)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if not st.session_state.chat_history:
    st.session_state.chat_history.append(("assistant", "Oi! Sou a IA da startup INEX e fui treinada para procurar oportunidades acadêmicas no Brasil. Não sou uma IA que vai conversar com você, por isso, atenção! Use palavras-chaves para falar comigo e receber as informações que você procura. Digite 'mestrado engenharia' ou 'extensão universitária', por exemplo, e veja o que acontece. Vamos começar?"))

for role, message in st.session_state.chat_history:
    st.chat_message(role).write(message)

# Input do Usuário (Seu código original)
user_message = st.chat_input("Escreva as palavras-chave para encontrar oportunidades acadêmicas. Dica: em vez de digitar 'mestrado em matemática', escreva 'mestrado matemática'.")

# --- LÓGICA PRINCIPAL (Original + Injeção de RAG) ---
if user_message:
    st.chat_message("user").write(user_message)
    st.session_state.chat_history.append(("user", user_message))

    # --- INÍCIO DA LÓGICA RSS ---

    # Lista de feeds RSS que você forneceu
    urls_dos_feeds = [
        "https://www.google.com.br/alerts/feeds/01818713549597334619/9698812997214701243",
        "https://www.google.com.br/alerts/feeds/01818713549597334619/8851643920037245402",
        "https://www.google.com.br/alerts/feeds/01818713549597334619/1452649767478625646",
        "https://www.google.com.br/alerts/feeds/01818713549597334619/18209722975849713093",
        "https://www.google.com.br/alerts/feeds/01818713549597334619/9997263269009676696",
        "https://www.google.com.br/alerts/feeds/01818713549597334619/14222190083815897446",
        "https://www.google.com.br/alerts/feeds/01818713549597334619/12148638501725476822",
        "https://www.google.com.br/alerts/feeds/01818713549597334619/448393206293627164",
        "https://www.google.com.br/alerts/feeds/01818713549597334619/15309007213012145968",
        "https://www.google.com.br/alerts/feeds/01818713549597334619/15210665704084798616",
        "https://www.google.com.br/alerts/feeds/01818713549597334619/2723101667317555779",
        "https://www.google.com.br/alerts/feeds/01818713549597334619/1389215342005614040",
        "https://www.google.com.br/alerts/feeds/01818713549597334619/9108155755772339439",
        "https://www.google.com.br/alerts/feeds/01818713549597334619/10992025689305529155",
        "https://www.google.com.br/alerts/feeds/01818713549597334619/1389215342005616086",
        "https://www.google.com.br/alerts/feeds/01818713549597334619/14940256395612108869",
        "https://www.google.com.br/alerts/feeds/01818713549597334619/438955880278118194",
        "https://www.google.com.br/alerts/feeds/01818713549597334619/83998224060057865",
        "https://www.google.com.br/alerts/feeds/01818713549597334619/16481529896605578269",
        "https://www.google.com.br/alerts/feeds/01818713549597334619/3675238271451375144",
        "https://www.google.com.br/alerts/feeds/01818713549597334619/15526109481784073915",
        "https://www.google.com.br/alerts/feeds/01818713549597334619/12658578375107774521"
    ]
    
    # Verifica se é uma saudação ou uma busca real
    palavras_nao_busca = ["oi", "tudo bem", "olá", "bom dia", "boa tarde", "boa noite", "obrigado", "obrigada"]
    busca_realizada = False
    for palavra in palavras_nao_busca:
        if palavra in user_message.lower():
            busca_realizada = True
            contexto_dos_feeds = "Não é uma busca. Apenas respondendo ao usuário."
            break
    
    # Se não for uma saudação, FAZ A BUSCA
    if not busca_realizada:
        with st.spinner(f"Buscando por '{user_message}' nos feeds..."):
            # Carrega os feeds (do cache, se disponível)
            # (tuple() é necessário para o cache do streamlit funcionar com listas)
            entradas_cacheadas = carregar_todos_os_feeds(tuple(urls_dos_feeds))
            # Busca nas entradas cacheadas (rápido)
            contexto_dos_feeds = buscar_oportunidades_rss(entradas_cacheadas, user_message)
    
    # INJETANDO OS DADOS DO RSS NO PROMPT RÍGIDO
    # Este é o novo prompt que força a IA a usar apenas os feeds
    system_prompt = f"""
    Você é a IA da startup INEX. A língua padrão é o Português do Brasil.
    Sua única tarefa é responder às perguntas do usuário usando **ESTRITAMENTE E APENAS** as informações fornecidas abaixo na seção "CONTEXTO DOS FEEDS RSS".

    **REGRAS ABSOLUTAS E INFLEXÍVEIS:**
    1.  **NÃO USE SEU CONHECIMENTO GERAL.** Você está **PROIBIDA** de usar qualquer informação que não esteja escrita literalmente no "CONTEXTO". Sua memória interna está bloqueada.
    2.  Se o "CONTEXTO" disser "Nenhuma oportunidade relevante encontrada...", sua única resposta deve ser informar isso ao usuário de forma gentil (ex: "Desculpe, não encontrei nenhuma oportunidade sobre '...' nos nossos feeds no momento.") e não deve sugerir mais nada.
    3.  Se o "CONTEXTO" for "Não é uma busca...", apenas responda à saudação gentilmente e pergunte o que o usuário gostaria de buscar (ex: "Olá! Sobre qual oportunidade acadêmica você gostaria de saber hoje?").
    4.  Se o usuário perguntar algo não relacionado a oportunidades acadêmicas, sua única resposta deve ser gentilmente trazer a conversa de volta ao tópico (ex: "Eu sou uma IA focada em oportunidades acadêmicas. Você gostaria de buscar por algum edital?").
    5.  Seja sempre gentil, amigável e direta ao ponto. Não invente informações.

    ---
    CONTEXTO DOS FEEDS RSS (Sua única fonte de verdade. Você não sabe de mais nada):
    {contexto_dos_feeds}
    ---
    """
    # --- FIM DA LÓGICA RSS ---

    
    # (O resto do seu código original)
    full_input = f"{system_prompt}\n\nUser message:\n\"\"\"{user_message}\"\"\""

    context = [
        *[
            {"role": role, "parts": [{"text": msg}]} for role, msg in st.session_state.chat_history
        ],
        {"role": "user", "parts": [{"text": full_input}]}
    ]

    try:
        response = model.generate_content(
            context,
            generation_config={
                "temperature": temperature,
                "max_output_tokens": 1000
            }
        )
        assistant_reply = response.text
    except Exception as e:
        assistant_reply = f"Desculpe, ocorreu um erro ao chamar a IA: {e}"

    st.chat_message("assistant").write(assistant_reply)
    st.session_state.chat_history.append(("assistant", assistant_reply))