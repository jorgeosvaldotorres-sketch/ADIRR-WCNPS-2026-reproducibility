# ADIRR WCNPS 2026 — Resultados científicos v0.1 (R=2000)

Data: 2026-09-29
Status: execução científica concluída e aceita. Base para a seção de
Resultados do manuscrito.
Código: commit congelado `3376de5` (branch `wcnps-2026-fase0-d4`), conforme
`06_reprodutibilidade/FREEZE_MANIFESTO_v0_1.md`.

## Execução

- R = 2000 réplicas científicas (conforme `ProtocolConfig.scientific_replications`).
- Grade completa: L ∈ {25, 50, 100} × q ∈ {1,00; 0,80; 0,60; 0,40} × M1/M2.
- Tempo total: 792,7 s (13,21 min).
- Janelas inválidas (evidence_mass=0) em toda a execução: **0**.
- Critério de precisão Monte Carlo (MCSE ≤ 2,5% do DP-Rep, seção 5.8.1 do
  manuscrito) satisfeito nas 24 condições, sem exceção.

## Resultado central: DMA, MAE, Δ pareado (M2−M1)

DMA, MAE e DP-Rep são idênticos entre L=25, 50 e 100 para cada q (ver
seção "Achado metodológico" abaixo para a explicação). A tabela reporta,
portanto, uma linha por q, válida para os três valores de L:

| q | DMA (M1) | DMA (M2) | MAE (M2) | DP-Rep (M2) | Δ̄=M2−M1 | MCSE_Δ |
|---|---|---|---|---|---|---|
| 1,00 | 0,000000 | 0,000000 | 0,000000 | 0,000000 | 0,000000 | 0,000000 |
| 0,80 | 0,000000 | −0,099910 | 0,099910 | 0,006300 | −0,099910 | 0,000141 |
| 0,60 | 0,000000 | −0,199919 | 0,199919 | 0,007908 | −0,199919 | 0,000177 |
| 0,40 | 0,000000 | −0,299769 | 0,299769 | 0,007777 | −0,299769 | 0,000174 |

M1 nunca se desvia da referência O100 (DMA=MAE=0 em toda condição): o
agente cooperativo determinístico nunca produz suporte negativo, e M1
nunca converte ausência em suporte negativo, logo ρ_M1 = 1 sempre, por
construção — não é um resultado a ser testado, é uma verificação de
consistência que passou. M2 degrada de forma aproximadamente linear com a
queda de observabilidade nominal, com MCSE três ordens de grandeza menor
que o efeito estimado — a diferença é estatisticamente inequívoca com
R=2000.

Como DMA(M1)=0 em toda condição, Δ̄(q) = DMA(M2,q) − 0 = DMA(M2,q):
a diferença pareada não adiciona informação além do DMA de M2 neste
cenário específico (agente sem falhas reais). Isso deve ser declarado
explicitamente na Discussão, não apresentado como dois achados
independentes.

## Achado metodológico: a interação q×L NÃO aparece nas métricas primárias

Este é o resultado mais importante deste ciclo de execução, e precisa ser
reportado com precisão, não suavizado.

O desenho fatorial q×L (`DESENHO_FATORIAL_Q_L_v0_1.md`) foi motivado pela
pergunta: o efeito de observabilidade reduzida sobre a reputação depende
da largura da janela de agregação em D2? A resposta, para DMA, MAE e
DP-Rep como definidos no protocolo (seção 5.7 do manuscrito), é **não,
por uma razão analítica, não por limitação estatística**.

### Demonstração

Para o cenário binário, cooperativo, determinístico, com imputação
neutra M2, cada janela produz:

```
rho_janela = 0,5 + 0,5 x taxa_observada_na_janela
D_janela = rho_janela - 1 = -0,5 x (1 - taxa_observada_na_janela)
```

`DMA_r` é a média de `D_janela` entre as K janelas de uma replicação.
Como todas as janelas de uma replicação têm o mesmo tamanho L e a soma
das observações por janela, somada sobre todas as janelas, é igual ao
total de observações da replicação inteira (independente de como T é
particionado em janelas), `DMA_r` é **algebricamente idêntico** para
qualquer L que divida T — não converge para o mesmo valor "no limite",
é constante para qualquer R.

### Confirmação empírica no caso extremo

Testado fora da grade oficial, apenas como verificação: L=1 (1000
janelas de tamanho 1) contra L=1000 (uma única janela cobrindo a
replicação inteira), mesma seed, 3 réplicas:

| replicação | L=1 (DMA) | L=1000 (DMA) |
|---|---|---|
| 0 | −0,317500000 | −0,317500000 |
| 1 | −0,292000000 | −0,292000000 |
| 2 | −0,284000000 | −0,284000000 |

Igualdade exata no intervalo mais extremo possível de L. Não há execução
com R maior, nem qualquer outro valor de L dentro de [1, T], que
produziria um resultado diferente.

### Por que isso não invalida o desenho fatorial nem o esforço de rodá-lo

1. Rodar a grade q×L não foi esforço desperdiçado: descartar a hipótese
   de interação q×L, com prova analítica e confirmação empírica no
   extremo, é um resultado válido — evita que o artigo afirme ou sugira
   uma interação que não existe.
2. A invariância é uma propriedade **deste cenário estacionário**
   (comportamento-verdade constante ao longo de toda a replicação). A
   largura da janela só pode interagir com métricas agregadas quando há
   mudança de comportamento dentro do horizonte observado — exatamente o
   que as etapas futuras (agente on-off, mudança abrupta) introduzem. A
   sensibilidade a L é, portanto, uma pergunta em aberto para essas
   etapas futuras, não uma pergunta fechada para este cenário.
3. A dispersão de ρ por janela observada no piloto (`sd_rho` decrescendo
   com L, ver `RESULTADOS_PILOTO_TECNICO_v0_1.md`) permanece válida como
   estatística descritiva de variabilidade **dentro de uma condição**
   (entre janelas, agregando réplicas), mas é conceitualmente distinta de
   DP-Rep (variabilidade **entre réplicas** da média por replicação) e
   não deve ser citada como evidência de efeito de L sobre DMA/MAE/DP-Rep.

## O que reportar no artigo (orientação para a seção de Resultados)

- Reportar a tabela DMA/MAE/Δ por q (única, válida para os três L).
- Reportar a invariância a L como resultado analítico comprovado, com a
  demonstração e o teste extremo acima, não como ausência de efeito por
  falta de poder estatístico.
- Declarar explicitamente que Δ̄=DMA(M2) neste cenário, e por quê.
- Registrar a sensibilidade a L como pergunta em aberto para as etapas
  futuras com agentes não estacionários (malicioso, on-off), não como
  conclusão negativa geral sobre a arquitetura.

## Artefatos desta execução

- `execucao_cientifica_metricas_finais.csv` — DMA/MAE/DP-Rep/MCSE por
  (método, q, L), 24 linhas.
- `execucao_cientifica_delta_pareado.csv` — Δ̄ e MCSE_Δ por (q, L), 12
  linhas.
- `execucao_cientifica_per_replicacao.csv` — DMA_r/MAE_r/Delta_r por
  (réplica, método, q, L), 48.000 linhas, base para os agregados acima e
  para qualquer reanálise futura sem precisar re-executar a simulação.
