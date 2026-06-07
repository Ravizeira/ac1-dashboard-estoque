# Copilot Instructions — ac1-dashboard-estoque

## Contexto do projeto
- Projeto acadêmico de **Construção de Software** com foco em **BI de giro de estoque**.
- Entregas evolutivas já implementadas: **AC1 (dashboard + alertas + cadastro)**, **AC2 (relatórios PDF)** e **AC3 (movimentações com histórico)**.
- Cada nova funcionalidade deve ser um fatiamento vertical completo: **UI + regra de negócio + persistência em banco**.

## Stack e arquitetura obrigatórias
- **Python 3 + Streamlit** para interface e fluxo da aplicação.
- **SQLAlchemy + Pandas** para acesso/processamento de dados.
- **PostgreSQL** como banco relacional principal.
- **Não usar SQLite/H2 para versão web**.

## Princípios de implementação
1. Priorize **software funcionando** acima de documentação extensa.
2. Não entregar tarefas isoladas de apenas uma camada (somente tela, somente tabela, somente endpoint).
3. Em funcionalidades de BI, incluir sempre:
   - nova análise/insight com dados;
   - nova visualização relevante no dashboard ou relatório.
4. Priorizar funcionalidades de negócio (estoque, movimentação, indicadores, relatórios) antes de itens periféricos.
5. Manter compatibilidade com as tabelas existentes:
   - `produtos_estoque`
   - `movimentacoes_estoque`

## Padrões de código neste repositório
- Manter textos da interface em **Português (pt-BR)**.
- Reutilizar funções de backend existentes em `app.py` quando possível:
  - `load_data`, `add_product`, `register_movement`, `load_movements`, `generate_pdf_report`.
- Em SQL, usar consultas parametrizadas com `sqlalchemy.text(...)`.
- Em movimentação de estoque:
  - validar tipo (`ENTRADA`/`SAIDA`);
  - bloquear saída com estoque insuficiente;
  - persistir histórico de movimentações.
- Não adicionar instalação dinâmica de dependências em runtime.

## Documentação e entregáveis
- Se houver nova funcionalidade, atualizar o `README.md` na seção da entrega correspondente.
- Quando solicitado, manter consistência com os artefatos de apresentação:
  - roteiros de vídeo (`roteiro_video*.md`);
  - fichas de entrega (`FICHA DE ENTREGA - ...`).

## Execução local esperada
- Instalação: `pip install -r requirements.txt`
- Setup do banco: `python setup_db.py` (com variáveis de ambiente de banco configuradas)
- Execução da app: `streamlit run app.py`

## Segurança e qualidade
- Não commitar senhas, tokens ou credenciais reais.
- Preferir mudanças pequenas, claras e diretamente relacionadas à funcionalidade solicitada.