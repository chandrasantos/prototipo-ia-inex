# Protótipo INEX: chatbot de oportunidades acadêmicas (RAG/LLM gemini-2.0-flash)
Esse repositório apresenta a versão 1 do protótipo criado pelos alunos Chandra dos Santos, Ennio Ennio Bernardo Pessoa dos Santos e Willian Rocha da Silva, para conclusão da disciplina PROJETO INTEGRADOR DE CIÊNCIA DOS DADOS I-T01-2025-2, do curso de graduação em Ciência dos Dados da Universidade Federal do Mato Grosso do Sul (UFMS). O objetivo da ferramenta é atuar como um assistente de IA para a startup "INEX", ajudando usuários a encontrar oportunidades acadêmicas (mestrado, doutorado, extensão, por exemplo) no Brasil. 

# Acesso
O aplicativo está publicado em versão de teste para a comunidade e pode ser acessado aqui: [solicite o link]

# Formulário de avaliação
[solicite o link]

# Funcionalidades Principais

Este não é um chatbot de conversação genérico. É uma aplicação de RAG (Retrieval-Augmented Generation) com um propósito específico.

Arquitetura RAG: o chatbot não usa seu conhecimento geral para responder. Ele busca em um conjunto pré-definido de 22 feeds RSS (configurados via Google Alerts) e usa apenas essa informação como contexto para a resposta da IA.

Prompt Rígido (Anti-Alucinação): oprompt do sistema (a system_prompt no app.py) proíbe estritamente a IA de inventar informações ou usar conhecimento externo. Se a informação não estiver nos feeds, o bot informa que não encontrou.

Cache de Performance: para garantir que o aplicativo seja rápido e não consulte 22 feeds a cada pergunta, os resultados dos feeds são cacheados por 24 horas (@st.cache_data(ttl=86400)).

Limpeza de Links do Google: a aplicação extrai automaticamente os links diretos das URLs de rastreamento do Google Alerts, fornecendo uma melhor experiência ao usuário.

# Fluxo de dados da aplicação

O usuário digita uma consulta (ex: "mestrado engenharia").

A aplicação verifica o cache (@st.cache_data). Se o cache de 24h estiver expirado, ele busca e analisa todos os 22 feeds RSS.

A função buscar_oportunidades_rss filtra as centenas de entradas de feed pelas palavras-chave do usuário.

O system_prompt é montado, injetando os resultados filtrados (o "contexto") e as regras rígidas.

O contexto e a pergunta são enviados ao modelo gemini-2.0-flash da Google.

A IA gera uma resposta baseada apenas no contexto fornecido.

O Streamlit exibe a resposta.


# Tecnologias Utilizadas

Python 3.10+: como linguagem de programação.

Streamlit: para a criação da interface web (UI).

Google Gemini API (gemini-2.0-flash): como o modelo de linguagem (LLM) para gerar as respostas.

Feedparser: para ler e analisar os feeds RSS.

Streamlit Community Cloud: para a publicação e hospedagem gratuita do aplicativo.

# Contexto e Evolução do Projeto

## Ideia inicial

Este protótipo nasceu para resolver um desafio central identificado pela startup INEX: a dificuldade que estudantes e pesquisadores enfrentam para encontrar oportunidades acadêmicas (bolsas, cursos, editais), que são vastas, mas muito descentralizadas.

O briefing inicial do projeto explorou diversas abordagens, como a integração direta com o WhatsApp, o uso de web scraping focado no LinkedIn, um recorte geográfico para o Rio de Janeiro e a implementação de plataformas de NLP como Rasa/Dialogflow. 

No entanto, para atender às restrições críticas de baixo custo, manutenção zero e rapidez na publicação (requisitos fundamentais da startup, o projeto final evoluiu para uma arquitetura mais moderna e robusta: a solução entregue é um aplicativo Streamlit que implementa um padrão RAG (Retrieval-Augmented Generation) puro. 

Em vez de web scraping (que é instável) ou plataformas complexas (como Rasa), o protótipo final utiliza um LLM (Google Gemini) "trancado" para ler apenas de um conjunto de fontes de dados em tempo real (22 Feeds RSS). Esta abordagem garante que as respostas sejam sempre atuais, baseadas em fontes concretas e livres de "alucinações", ao mesmo tempo que permite a publicação gratuita via Streamlit Cloud. 
