# Roteiro de Vídeo - Entrega AC1 (3 a 4 Minutos)

**Regra Principal:** O vídeo não deve passar de 4 minutos, deve ser dinâmico e focar no **funcionamento da aplicação**. Não explique o código deeply. Apenas 1 membro da equipe precisa gravar.

## Parte 1: Board Ágil (0:00 - 0:30)
1. Abra o seu Trello / GitHub Projects.
2. Mostre rapidamente as tarefas que foram criadas para o projeto (Ex: "Criar Banco de Dados", "Construir Dashboard de Estoque").
3. Mostre a principal funcionalidade da entrega ("Dashboard Funcionando e Conexão BD") movida para a coluna **Done / Concluído**.
   - *Fala sugerida:* "Olá professor, aqui está o nosso quadro ágil. Como pode ver, concluímos a primeira grande entrega do nosso CRUD de produtos."

## Parte 2: Apresentando o Painel de BI (0:30 - 1:15)
1. Vá até o navegador onde a aplicação está rodando (`localhost:8501`).
2. Demonstre as funcionalidades de Análise na aba principal (`Dashboard de BI`):
   - Exiba as Métricas Totais, o Gráfico Comparativo e a Tabela Completa.
   - Mostre a seção de **Alertas de Reposição (Estoque < 5)**, ressaltando a regra de negócio do projeto.

## Parte 3: Demonstração Funcional (CRUD) e Prova de Integração (1:15 - 2:45)
1. Clique na aba **"➕ Novo Produto"**.
   - Cadastre um produto de teste. Exemplo: Nome = *Produto Teste AC1*, Estoque Inicial = *2*, Vendida = *0*, Valor = *10,00*.
   - Clique em **Salvar** e mostre a mensagem de sucesso na tela Streamlit.
2. Clique na aba **"🔄 Atualizar Estoque"**.
   - Selecione um produto já existente na lista (O produto teste que você acabou de criar ou outro).
   - Indique a adição de *5* unidades no estoque e confirme. Mostre a mensagem de sucesso.
3. Volte para a aba **"📊 Dashboard de BI"** e clique no botão **🔄 Atualizar Dados**.
   - Mostre que o painel atualizou automaticamente com os novos números do banco de dados alterando os alertas.
4. Abra o seu gerenciador de banco de dados do **PostgreSQL** (PgAdmin ou DBeaver).
5. Mostre as tabelas ou faça rapidamente um `SELECT * FROM produtos_estoque ORDER BY id DESC LIMIT 5;` comprovando de que tudo o que você preencheu nas abas anteriores foi salvo não na memória, mas no banco relacional exigido.

## Parte 4: Opcional e Finalização (2:45 - 3:30)
1. (Opcional) Mostre apenas superficialmente sua estrutura de pastas no VS Code (`app.py`, uso do `.env` para segurança). Não pare para ficar lendo linhas de código!
2. Acesse a página do repositório no **GitHub** e mostre que ele está em status **Público**.
3. Agradeça e encerre a gravação.

---

### Dicas Extras:
* Grave a tela com o microfone ativado. Softwares recomendados: **Loom** (gravações de até 5min gratuitas) ou **OBS Studio**.
* Garanta que todos do grupo estão informados de subir o mesmo link (a Ficha de Entrega) no ambiente do Classroom.
