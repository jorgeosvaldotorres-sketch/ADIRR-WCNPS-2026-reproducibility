# ADIRR WCNPS 2026 — Resultados do piloto técnico v0.1

Data: 2026-09-29
Status: piloto concluído e aprovado. Gate de engenharia satisfeito para
prosseguir ao congelamento (Fase 5) e à execução científica (Fase 6, R=2000).

Não constitui resultado científico do artigo — é validação de engenharia,
conforme já delimitado em `PROTOCOLO_EXPERIMENTAL_v0_1.md` e
`DESENHO_FATORIAL_Q_L_v0_1.md`.

## Execução

- Notebook: `ADIRR_WCNPS_2026_COLAB_v0_4.ipynb`.
- R = 100 (piloto técnico, conforme `ProtocolConfig.pilot_replications`).
- Grade completa: L ∈ {25, 50, 100} × q ∈ {1,00; 0,80; 0,60; 0,40} × M1/M2
  = 24 condições.
- Total: 56.000 linhas de registro D6 (100 réplicas × 24 condições × K
  janelas por condição, K variando com L).
- Seed mestra: 20260922 (inalterada).

## Execução cruzada entre dois ambientes independentes

| Ambiente | Python | NumPy | Pandas | Tempo (100 réplicas) |
|---|---|---|---|---|
| Google Colab (pesquisador) | 3.13.15 | 2.1.3 | 2.2.3 | 63,8 s |
| Validação local (assistente) | 3.11.15 | 2.4.6 | 3.0.6 | 38,5–64,0 s |

Os dois ambientes produziram **resultados numericamente idênticos até a
6ª casa decimal** em todas as 24 condições (ver tabela abaixo). Isso é
evidência direta de reprodutibilidade entre versões de bibliotecas e de
interpretador, consistente com o que a seção 5.2 do manuscrito exige
("execuções deverão ser reproduzíveis a partir dos artefatos armazenados
no repositório"). Recomenda-se citar este teste cruzado no artigo.

## Invariantes verificados (sobre as 100 réplicas, não apenas 1)

1. O100: M1 = M2 em `support`, `counter_support`, `observability`,
   `uncertainty` e `rho`, para os três valores de L — confirmado.
2. M2: `uncertainty = 0` e `rho` válido (não-NaN) em 100% das janelas —
   confirmado.
3. M1/O40: `uncertainty = 1` (e `rho = NaN`) apenas em janelas com
   `evidence_mass = 0` — nenhuma ocorrência nas 100 réplicas (esperado:
   probabilidade nominal ≈0,23 janela vazia em toda a execução científica
   de 2000 réplicas em L=25/O40; com 100 réplicas a expectativa é ainda
   menor).
4. `rho ∈ [0,1]` em toda janela válida — confirmado.
5. Nenhuma janela inválida em nenhuma das 24 condições (`n_invalid = 0`
   em todas as linhas da tabela-resumo).

## Tabela-resumo (`piloto_tecnico_100rep_resumo.csv`)

| L | q | método | ρ médio | dp(ρ) | janelas |
|---|---|---|---|---|---|
| 25 | 0,40 | M1 | 1,0000 | 0,0000 | 4000 |
| 25 | 0,40 | M2 | 0,7003 | 0,0493 | 4000 |
| 25 | 0,60 | M1 | 1,0000 | 0,0000 | 4000 |
| 25 | 0,60 | M2 | 0,8007 | 0,0493 | 4000 |
| 25 | 0,80 | M1 | 1,0000 | 0,0000 | 4000 |
| 25 | 0,80 | M2 | 0,9009 | 0,0404 | 4000 |
| 50 | 0,40 | M1 | 1,0000 | 0,0000 | 2000 |
| 50 | 0,40 | M2 | 0,7003 | 0,0352 | 2000 |
| 50 | 0,60 | M2 | 0,8007 | 0,0353 | 2000 |
| 50 | 0,80 | M2 | 0,9009 | 0,0286 | 2000 |
| 100 | 0,40 | M2 | 0,7003 | 0,0254 | 1000 |
| 100 | 0,60 | M2 | 0,8007 | 0,0253 | 1000 |
| 100 | 0,80 | M2 | 0,9009 | 0,0199 | 1000 |

(tabela completa com as 24 linhas em `piloto_tecnico_100rep_resumo.csv`;
q=1,00 omitido acima por ser sempre ρ=1,0000/dp=0 em ambos os métodos,
por construção do invariante O100)

## Achado científico observado no piloto (não hipotético)

`mean_rho` é **idêntico entre L=25, 50 e 100** para o mesmo q e método —
esperado, pois é a mesma evidência total agregada, apenas particionada em
janelas de tamanhos diferentes. Já `sd_rho` (variabilidade entre janelas)
**decresce monotonicamente conforme L cresce**, para todo q<1,00:

- q=0,40/M2: 0,0493 (L=25) → 0,0352 (L=50) → 0,0254 (L=100)
- q=0,60/M2: 0,0493 (L=25) → 0,0353 (L=50) → 0,0253 (L=100)
- q=0,80/M2: 0,0404 (L=25) → 0,0286 (L=50) → 0,0199 (L=100)

Interpretação: janelas maiores acumulam mais oportunidades de evidência,
reduzindo a variância de `ρ` entre janelas — um efeito estatístico
esperado (redução de variância com tamanho de amostra), mas que só se
torna visível empiricamente com o desenho fatorial q×L, e que M1 não
exibe (M1 tem `sd_rho = 0` em toda condição, porque o agente é
determinístico e M1 nunca introduz suporte negativo). Isso já é
suficiente para uma subseção de Resultados sobre a interação q×L, sem
necessidade da execução científica completa para ser relatado
qualitativamente — a execução científica (R=2000) serve para
quantificar esse efeito com precisão Monte Carlo (MCSE) adequada, não
para descobri-lo.

## Extrapolação de tempo para a execução científica (R=2000)

Com base no tempo real observado (não estimado): 38,5–64,0 s para 100
réplicas → **13–21 minutos para R=2000**, na grade fatorial completa (24
condições). Compute não é fator limitante para a decisão de prazo.

## Decisão

Piloto aprovado. Prossegue-se ao congelamento (Fase 5) do commit que
contém o notebook v0.4 validado, antes da execução científica.
