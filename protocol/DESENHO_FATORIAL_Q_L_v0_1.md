# ADIRR WCNPS 2026 — Desenho fatorial q × L v0.1

Data: 2026-09-28
Status: decisão de protocolo experimental, aguardando início da execução.

## Decisão

O protocolo v0.1 previa L=50 como configuração principal e L=25/L=100 como
análise de sensibilidade opcional, fora do escopo mínimo (seção 5.9.5 do
manuscrito 2.9). Esta decisão promove a sensibilidade de L de extensão
opcional a **eixo experimental principal**, combinado factorialmente com os
níveis de observabilidade já definidos.

## Desenho resultante

- Observabilidade: q ∈ {1,00; 0,80; 0,60; 0,40} (inalterado, já consolidado
  em `MECANISMO_OBSERVABILIDADE_v01_2026-09-22.md`).
- Janelas D2: L ∈ {25; 50; 100}, com S=L (tumbling), produzindo K = 40, 20,
  10 janelas por replicação respectivamente. T=1000 permanece fixo.
- Método: M1 (ausência preservada) × M2 (imputação neutra), inalterado.
- Total de condições: 4 (q) × 3 (L) × 2 (método) = 24 condições pareadas
  por replicação.

## Por que isso não altera a arquitetura

L e os níveis de q são parâmetros do protocolo experimental, não da ADIRR.
Nenhuma equação (1)-(7) do artigo-base é alterada por este desenho. A
justificativa segue a mesma regra já registrada em
`WCNPS_2026_DECISOES_ESTRATEGICAS_2026-09-22.md`, item 8: parâmetros sem
valor canônico na literatura são parâmetros de cenário, sujeitos a análise
de sensibilidade.

## Justificativa científica

A pergunta original ("ausência de observação ≠ comportamento neutro")
testa apenas o eixo q. O eixo L introduz uma pergunta complementar: o
efeito da observabilidade reduzida sobre a saída reputacional depende da
granularidade temporal da agregação em D2? Isso é relevante porque D2
define explicitamente que "windows may be fixed, sliding, or adaptive" e
que a escolha "affects sensitivity to recent change, retained history, and
processing cost" (artigo-base, seção 3.2). Testar q isoladamente, sem
variar L, deixaria essa dependência arquitetural sem exame empírico.

A literatura de concept drift já citada no manuscrito (Player e Griffiths,
tamanhos de janela 50/100/200; Gama et al., trade-offs de tamanho de
janela) já apoia a relevância de L como fator, não apenas como robustez
acessória.

## Consequência prática sobre o volume de resultados

24 condições pareadas (em vez de 8, no desenho L=50-only) devem ser
reportadas como tabelas/matrizes bidimensionais (q × L) por método e por
métrica, não como texto condição a condição. Isso contém o custo de
redação apesar do desenho maior.

## Plano de contingência (declarado a priori, não é recuo silencioso)

Caso o piloto técnico (Fase 4) ou a proximidade do prazo de submissão
indiquem inviabilidade da grade completa, o desenho reduz-se para
L=50 apenas (4 q × 1 L × 2 métodos = 8 condições), que permanece
cientificamente completo e autossuficiente para a pergunta original. Este
recuo é parte do desenho, registrado antes da execução, e não constitui
enfraquecimento não documentado do experimento.

## Não afetado por esta decisão

- D0–D6 e Equações (1)–(7) do artigo-base.
- Agente cooperativo determinístico.
- Seed mestra (20260922) e política de streams por replicação.
- Métricas mínimas: DMA, MAE, DP-Rep, diferença pareada M2−M1, MCSE.
- Exclusões já registradas: D5, proveniência completa, DLT, governança,
  ataques sofisticados, agentes malicioso/on-off, recomendação indireta.
