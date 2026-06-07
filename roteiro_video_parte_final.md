# Roteiro de Vídeo — Parte Final

**Regra principal:** vídeo com cerca de **5 minutos**, focado na demonstração da entrega final.  
**Ordem rígida:** **Board → Funcionalidade nova → Diagrama de Casos de Uso → Modelo de Dados Lógico**.  
**Importante:** não começar explicando o código-fonte.

## 1. O Board

1. Abra o board do projeto.
   - Fala: "Aqui está o nosso board com as etapas do projeto e a evolução das entregas."
2. Mostre rapidamente o que foi planejado e o que já estava concluído.
   - Fala: "A organização foi feita por etapas, separando o que estava em andamento e o que já havia sido entregue nas fases anteriores."
3. Destaque a tarefa da parte final.
   - Fala: "Na parte final, adicionamos uma nova funcionalidade completa conectada ao banco de dados e ao dashboard."

## 2. A Funcionalidade Nova

1. Abra a aplicação no Streamlit.
   - Fala: "Agora vou demonstrar a funcionalidade nova em funcionamento."
2. Acesse a aba **Reposição Inteligente**.
   - Fala: "Essa aba calcula sugestões de compra para os produtos com base no estoque atual e nas vendas acumuladas."
3. Clique em **Gerar Plano de Reposição**.
   - Fala: "Ao gerar o plano, o sistema calcula estoque mínimo recomendado, meta de estoque e quantidade sugerida."
4. Mostre as métricas, o gráfico e a tabela.
   - Fala: "Aqui eu consigo ver os produtos que precisam de reposição, a prioridade de compra e o volume recomendado."
5. Explique a persistência.
   - Fala: "Essas sugestões não ficam só na tela: elas também são salvas no banco, garantindo consistência entre a interface e os dados."

## 3. Diagrama de Casos de Uso

1. Abra o diagrama de casos de uso.
   - Fala: "Este diagrama mostra as interações principais do usuário com o sistema."
2. Conecte o diagrama ao board.
   - Fala: "Cada caso de uso corresponde a uma atividade planejada no board, então o diagrama ajuda a visualizar o que foi entregue."
3. Destaque rapidamente a nova funcionalidade.
   - Fala: "A reposição inteligente aparece como um caso de uso novo dentro do fluxo do sistema."

## 4. Modelo de Dados Lógico

1. Abra o modelo de dados lógico.
   - Fala: "Como o projeto é de BI, aqui eu mostro o modelo de dados lógico em vez de um diagrama de classes."
2. Comece pela entidade principal.
   - Fala: "A entidade principal é `produtos_estoque`, que concentra os dados base do estoque."
3. Explique os relacionamentos.
   - Fala: "A tabela de movimentações registra o histórico operacional, e a tabela de reposição guarda as sugestões calculadas."
4. Feche com a importância técnica.
   - Fala: "Esse modelo mostra como o sistema mantém rastreabilidade, análise e persistência em banco."

