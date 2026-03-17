# Roteiro de Vídeo - Entrega AC1 (3 a 4 Minutos)

**Regra Principal:** O vídeo não deve passar de 4 minutos, deve ser dinâmico e focar no **funcionamento da aplicação**. Não explique o código deeply. Apenas 1 membro da equipe precisa gravar.

## Parte 1: Board Ágil (0:00 - 0:30)
1. Abra o seu Trello / GitHub Projects.
2. Mostre rapidamente as tarefas que foram criadas para o projeto (Ex: "Criar Banco de Dados", "Construir Dashboard de Estoque").
3. Mostre a principal funcionalidade da entrega ("Dashboard Funcionando e Conexão BD") movida para a coluna **Done / Concluído**.
   - *Fala sugerida:* "Olá professor, aqui está o nosso quadro ágil. Como pode ver, concluímos a primeira grande entrega do nosso CRUD de produtos."

## Parte 2: O Sistema Rodando (0:30 - 2:00)
1. Vá até o navegador onde a aplicação está rodando (`localhost:8501`).
2. Demonstre as funcionalidades principais rapidamente:
   - Exiba os gráficos e dados na tela principal (Análises). 
   - Cadastre um NOVO produto no painel de controle (ex: Nome = 'Produto Teste AC1', Quantidade = 50, Preço = 19.99).
   - Clique no botão de Salvar/Cadastrar.
   - Mostre a mensagem de sucesso na tela.

## Parte 3: Verificando o Banco de Dados (2:00 - 2:45)
1. Abra o seu SGBD (PgAdmin ou DBeaver).
2. Mostre o banco de dados rodando em PostgreSQL (uma exigência da AC1 é não usar SQLite/base local).
3. Execute o comando `SELECT * FROM produtos_estoque ORDER BY id DESC LIMIT 5;`
4. Mostre que o produto cadastrado na "Parte 2" ('Produto Teste AC1') realmente gravou e apareceu lá.
   - *Fala sugerida:* "Aqui está a prova da gravação no banco de dados PostgreSQL. O registro foi persistido perfeitamente no backend."

## Parte 4: Opcional e Finalização (2:45 - 3:30)
1. (Opcional) Mostre apenas superficialmente sua estrutura de pastas no VS Code (`app.py`, uso do `.env` para segurança). Não pare para ficar lendo linhas de código!
2. Acesse a página do repositório no **GitHub** e mostre que ele está em status **Público**.
3. Agradeça e encerre a gravação.

---

### Dicas Extras:
* Grave a tela com o microfone ativado. Softwares recomendados: **Loom** (gravações de até 5min gratuitas) ou **OBS Studio**.
* Garanta que todos do grupo estão informados de subir o mesmo link (a Ficha de Entrega) no ambiente do Classroom.
