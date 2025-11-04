# Protótipo INEX: Chatbot de Oportunidades Acadêmicas (IA Generativa)
Esse repositório apresenta a versão 1 do protótipo criado na disciplina PROJETO INTEGRADOR DE CIÊNCIA DOS DADOS I-T01-2025-2, do curso de graduação em Ciência dos Dados da Universidade Federal do Mato Grosso do Sul (UFMS). O objetivo da ferramenta é atuar como um assistente de IA para a startup "INEX", ajudando usuários a encontrar oportunidades acadêmicas (mestrado, doutorado, extensão, por exemplo) no Brasil. 

# Acesso
O aplicativo está publicado em versão de teste para a comunidade e pode ser acessado aqui: https://prototipo-ia-inex.streamlit.app/

# Funcionalidades Principais

Este não é um chatbot de conversação genérico. É uma aplicação de RAG (Retrieval-Augmented Generation) com um propósito específico.

Arquitetura RAG: O chatbot não usa seu conhecimento geral para responder. Ele busca em um conjunto pré-definido de 22 feeds RSS (configurados via Google Alerts) e usa apenas essa informação como contexto para a resposta da IA.

Prompt Rígido (Anti-Alucinação): O prompt do sistema (a system_prompt no app.py) proíbe estritamente a IA de inventar informações ou usar conhecimento externo. Se a informação não estiver nos feeds, o bot informa que não encontrou.

Cache de Performance: Para garantir que o aplicativo seja rápido e não consulte 22 feeds a cada pergunta, os resultados dos feeds são cacheados por 24 horas (@st.cache_data(ttl=86400)).

Limpeza de Links do Google: A aplicação extrai automaticamente os links diretos das URLs de rastreamento do Google Alerts, fornecendo uma melhor experiência ao usuário.

# Fluxo de dados da aplicação

O usuário digita uma consulta (ex: "mestrado engenharia").

A aplicação verifica o cache (@st.cache_data). Se o cache de 24h estiver expirado, ele busca e analisa todos os 22 feeds RSS.

A função buscar_oportunidades_rss filtra as centenas de entradas de feed pelas palavras-chave do usuário.

O system_prompt é montado, injetando os resultados filtrados (o "contexto") e as regras rígidas.

O contexto e a pergunta são enviados ao modelo gemini-2.0-flash da Google.

A IA gera uma resposta baseada apenas no contexto fornecido.

O Streamlit exibe a resposta.

# Tecnologias Utilizadas

Python 3.10+

Streamlit: Para a criação da interface web (UI).

Google Gemini API (gemini-2.0-flash): Como o modelo de linguagem (LLM) para gerar as respostas.

Feedparser: Para ler e analisar os feeds RSS.

Streamlit Community Cloud: Para a publicação e hospedagem gratuita do aplicativo.

GitHub: Para controle de versão e deploy (CI/CD).

