Plano Diretor de Projeto: Painel de Giro de Estoque e Business Intelligence

1. Visão Geral e Fundamentação Estratégica

Este projeto é arquitetado como uma iniciativa estratégica de Business Intelligence (BI) e desenvolvimento de software full-stack, projetada para transcender a simples visualização de dados. O objetivo central é a construção de uma solução robusta que converte dados brutos em inteligência acionável, garantindo que a tomada de decisão gerencial seja fundamentada em registros reais, persistentes e auditáveis. Em conformidade com o Manifesto Ágil, estabelecemos que o software em funcionamento é a única medida real de progresso, priorizando a entrega de valor contínuo sobre documentações exaustivas.

Para fins acadêmicos e de demonstração, a utilização de dados fictícios não sigilosos é uma manobra estratégica: permite a validação completa do fluxo de BI e das camadas do sistema sem os entraves de conformidade de dados sensíveis, focando estritamente na integridade dos cálculos e na funcionalidade técnica.

Camada "So What?": A integração vertical entre as três camadas (Front-end, Back-end e Banco de Dados) é o que diferencia este projeto de protótipos superficiais. Ao rejeitar o armazenamento em memória, garantimos a persistência e a integridade referencial, elementos indispensáveis para qualquer sistema de BI que pretenda oferecer históricos confiáveis e escalabilidade. Esta estrutura não apenas atende aos requisitos técnicos, mas cumpre as exigências de auditabilidade do Ministério da Educação (MEC), provando que o aluno domina o ciclo completo de construção de software.


--------------------------------------------------------------------------------


2. Arquitetura do Sistema e Stack Tecnológica

A seleção desta stack tecnológica não é arbitrária; ela impacta diretamente a agilidade do ciclo de desenvolvimento (Time-to-Market) e a reatividade da interface analítica. A arquitetura de três camadas deve ser rigorosamente respeitada para garantir a separação de responsabilidades.

Camada	Tecnologia	Justificativa Técnica e Diretrizes
Front-end & Back-end	Python 3 + Streamlit	Framework de alta produtividade que permite a criação de interfaces reativas e dashboards dinâmicos sem a complexidade do JS tradicional.
Integração / ORM	SQLAlchemy + Pandas	O SQLAlchemy abstrai a complexidade do SQL, enquanto o Pandas realiza o processamento analítico pesado com alta performance.
Banco de Dados	PostgreSQL	Mandatário. É terminantemente proibido o uso de bancos em memória ou em arquivos (SQLite, H2). Exigimos um SGBD relacional de produção para garantir a durabilidade.

Camada "So What?": O uso do SQLAlchemy como ponte entre o PostgreSQL e o Streamlit elimina gargalos de tradução de dados, reduzindo o tempo de entrega de valor ao usuário. Para o negócio, isso significa um dashboard que reflete transações em tempo real, permitindo que o gestor de estoque visualize o impacto de uma venda no giro de mercadorias no instante em que ela ocorre, sem latência de processamento de lote.


--------------------------------------------------------------------------------


3. Detalhamento da Sprint Atual (AC1)

Nesta fase inicial, o foco está na entrega de um MVP (Minimum Viable Product) que resolva a dor latente do cliente: a visibilidade do estoque. Evitamos "funcionalidades incipientes" — como sistemas de login isolados que não protegem dado algum — para priorizar recursos que impactam o resultado financeiro.

As funcionalidades entregues na AC1 são:

1. Dashboard de BI: Cálculo automatizado do Giro de Estoque (Total Vendido / Estoque Atual) com visualização gráfica reativa de Vendas vs. Saldo.
2. Alerta Inteligente: Filtro dinâmico para produtos com estoque crítico (abaixo de 5 unidades), permitindo ação imediata de ressuprimento.
3. Gestão de Itens: Interface funcional para cadastro de novos produtos e simulação de movimentações que atualizam o banco de dados e os gráficos de BI instantaneamente.

Camada "So What?": A decisão de priorizar o BI e a gestão de estoque sobre o sistema de login aplica o Princípio de Pareto: 80% do valor de negócio para o gestor vem da análise do giro de estoque, não da tela de entrada. Postergar o login garante que o esforço de engenharia seja aplicado onde o retorno sobre o investimento de tempo é máximo nesta iteração.


--------------------------------------------------------------------------------


4. Arquitetura de Dados (Modelo Relacional)

A persistência de dados no PostgreSQL é a âncora de confiabilidade do sistema. A estrutura da tabela produtos_estoque foi projetada para evitar inconsistências e garantir a precisão aritmética necessária para BI.

Coluna	Tipo	Descrição	Restrição
id	SERIAL	Identificador único e incremental	Chave Primária (PK)
nome_produto	VARCHAR(255)	Descrição textual do item	Not Null
quantidade_estoque_atual	INT	Saldo disponível em armazém	Default: 0
quantidade_vendida_total	INT	Acumulado histórico de vendas	Default: 0
valor_unitario	NUMERIC(10,2)	Preço de venda unitário	Precisão Decimal

Camada "So What?": O uso do tipo SERIAL para o ID garante a integridade dos registros durante inserções concorrentes. A definição de valores default (zero) e a precisão de NUMERIC(10,2) para valores monetários previnem os erros de arredondamento e campos nulos (null) que frequentemente corrompem métricas financeiras em larga escala, garantindo que o Giro de Estoque seja sempre um cálculo válido.


--------------------------------------------------------------------------------


5. Roadmap de Entregas e Evolução do Projeto

O desenvolvimento segue um modelo de fatiamento vertical: cada entrega deve ser uma funcionalidade nova e completa (Front-Back-DB).

1. AC1 (Atual): BI dinâmico e gestão básica de estoque.
2. AC2: Implementação de uma funcionalidade inédita (ex: nova perspectiva analítica ou módulo de relatórios).
3. AC3: Expansão do sistema com a terceira funcionalidade funcional completa.
4. Prova Final (7 de Junho): Entrega da 4ª funcionalidade nova + Diagramas UML (Classe e Casos de Uso) explicados em vídeo.

Nota Crítica: É proibido utilizar resumos de entregas anteriores (AC1, AC2, AC3) como conteúdo da Prova Final. A prova exige uma funcionalidade inédita. O sistema será encerrado definitivamente em 14 de Junho.

Camada "So What?": Este modelo evolutivo demonstra a maturidade do projeto para os auditores. Cada AC não é apenas um "pedaço" do código, mas um incremento funcional que poderia ser colocado em produção individualmente, mitigando o risco de falha sistêmica no final do projeto.


--------------------------------------------------------------------------------


6. Protocolo de Entrega e Critérios de Qualidade

Para garantir a auditabilidade e o sucesso da avaliação, os protocolos abaixo são rígidos. O descumprimento de qualquer item pode resultar em nota zero.

Regras de Submissão:

* Individuais e Obrigatórias: Mesmo em grupos (máximo de 7 alunos), cada integrante deve realizar a submissão individual no Classroom para garantir seu registro de nota.
* Proibição de Formatos Compactados: É estritamente proibido o envio de arquivos .ZIP ou .RAR. A entrega deve ser um PDF contendo apenas links clicáveis.
* Auditabilidade do Board: O vídeo demonstrativo deve começar obrigatoriamente pelo Board de Tarefas, indicando qual funcionalidade será apresentada.

Checklist de Qualidade:

* [ ] Link do GitHub: Repositório público (links que retornarem erro 404 serão zerados).
* [ ] Link do Board: Planejamento ágil atualizado (Trello ou similar).
* [ ] Vídeo (2-3 min): Obrigatório conter áudio com explicação. Vídeos sem som ou que iniciem direto no código sem passar pelo Board serão penalizados.
* [ ] PDF de Entrega: Documento centralizador com todos os links.

Camada "So What?": O rigor com o vídeo e o Board visa comprovar a autoria e a compreensão do processo ágil. O vídeo com áudio é a "prova real" de que o desenvolvedor entende a arquitetura que construiu, protegendo a integridade acadêmica do projeto contra plágios e garantindo o padrão de excelência exigido em auditorias externas.
