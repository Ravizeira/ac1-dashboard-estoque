# Checklist de Teste Manual — AC3 e Parte Final

**Projeto:** Painel de Giro de Estoque  
**Objetivo:** validar manualmente a funcionalidade **AC3 (Movimentações com Histórico)** e a funcionalidade final **Reposição Inteligente**.

## 1. Pré-requisitos

- [ ] Aplicação iniciada com sucesso em `streamlit run app.py`
- [ ] Banco PostgreSQL acessível e com a estrutura criada
- [ ] Existem produtos cadastrados na tabela `produtos_estoque`
- [ ] A aba **🔄 Movimentações (AC3)** está visível
- [ ] A aba **📦 Reposição Inteligente** está visível

## 2. Dados de teste sugeridos

- Produto com estoque baixo: `Pudim de Nutella` ou `Pudim Vegano`
- Produto com estoque alto: `Pudim Tradicional`

## 3. Checklist — AC3 (Movimentações com Histórico)

### 3.1 Cadastro / seleção de produto

- [ ] Selecionar um produto existente na aba **Movimentações (AC3)**
- [ ] Confirmar que o produto aparece corretamente no selectbox

### 3.2 Entrada de estoque

- [ ] Registrar uma movimentação do tipo **ENTRADA**
- [ ] Informar uma quantidade maior que zero
- [ ] Opcionalmente preencher observação
- [ ] Confirmar o envio
- [ ] Verificar mensagem de sucesso na interface
- [ ] Atualizar o dashboard principal e confirmar aumento no estoque
- [ ] Consultar o banco e confirmar que:
  - [ ] `quantidade_estoque_atual` aumentou
  - [ ] o histórico foi salvo em `movimentacoes_estoque`

### 3.3 Saída válida de estoque

- [ ] Registrar uma movimentação do tipo **SAIDA**
- [ ] Informar uma quantidade menor ou igual ao estoque disponível
- [ ] Confirmar o envio
- [ ] Verificar mensagem de sucesso na interface
- [ ] Atualizar o dashboard principal e confirmar redução no estoque
- [ ] Consultar o banco e confirmar que:
  - [ ] `quantidade_estoque_atual` diminuiu
  - [ ] `quantidade_vendida_total` aumentou
  - [ ] o registro apareceu no histórico

### 3.4 Bloqueio de saída inválida

- [ ] Tentar registrar **SAIDA** maior que o estoque disponível
- [ ] Confirmar que o sistema bloqueia a operação
- [ ] Verificar a mensagem: **“Saída inválida: estoque insuficiente.”**
- [ ] Confirmar que nenhuma alteração foi feita no banco

### 3.5 Histórico de movimentações

- [ ] Abrir a seção **Histórico de Movimentações**
- [ ] Confirmar que as colunas estão visíveis: data/hora, produto, tipo, quantidade e observação
- [ ] Confirmar que a movimentação mais recente aparece no topo

## 4. Checklist — Parte Final (Reposição Inteligente)

### 4.1 Geração do plano

- [ ] Abrir a aba **📦 Reposição Inteligente**
- [ ] Confirmar que o resumo da funcionalidade aparece na tela
- [ ] Clicar em **Gerar Plano de Reposição**
- [ ] Verificar mensagem de sucesso ou aviso de que não há produtos para reposição

### 4.2 Validação do cálculo

- [ ] Confirmar que o sistema calcula `estoque_minimo_recomendado`
- [ ] Confirmar que o sistema calcula `estoque_meta`
- [ ] Confirmar que o sistema calcula `quantidade_sugerida`
- [ ] Confirmar que os produtos críticos recebem prioridade **ALTA**
- [ ] Confirmar que produtos com necessidade intermediária recebem prioridade **MEDIA**

### 4.3 Exibição analítica

- [ ] Verificar as métricas:
  - [ ] quantidade de produtos com sugestão
  - [ ] unidades sugeridas
  - [ ] prioridade alta
- [ ] Verificar o gráfico de sugestão de compra
- [ ] Verificar a tabela do plano salvo

### 4.4 Persistência no banco

- [ ] Consultar a tabela `reposicoes_inteligentes`
- [ ] Confirmar que os campos foram gravados corretamente:
  - [ ] `produto_id`
  - [ ] `estoque_atual`
  - [ ] `quantidade_vendida_total`
  - [ ] `estoque_minimo_recomendado`
  - [ ] `estoque_meta`
  - [ ] `quantidade_sugerida`
  - [ ] `prioridade`
  - [ ] `motivo`
  - [ ] `data_calculo`

### 4.5 Reflexo da base de dados

- [ ] Alterar estoque por AC3 e gerar novamente o plano
- [ ] Confirmar que as sugestões mudam de acordo com os novos saldos

## 5. Evidências finais para entrega

- [ ] Print da aba **AC3** com movimentação registrada
- [ ] Print do histórico de movimentações
- [ ] Print da aba **Reposição Inteligente**
- [ ] Print da tabela do plano salvo
- [ ] Print do `SELECT` no banco confirmando persistência

