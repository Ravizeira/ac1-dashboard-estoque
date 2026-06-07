# Roteiro de Vídeo - Entrega AC3 (3 a 4 Minutos)

**Regra Principal:** foco em **software funcionando** e integração das 3 camadas (Streamlit + regra de negócio + PostgreSQL). Não fazer explicação longa de código.

## Parte 1: Board Ágil (0:00 - 0:30)
1. Abra o GitHub Projects/Trello do grupo.
   - *Fala:* "Professor, este é nosso board ágil com backlog, em andamento e concluído."
2. Mostre o card da funcionalidade nova da AC3 em **Done/Concluído**.
   - *Fala:* "Nesta entrega AC3, concluímos o módulo de movimentações com histórico."

## Parte 2: Contexto rápido da funcionalidade (0:30 - 0:50)
1. Abra o app em `localhost:8501`.
2. Mostre a aba **🔄 Movimentações (AC3)**.
   - *Fala:* "Aqui registramos entrada e saída de estoque com persistência e trilha de auditoria."

## Parte 3: Demonstração funcional AC3 (0:50 - 2:40)
1. Na aba **Movimentações (AC3)**, selecione um produto.
2. Faça uma movimentação de **ENTRADA** (ex.: +5) com observação.
   - *Fala:* "Registro uma entrada para aumentar o saldo atual."
3. Faça uma movimentação de **SAÍDA** válida (ex.: -2) com observação.
   - *Fala:* "Agora registro uma saída; além de reduzir estoque, a venda acumulada também é atualizada."
4. Tente uma **SAÍDA inválida** (maior que o estoque) para mostrar a regra de negócio.
   - *Fala:* "O sistema bloqueia saída com estoque insuficiente, evitando inconsistência."
5. Mostre o **Histórico de Movimentações** exibido na própria aba.
   - *Fala:* "Cada operação fica registrada com data/hora, produto, tipo e quantidade."

## Parte 4: Reflexo no BI e prova no banco (2:40 - 3:30)
1. Vá para **📊 Dashboard de BI** e clique em **🔄 Atualizar Dados**.
   - *Fala:* "Com a atualização, os indicadores de estoque e giro já refletem as movimentações."
2. Abra o PostgreSQL (PgAdmin/DBeaver) e rode:
   - `SELECT * FROM produtos_estoque ORDER BY id;`
   - `SELECT * FROM movimentacoes_estoque ORDER BY data_movimentacao DESC LIMIT 10;`
   - *Fala:* "Aqui está a prova de persistência real no banco relacional, não em memória."

## Parte 5: Encerramento (3:30 - 4:00)
1. Mostre rapidamente o repositório público no GitHub.
   - *Fala:* "O código está público com a evolução da AC3."
2. Finalize.
   - *Fala:* "Encerramos a AC3 com funcionalidade nova e completa nas 3 camadas. Obrigado!"

---

### Checklist antes de gravar
* Áudio ligado e vídeo entre 3 e 4 minutos.
* Começar pelo Board.
* Demonstrar entrada, saída, validação de erro e histórico.
* Mostrar `SELECT` no banco.
* Garantir link do vídeo pronto para a ficha de entrega.
