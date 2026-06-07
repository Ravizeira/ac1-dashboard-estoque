FICHA DE ENTREGA - AVALIAÇÃO CONTINUADA 3 (AC3)
Integrante do Grupo
Nome : Luis Gustavo Palazzi Goulart
Funcionalidade Entregue nesta AC3:
Implementação de uma nova funcionalidade completa nas 3 camadas (front-end, back-end e banco de dados):
Movimentações de Estoque com Histórico (AC3):
● Nova aba no dashboard: "🔄 Movimentações (AC3)".
● Registro de movimentações de ENTRADA e SAÍDA diretamente pela interface Streamlit.
● Regra de negócio para bloquear saídas com estoque insuficiente.
● Atualização automática no PostgreSQL:
- ENTRADA: incrementa quantidade_estoque_atual.
- SAÍDA: decrementa quantidade_estoque_atual e incrementa quantidade_vendida_total.
● Histórico de movimentações com data/hora, produto, tipo, quantidade e observação.
Conteúdo Analítico da Funcionalidade:
● Rastreabilidade completa das operações de estoque (trilha de auditoria).
● Reflexo direto no Dashboard de BI após atualização dos dados.
● Consistência dos indicadores de giro de estoque com base nas movimentações persistidas.
Origem dos Dados:
O projeto segue foco em BI e Análise de Dados. Os dados não são sigilosos; são dados
fictícios inseridos e persistidos no banco relacional PostgreSQL pela própria aplicação,
comprovando integração real entre interface, lógica de negócio e base de dados.
Links Obrigatórios
● Link do Board (Quadro Ágil): https://github.com/users/Ravizeira/projects/1/views/2
● Link do GitHub: https://github.com/Ravizeira/ac1-dashboard-estoque
● Link do Vídeo: [INSERIR LINK DO VÍDEO AC3]
