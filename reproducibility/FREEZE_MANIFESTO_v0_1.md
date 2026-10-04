# ADIRR WCNPS 2026 — Manifesto de congelamento (freeze) v0.1

Data: 2026-09-29
Status: código e parâmetros congelados para a execução científica (R=2000).

## O que está sendo congelado

O código-fonte do notebook experimental na versão que passou no piloto
técnico (100 réplicas, 24 condições, 0 invariantes violados, cross-validado
em dois ambientes independentes — ver
`04_resultados/RESULTADOS_PILOTO_TECNICO_v0_1.md`).

- Arquivo congelado: `01_colab/ADIRR_WCNPS_2026_COLAB_v0_4.ipynb`
- Commit congelado: `3376de5` (branch `wcnps-2026-fase0-d4`) — "Fecha decisao
  de uncertainty (Fase 1) e implementa D6 (Eq. 7)"
- Tag git: `freeze-wcnps2026-d0d6-v0.4`

Commits posteriores a `3376de5` neste branch (documentação de piloto,
matriz, este manifesto) **não alteram nenhuma célula de código** do
notebook. Qualquer alteração de código a partir de agora exige nova tag de
freeze e invalida a comparabilidade com o piloto já validado.

## Parâmetros congelados (`ProtocolConfig`)

```
master_seed = 20260922
T = 1000
L_levels = (25, 50, 100)
q_levels = (1.00, 0.80, 0.60, 0.40)
pilot_replications = 100      # ja executado
scientific_replications = 2000  # a executar
mcse_ratio_target = 0.025
neutral_weight_positive = 0.5
neutral_weight_negative = 0.5
```

## Versões de biblioteca validadas (dois ambientes independentes)

| Ambiente | Python | NumPy | Pandas |
|---|---|---|---|
| Google Colab (pesquisador) | 3.13.15 | 2.1.3 | 2.2.3 |
| Validação local (assistente) | 3.11.15 | 2.4.6 | 3.0.6 |

Resultados idênticos até a 6ª casa decimal nos dois ambientes — a execução
científica não está restrita a uma versão específica de biblioteca dentro
dessa faixa já testada.

## Regras de instanciação congeladas (não numéricas, mas parte do freeze)

- D3 (`OPERACIONALIZACAO_D3_v0_1.md`): φ instancia taxa de sucesso, taxa de
  falha e taxa de observabilidade a partir de `E_{a,c}(W_t)` e
  `m_{a,c}(W_t)`.
- D4 (`OPERACIONALIZACAO_D4_v0_1.md`): B = (support, counter_support,
  uncertainty, observability); uncertainty binária (1 sse evidence_mass=0),
  decisão confirmada em 2026-09-28; E_dir=E_ind=vazio; G_prov de fonte
  única; π_t explícito.
- D6 (`OPERACIONALIZACAO_D6_v0_1.md`): rho = support/(support+counter_support)
  quando evidence_mass>0, senão NaN com valid=False.
- Desenho fatorial (`DESENHO_FATORIAL_Q_L_v0_1.md`): grade completa L×q×método,
  24 condições. Plano de contingência (recuo para L=50) permanece disponível
  e não exige nova implementação — apenas filtrar o eixo L na análise.

## O que NÃO está congelado

- Código de análise/visualização pós-execução (ainda não escrito — depende
  dos dados brutos da execução científica).
- Redação do artigo (Resumo, Resultados, Discussão, Conclusão).
- Decisão sobre expansão para agente malicioso/on-off (fora do escopo desta
  etapa, conforme decisões estratégicas originais).

## Autorização

Este manifesto documenta o estado congelado. A execução científica
(R=2000) só deve começar após o pesquisador autorizar explicitamente,
dado que qualquer resultado gerado a partir daqui passa a ser candidato a
resultado científico do artigo, não apenas validação de engenharia.
