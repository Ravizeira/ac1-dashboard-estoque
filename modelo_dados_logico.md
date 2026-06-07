# Modelo de Dados Lógico — Parte Final

```mermaid
erDiagram
    PRODUTOS_ESTOQUE {
        int id PK
        varchar nome_produto
        int quantidade_estoque_atual
        int quantidade_vendida_total
        decimal valor_unitario
        timestamp data_atualizacao
    }

    MOVIMENTACOES_ESTOQUE {
        int id PK
        int produto_id FK
        varchar tipo_movimentacao
        int quantidade
        varchar observacao
        timestamp data_movimentacao
    }

    REPOSICOES_INTELIGENTES {
        int id PK
        int produto_id FK
        int estoque_atual
        int quantidade_vendida_total
        int estoque_minimo_recomendado
        int estoque_meta
        int quantidade_sugerida
        varchar prioridade
        varchar motivo
        timestamp data_calculo
    }

    PRODUTOS_ESTOQUE ||--o{ MOVIMENTACOES_ESTOQUE : registra
    PRODUTOS_ESTOQUE ||--o{ REPOSICOES_INTELIGENTES : gera
```

## Leitura do modelo

- **PRODUTOS_ESTOQUE**: entidade principal do sistema.
- **MOVIMENTACOES_ESTOQUE**: histórico operacional das entradas e saídas.
- **REPOSICOES_INTELIGENTES**: sugestões de compra calculadas a partir do estoque e das vendas acumuladas.

