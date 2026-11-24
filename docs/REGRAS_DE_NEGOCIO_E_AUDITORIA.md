# Regras de Negócio e Auditoria de Qualidade (QA)

Este documento reúne as premissas de negócio, a lógica dos cálculos financeiros e os critérios de verificação aplicados ao modelo BMG Canvas e ao simulador em Python.

## 1. Premissas do Modelo de Negócio (BMG Canvas)
- **Proposta de Valor:** Oferta de pizzas artesanais com padrão consistente de qualidade, atendimento ágil e precificação transparente.
- **Segmentos de Clientes:** Consumidores locais (retirada e entrega), famílias e clientes recorrentes em busca de conveniência e confiabilidade.
- **Canais:** Pedidos diretos, canais digitais/aplicativos e atendimento presencial ou de retirada.
- **Estrutura de Custos:** Dividida em custos fixos mensais (aluguel, folha e encargos, utilidades, serviços) e custos variáveis por unidade (insumos, embalagens e taxas operacionais ligadas ao volume).
- **Fontes de Receita:** Venda unitária de pizzas e itens complementares, avaliada por ticket médio e volume mensal de vendas.

## 2. Regras de Cálculo Financeiro
- **Margem de Contribuição Unitária:** `Preço Médio Unitário - Custo Variável Unitário`. Representa quanto cada unidade vendida ajuda a cobrir os custos fixos.
- **Margem de Contribuição (%):** `Margem de Contribuição Unitária / Preço Médio Unitário` (quando o preço médio é maior que zero).
- **Ponto de Equilíbrio em Unidades:** `Custos Fixos Mensais / Margem de Contribuição Unitária` (exige margem de contribuição unitária positiva).
- **Ponto de Equilíbrio em Receita:** `Ponto de Equilíbrio em Unidades * Preço Médio Unitário`.
- **Resultado Operacional Mensal:** `(Unidades/Mês * Preço Médio Unitário) - (Custos Fixos Mensais + Unidades/Mês * Custo Variável Unitário)`.
- **Payback Estimado (Meses):** `Investimento Inicial / Lucro Líquido Estimado Mensal` (quando o lucro líquido estimado é maior que zero; caso contrário, não há retorno estimado no cenário).

## 3. Critérios de Auditoria e QA
- **Integridade de Dados e Privacidade:** Nenhum dado pessoal, identificação acadêmica, endereço real ou informação sensível deve constar nos arquivos públicos do repositório.
- **Validação de Entradas:** Volumes de venda negativos e margens de contribuição inválidas (zero ou negativas) devem ser bloqueados ou sinalizados com erro explícito.
- **Consistência entre Planilha e Código:** As abas, fórmulas e parâmetros da planilha em `data/modelo_negocio_pizzaria.xlsx` devem refletir as mesmas regras testadas em `tests/test_auditoria_planilha.py`.
- **Rastreabilidade de Mudanças:** Toda alteração em regras de cálculo ou premissas deve ser registrada com mensagem de commit clara e acompanhada de atualização nos testes.
