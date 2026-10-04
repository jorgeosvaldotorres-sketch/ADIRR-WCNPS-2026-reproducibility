# ADIRR WCNPS 2026 — Protocolo experimental v0.1

Data: 2026-09-22  
Status: consolidado para início da implementação e piloto técnico.

## Escopo

Primeira instanciação experimental parcial do caminho:

**D0 → D1 → D2 → D3 → D4 → D6**

D5 e os elementos não necessários ao primeiro teste permanecem fora do escopo.

## Configuração principal

| Elemento | Valor |
|---|---|
| Perfil comportamental | agente cooperativo determinístico |
| Granularidade | 1 oportunidade de interação por tick |
| Horizonte | T = 1000 |
| Observabilidade | MCAR, Bernoulli independente |
| q | 1.00, 0.80, 0.60, 0.40 |
| Janela D2 | tumbling |
| L | 50 |
| S | 50 |
| K | 20 |
| Baseline | imputação neutra unitária na interface D2→D3 |
| Pseudo-evidência | η° = (0.5, 0.5) |
| Ground truth | comportamento sempre cooperativo |
| Referência reputacional | O100 da mesma implementação |
| R piloto | 100 |
| R científico | 2000 |
| Seed mestra | 20260922 |
| Precisão MCSE | ≤ 2.5% do DP entre replicações para medidas baseadas em média |
| Métricas primárias | DMA, MAE, DP-Rep, diferença pareada M2−M1 |
| Incerteza experimental | MCSE |
| RMSE | secundário/opcional |

## Aleatoriedade

Cada replicação recebe um stream-filho independente derivado da seed mestra.

Dentro da replicação, uma única sequência U(r,t) ~ Uniforme(0,1) gera todos os níveis q:

O(r,t;q) = 1[U(r,t) ≤ q].

As máscaras são aninhadas e M1/M2 usam a mesma máscara.

## Invariantes

1. M1 e M2 compartilham oportunidades, contexto, janelas, parâmetros e código D3/D4.
2. O100 deve produzir M1=M2.
3. Pseudo-evidência só pode surgir em posições O=0.
4. Pseudo-evidência não pode ser registrada como evento real de D0/D1.
5. Falhas devem ser registradas, nunca descartadas silenciosamente.
6. D3/D4 não podem ser substituídos por formulações ad hoc.

## Notebook

Notebook inicial: 01_colab/ADIRR_WCNPS_2026_COLAB_v0_1.ipynb

O notebook implementa configuração, streams/seed, D0, validação D1, observabilidade D2, janelas, baseline M1/M2, invariantes pré-D3, contrato D6, funções de métricas e checks globais.

D3 e D4 permanecem como interfaces não implementadas até revisão da operacionalização fiel ao artigo-base.

## Gate para piloto

O piloto técnico de 100 replicações só poderá ser executado depois de:

1. D3 implementado e revisado;
2. D4 implementado e revisado;
3. D6 mínimo implementado;
4. teste unitário O100 M1=M2 aprovado;
5. persistência de seeds, máscaras e versões verificada.

## Gate para execução científica

As 2000 replicações científicas só serão executadas após piloto aprovado, código/parâmetros congelados, versão do notebook registrada, checks automáticos aprovados e diretório de resultados preparado.