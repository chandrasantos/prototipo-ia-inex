# Protótipo INEX: chatbot de oportunidades acadêmicas (RAG/LLM gemini-2.0-flash)
Esse repositório apresenta a versão 1 do protótipo criado pelos alunos Chandra dos Santos, Ennio Ennio Bernardo Pessoa dos Santos e Willian Rocha da Silva, para conclusão da disciplina PROJETO INTEGRADOR DE CIÊNCIA DOS DADOS I-T01-2025-2, do curso de graduação em Ciência dos Dados da Universidade Federal do Mato Grosso do Sul (UFMS). O objetivo da ferramenta é atuar como um assistente de IA para a startup "INEX", ajudando usuários a encontrar oportunidades acadêmicas (mestrado, doutorado, extensão, por exemplo) no Brasil. 

# Acesso
O aplicativo foi publicado em versão de teste em ambiente controlado para testes como a comunidade. 

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

# Resultados: Solução Final
A solução final desenvolvida pelo grupo foi um chatbot baseado no modelo Gemini, integrado ao Google Alertas, projetado para identificar e disponibilizar oportunidades acadêmicas de maneira automática e confiável. A escolha dessa arquitetura se deu por dois motivos principais: a necessidade de reduzir o risco de alucinações por parte do modelo de linguagem e a busca por uma solução sustentável e de baixo custo, alinhada às restrições da startup parceira Inex.

Durante o processo de implementação, a ferramenta foi configurada para monitorar alertas do Google vinculados a palavras-chave específicas relacionadas a pesquisa, bolsas, mestrado, doutorado e extensão universitária. Os resultados obtidos são filtrados e apresentados ao usuário em formato de lista, contendo título, fonte e link da oportunidade. Essa abordagem foi intencionalmente simples e objetiva, priorizando a confiabilidade das respostas em detrimento de um comportamento conversacional complexo.

O chatbot foi testado por um grupo de 15 usuários, composto majoritariamente por estudantes de graduação e pós-graduação. A média geral atribuída ao desempenho da IA foi 3,8 em uma escala de 1 a 5, enquanto a média de recomendação atingiu 4,2, demonstrando aceitação satisfatória e potencial de evolução.

Entre os principais pontos positivos identificados nos feedbacks destacam-se:
- A veracidade e atualização das oportunidades retornadas;
- A interface simples e direta, de fácil uso;
- A rapidez nas respostas e a adequação ao propósito de facilitar a busca por bolsas e programas acadêmicos.

Vários participantes elogiaram a clareza do funcionamento e a objetividade do sistema, relatando que ele “cumpre bem a proposta de buscar oportunidades acadêmicas” e é “uma boa primeira versão funcional e promissora”.

Entretanto, os feedbacks também revelaram limitações técnicas e oportunidades de melhoria:
- O sistema apresenta baixa tolerância a erros de digitação e interpretação literal das consultas (“matematica” não gera os mesmos resultados que “matemática”);
- As respostas, em alguns casos, trouxeram notícias não relacionadas diretamente a oportunidades, o que sugere necessidade de curadoria ou filtragem semântica;
- Alguns usuários sugeriram o uso de resumos automáticos das oportunidades, deduplicação de resultados e tratamento de mensagens de erro mais compreensível para o público não técnico.

Com base nessas devolutivas, foram aplicados ajustes incrementais na interface e na filtragem dos alertas. O chatbot passou a exibir mensagens mais claras quando não encontra resultados, além de adotar um conjunto mais restrito de palavras-chave e fontes, reduzindo a chance de retornos irrelevantes.

Assim, a solução final se caracteriza por ser um protótipo funcional, confiável e escalável, que prioriza a precisão informacional e abre espaço para iterações futuras, nas quais técnicas mais avançadas de NLP e classificação poderão ser incorporadas sem comprometer a estabilidade do sistema.

Foi realizada, por fim, uma nova reunião com a Inex, para entrega da solução, demonstração e passagem de conhecimento.

# Proposta da disciplina 


# Proposta da disciplina
## Ementa
Desenvolvimento de Ações de Extensão. Resolução de problemas. Levantamento de requisitos (Visita técnica). Modelagem. Banco de Dados. Desenvolvimento de aplicações Web/Desktop (Prática Profissional Supervisionada). Controle de Versão.
 
## Objetivos
### Objetivo Geral:

Oportunizar a vivência prática-profissional em modelagem, criação e organização de bases de dados, mediante à aplicação dos conhecimentos adquiridos durante o curso em problemas reais identificados.

### Objetivos Específicos:

Identificar e realizar o mapeamento de demandas e necessidades da comunidade local;

Analisar o objeto de estudo, definido por meio da identificação das demandas, propondo possíveis soluções ou novas ideias que articulem temas e conteúdos apresentados ao longo do curso;

Implementar e testar a solução proposta junto à comunidade local e redigir o relatório do projeto.

# Informação Sobre Carga Horária De Extensão (51h de projeto + 8H atividades com a comunidade)
A ação de extensão será desenvolvida articulando os conteúdos da ementa com a aplicabilidade desse conteúdo em benefício da sociedade. É o momento que o estudante irá mobilizar conhecimentos, habilidades e atitudes para planejar, executar e comprovar a execução de uma ação diretamente vinculada aos conteúdos aprendidos na disciplina.

Nesta disciplina, as atividades de extensão serão desenvolvidas seguindo as diretrizes específicas dos enunciados das atividades e avaliações elaboradas pelo professor especialista. Tais diretrizes estão disponíveis no AVA UFMS de oferta da disciplina e todo o acompanhamento no desenvolvimento das ações será realizado pelo professor tutor.
 
# Título Do Projeto De Extensão
Programa de Extensão UFMS Digital
 
# Protocolo De Submissão Da Proposta No Sigproj
95DX7.200525
 
# Nome Do Coordenador Da Ação
Daiani Damm Tonetto Riedner

